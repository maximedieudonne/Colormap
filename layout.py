from dash import html, dcc

def create_layout():
    return html.Div(
        [
            html.H1("Interactive Colormap Builder", style={"textAlign": "center"}),

            html.Div(
                [
                    html.Label("Select Color:"),
                    dcc.Dropdown(
                        id="color-dropdown",
                        options=[
                            {"label": color.title(), "value": color}
                            for color in ["red", "blue", "green", "orange", "purple", "yellow", "cyan", "magenta", "gray", "brown"]
                        ],
                        placeholder="Select a color",
                    ),
                    html.Label("Minimum Range:"),
                    dcc.Input(id="min-range", type="number", placeholder="Enter min range"),
                    html.Label("Maximum Range:"),
                    dcc.Input(id="max-range", type="number", placeholder="Enter max range"),
                    html.Button("Add Color", id="add-color-btn"),
                    html.Label("Background Color:"),
                    dcc.Dropdown(
                        id="background-color-dropdown",
                        options=[
                            {"label": "White", "value": "white"},
                            {"label": "Black", "value": "black"},
                            {"label": "Gray", "value": "gray"},
                            {"label": "Light Blue", "value": "lightblue"},
                            {"label": "Light Green", "value": "lightgreen"},
                        ],
                        value="white",
                    ),
                    html.Button("Save Colormap", id="save-colormap-btn"),
                    html.Span(id="save-status", style={"color": "green"}),
                    html.Label("My Colormaps:"),
                    dcc.Dropdown(id="colormap-dropdown", placeholder="Select a colormap to load"),
                    html.Button("Reset Colormap", id="reset-colormap-btn"),
                ],
                style={"width": "30%", "display": "inline-block", "padding": "10px"},
            ),
            html.Div(
                [
                    html.Label("Colormap Visualization:"),
                    dcc.Graph(id="colormap-visual"),
                    html.Div(id="color-info", style={"marginTop": "20px"}),
                ],
                style={"width": "65%", "display": "inline-block", "padding": "10px"},
            ),
        ],
        style={"padding": "20px"},
    )
