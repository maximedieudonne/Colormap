import json
from dash import Input, Output, State, ctx, html, no_update
import plotly.graph_objects as go

# Global variables for colormap data
colormap_data = [{"color": "white", "min": 0, "max": 100}]
saved_colormaps = {}
background_color = "white"
mincolormap = 0
maxcolormap = 100

def replace_background_color(new_bg_color):
    """Replace the background color in the colormap."""
    global colormap_data, background_color
    for entry in colormap_data:
        if entry["color"] == background_color:
            entry["color"] = new_bg_color
    background_color = new_bg_color

def update_intervals(new_color, new_min, new_max):
    """Update colormap intervals dynamically based on new input."""
    global colormap_data
    updated_data = []

    for entry in colormap_data:
        if entry["max"] <= new_min or entry["min"] >= new_max:
            # Keep intervals that are completely outside the new range
            updated_data.append(entry)
        else:
            # Adjust or split overlapping intervals
            if entry["min"] < new_min:
                updated_data.append({"color": entry["color"], "min": entry["min"], "max": new_min})
            if entry["max"] > new_max:
                updated_data.append({"color": entry["color"], "min": new_max, "max": entry["max"]})

    # Insert the new interval
    updated_data.append({"color": new_color, "min": new_min, "max": new_max})
    updated_data.sort(key=lambda x: x["min"])

    colormap_data = updated_data

def trim_and_expand_colormap(new_mincolormap, new_maxcolormap):
    """Trim or expand the colormap based on new bounds."""
    global colormap_data, background_color

    updated_data = []

    for entry in colormap_data:
        if entry["max"] < new_mincolormap or entry["min"] > new_maxcolormap:
            # Remove intervals completely outside the bounds
            continue
        if entry["min"] < new_mincolormap and entry["max"] > new_mincolormap:
            # Adjust the min to the new mincolormap
            entry["min"] = new_mincolormap
        if entry["max"] > new_maxcolormap and entry["min"] < new_maxcolormap:
            # Adjust the max to the new maxcolormap
            entry["max"] = new_maxcolormap
        updated_data.append(entry)

    # Add background color if needed
    if updated_data and updated_data[0]["min"] > new_mincolormap:
        updated_data.insert(0, {"color": background_color, "min": new_mincolormap, "max": updated_data[0]["min"]})
    elif not updated_data:
        updated_data = [{"color": background_color, "min": new_mincolormap, "max": new_maxcolormap}]

    if updated_data and updated_data[-1]["max"] < new_maxcolormap:
        updated_data.append({"color": background_color, "min": updated_data[-1]["max"], "max": new_maxcolormap})

    # Merge consecutive background color intervals
    merged_data = []
    for entry in updated_data:
        if merged_data and entry["color"] == merged_data[-1]["color"]:
            merged_data[-1]["max"] = entry["max"]
        else:
            merged_data.append(entry)

    colormap_data = merged_data

def normalize_colormap(new_mincolormap, new_maxcolormap):
    """Normalize the colormap to fit within a fixed length, ensuring min and max are constant."""
    global colormap_data

    total_range = new_maxcolormap - new_mincolormap
    normalized_data = []

    for entry in colormap_data:
        normalized_min = (entry["min"] - new_mincolormap) / total_range
        normalized_max = (entry["max"] - new_mincolormap) / total_range
        normalized_data.append({"color": entry["color"], "min": normalized_min, "max": normalized_max})

    return normalized_data

def generate_colormap(new_mincolormap, new_maxcolormap):
    """Generate a Plotly figure for the colormap."""
    normalized_data = normalize_colormap(new_mincolormap, new_maxcolormap)
    fig = go.Figure()

    for entry in normalized_data:
        fig.add_trace(
            go.Scatter(
                x=[entry["min"], entry["max"]],
                y=[1, 1],
                mode="lines",
                line=dict(color=entry["color"], width=20),
                showlegend=False,
            )
        )

    # Ensure all tick values and text are present
    tickvals = [entry["min"] for entry in normalized_data] + [entry["max"] for entry in normalized_data]
    ticktext = [f"{new_mincolormap + t * (new_maxcolormap - new_mincolormap):.2f}" for t in tickvals]

    fig.update_layout(
        xaxis=dict(
            title="Normalized Range",
            range=[0, 1],
            tickvals=tickvals,
            ticktext=ticktext,
            showgrid=False,
            zeroline=False,
            tickangle=0,
        ),
        yaxis=dict(visible=False),
        height=250,
        margin=dict(l=20, r=20, t=20, b=50),
    )
    return fig

def register_callbacks(app):
    @app.callback(
        [
            Output("colormap-visual", "figure"),
            Output("color-info", "children"),
            Output("colormap-dropdown", "options"),
            Output("save-status", "children"),
            Output("background-color-dropdown", "options"),
        ],
        [
            Input("add-color-btn", "n_clicks"),
            Input("save-colormap-btn", "n_clicks"),
            Input("reset-colormap-btn", "n_clicks"),
            Input("colormap-dropdown", "value"),
            Input("background-color-dropdown", "value"),
            Input("apply-bounds-btn", "n_clicks"),
        ],
        [
            State("color-dropdown", "value"),
            State("min-range", "value"),
            State("max-range", "value"),
            State("mincolormap", "value"),
            State("maxcolormap", "value"),
        ],
    )
    def update_colormap(
        n_clicks_add, n_clicks_save, n_clicks_reset, selected_colormap, new_bg_color, n_clicks_apply_bounds,
        color, min_range, max_range, new_mincolormap, new_maxcolormap
    ):
        global colormap_data, saved_colormaps, background_color, mincolormap, maxcolormap
        save_status = ""

        # Provide default values for new_mincolormap and new_maxcolormap if they are None
        if new_mincolormap is None:
            new_mincolormap = 0
        if new_maxcolormap is None:
            new_maxcolormap = 100

        # Apply colormap bounds
        if ctx.triggered_id == "apply-bounds-btn":
            mincolormap, maxcolormap = new_mincolormap, new_maxcolormap
            trim_and_expand_colormap(mincolormap, maxcolormap)

        # Update background color if changed
        if new_bg_color and new_bg_color != background_color:
            replace_background_color(new_bg_color)

        # Add a new color interval
        if ctx.triggered_id == "add-color-btn" and color and min_range is not None and max_range is not None:
            update_intervals(color, min_range, max_range)

        # Save the current colormap
        if ctx.triggered_id == "save-colormap-btn":
            colormap_name = f"colormap_{len(saved_colormaps) + 1:02d}"
            saved_colormaps[colormap_name] = {
                "data": list(colormap_data),
                "mincolormap": mincolormap,
                "maxcolormap": maxcolormap,
            }
            save_status = f"{colormap_name} saved"
            with open(f"{colormap_name}.json", "w") as file:
                json.dump(saved_colormaps[colormap_name], file, indent=4)

        # Reset to default colormap
        if ctx.triggered_id == "reset-colormap-btn":
            colormap_data = [{"color": "white", "min": 0, "max": 100}]
            mincolormap, maxcolormap = 0, 100
            background_color = "white"
            save_status = "Colormap reset to default"

        # Load a selected colormap
        if ctx.triggered_id == "colormap-dropdown" and selected_colormap:
            selected_data = saved_colormaps[selected_colormap]
            colormap_data = selected_data["data"]
            mincolormap = selected_data["mincolormap"]
            maxcolormap = selected_data["maxcolormap"]

        # Generate the visualization
        colormap_figure = generate_colormap(mincolormap, maxcolormap)
        colormap_info = [
            f"Color: {entry['color']}, Range: [{entry['min']}, {entry['max']}]"
            for entry in colormap_data
        ]

        dropdown_options = [{"label": name, "value": name} for name in saved_colormaps.keys()]
        bg_color_options = [{"label": c.title(), "value": c} for c in {"white", "black", "gray", "lightblue", "lightgreen", new_bg_color}]

        return colormap_figure, [html.Div(info) for info in colormap_info], dropdown_options, save_status, bg_color_options
