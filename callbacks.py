import json
from dash import Input, Output, State, ctx, html, no_update
import plotly.graph_objects as go
from matplotlib.colors import to_hex, to_rgba

# Global variables for colormap data
colormap_data = [{"color": "white", "min": 0, "max": 100}]
saved_colormaps = {}
background_color = "white"

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

def generate_colormap():
    """Generate a Plotly figure for the colormap."""
    fig = go.Figure()

    for entry in colormap_data:
        fig.add_trace(
            go.Scatter(
                x=[entry["min"], entry["max"]],
                y=[1, 1],
                mode="lines",
                line=dict(color=entry["color"], width=20),
                showlegend=False,
            )
        )

    fig.update_layout(
        xaxis=dict(
            title="Range",
            range=[0, 100],
            tickvals=[entry["min"] for entry in colormap_data] + [entry["max"] for entry in colormap_data],
            ticktext=[entry["min"] for entry in colormap_data] + [entry["max"] for entry in colormap_data],
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
        ],
        [
            State("color-dropdown", "value"),
            State("min-range", "value"),
            State("max-range", "value"),
        ],
    )
    def update_colormap(
        n_clicks_add, n_clicks_save, n_clicks_reset, selected_colormap, new_bg_color, color, min_range, max_range
    ):
        global colormap_data, saved_colormaps, background_color
        save_status = ""

        # Update background color if changed
        if new_bg_color and new_bg_color != background_color:
            replace_background_color(new_bg_color)

        # Add a new color interval
        if ctx.triggered_id == "add-color-btn" and color and min_range is not None and max_range is not None:
            update_intervals(color, min_range, max_range)

        # Save the current colormap
        if ctx.triggered_id == "save-colormap-btn":
            colormap_name = f"colormap_{len(saved_colormaps) + 1:02d}"
            saved_colormaps[colormap_name] = list(colormap_data)
            save_status = f"{colormap_name} saved"
            with open(f"{colormap_name}.json", "w") as file:
                json.dump(colormap_data, file, indent=4)

        # Reset to default colormap
        if ctx.triggered_id == "reset-colormap-btn":
            colormap_data = [{"color": "white", "min": 0, "max": 100}]
            background_color = "white"
            save_status = "Colormap reset to default"

        # Load a selected colormap
        if ctx.triggered_id == "colormap-dropdown" and selected_colormap:
            colormap_data = saved_colormaps[selected_colormap]

        # Generate the visualization
        colormap_figure = generate_colormap()
        colormap_info = [
            f"Color: {entry['color']}, Range: [{entry['min']}, {entry['max']}]"
            for entry in colormap_data
        ]

        dropdown_options = [{"label": name, "value": name} for name in saved_colormaps.keys()]
        bg_color_options = [{"label": c.title(), "value": c} for c in {"white", "black", "gray", "lightblue", "lightgreen", new_bg_color}]

        return colormap_figure, [html.Div(info) for info in colormap_info], dropdown_options, save_status, bg_color_options
