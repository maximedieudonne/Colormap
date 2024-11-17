import json
from dash import Input, Output, State, ctx, html, no_update
import plotly.graph_objects as go
import base64
import io

# Global variables for colormap data
colormap_data = [{"color": "white", "min": 0, "max": 100}]
saved_colormaps = {}
background_color = "white"

def generate_colormap():
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
            Output("save-status", "children"),
        ],
        [
            Input("add-color-btn", "n_clicks"),
            Input("save-colormap-btn", "n_clicks"),
            Input("load-colormap-upload", "contents"),
            Input("reset-colormap-btn", "n_clicks"),
        ],
        [
            State("color-dropdown", "value"),
            State("min-range", "value"),
            State("max-range", "value"),
        ],
    )
    def update_colormap(n_clicks_add, n_clicks_save, upload_contents, n_clicks_reset, color, min_range, max_range):
        global colormap_data
        save_status = ""

        # Handle Add Color button
        if ctx.triggered_id == "add-color-btn" and color and min_range is not None and max_range is not None:
            colormap_data.append({"color": color, "min": min_range, "max": max_range})
            colormap_data.sort(key=lambda x: x["min"])

        # Handle Save Colormap button
        if ctx.triggered_id == "save-colormap-btn":
            save_status = "Colormap saved successfully"
            with open("saved_colormap.json", "w") as file:
                json.dump(colormap_data, file, indent=4)

        # Handle Load Colormap upload
        if ctx.triggered_id == "load-colormap-upload" and upload_contents:
            content_type, content_string = upload_contents.split(",")
            decoded = base64.b64decode(content_string)
            try:
                loaded_colormap = json.load(io.StringIO(decoded.decode("utf-8")))
                colormap_data = loaded_colormap
                save_status = "Colormap loaded successfully"
            except Exception as e:
                save_status = f"Error loading colormap: {e}"

        # Handle Reset Colormap button
        if ctx.triggered_id == "reset-colormap-btn":
            colormap_data = [{"color": "white", "min": 0, "max": 100}]
            save_status = "Colormap reset to default"

        # Generate the colormap visualization
        colormap_figure = generate_colormap()
        colormap_info = [
            f"Color: {entry['color']}, Range: [{entry['min']}, {entry['max']}]"
            for entry in colormap_data
        ]

        return colormap_figure, [html.Div(info) for info in colormap_info], save_status
