from dash import Input, Output, State, ctx, html
import plotly.graph_objects as go

# Store colormap data
colormap_data = [{"color": "white", "min": 0, "max": 100}]

def split_existing_intervals(new_entry):
    """
    Adjusts existing intervals to accommodate the new entry without overlap.
    """
    global colormap_data
    new_min, new_max, new_color = new_entry["min"], new_entry["max"], new_entry["color"]
    updated_data = []

    for entry in colormap_data:
        entry_min, entry_max, entry_color = entry["min"], entry["max"], entry["color"]

        # Case 1: No overlap (keep as is)
        if entry_max <= new_min or entry_min >= new_max:
            updated_data.append(entry)

        # Case 2: Partial overlap on the left
        elif entry_min < new_min < entry_max:
            updated_data.append({"color": entry_color, "min": entry_min, "max": new_min})

        # Case 3: Partial overlap on the right
        if entry_min < new_max < entry_max:
            updated_data.append({"color": entry_color, "min": new_max, "max": entry_max})

    # Add the new color range
    updated_data.append(new_entry)
    return updated_data

def ensure_white_intervals():
    """
    Ensures that white intervals fill any gaps in the colormap.
    """
    global colormap_data
    colormap_data.sort(key=lambda x: x["min"])  # Sort by range start
    filled_data = []

    for i in range(len(colormap_data) - 1):
        filled_data.append(colormap_data[i])
        # Insert a white range if there's a gap between this and the next interval
        if colormap_data[i]["max"] < colormap_data[i + 1]["min"]:
            filled_data.append({"color": "white", "min": colormap_data[i]["max"], "max": colormap_data[i + 1]["min"]})

    filled_data.append(colormap_data[-1])  # Add the last range
    colormap_data = filled_data

def generate_colormap():
    """
    Generates a Plotly colorbar visualization based on the colormap data.
    """
    fig = go.Figure()

    # Extract transitions for tick labels
    transitions = sorted(set([entry["min"] for entry in colormap_data] + [entry["max"] for entry in colormap_data]))

    for entry in colormap_data:
        fig.add_trace(
            go.Scatter(
                x=[entry["min"], entry["max"]],
                y=[1, 1],  # Dummy data to create a horizontal bar
                mode="lines",
                line=dict(color=entry["color"], width=20),
                showlegend=False,
            )
        )
    
    fig.update_layout(
        xaxis=dict(
            title="Range",
            range=[0, 100],
            tickvals=transitions,  # Add the transitions as tick values
            ticktext=[str(val) for val in transitions],  # Add the transitions as tick labels
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            visible=False,
        ),
        height=200,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig

def format_colormap_info():
    """
    Generates a formatted string representation of the colormap data.
    """
    return [
        f"Color: {entry['color']}, Range: [{entry['min']}, {entry['max']}]"
        for entry in colormap_data
    ]

def register_callbacks(app):
    @app.callback(
        [Output("colormap-visual", "figure"), Output("color-info", "children")],
        Input("add-color-btn", "n_clicks"),
        State("color-dropdown", "value"),
        State("min-range", "value"),
        State("max-range", "value"),
    )
    def update_colormap(n_clicks, color, min_range, max_range):
        if ctx.triggered_id == "add-color-btn" and color and min_range is not None and max_range is not None:
            # Process the new entry
            new_entry = {"color": color, "min": min_range, "max": max_range}
            global colormap_data
            colormap_data = split_existing_intervals(new_entry)
            ensure_white_intervals()  # Fill gaps with white

        # Generate updated colormap figure and info
        colormap_figure = generate_colormap()
        colormap_info = format_colormap_info()

        return colormap_figure, [html.Div(info) for info in colormap_info]