from dash import html, dcc

def create_layout():
    return html.Div(
        [
            html.H1("Interactive Colormap Builder", style={"textAlign": "center"}),

            # Input Section
            html.Div(
                [
                    html.Label("Select Color:"),
                    dcc.Dropdown(
                        id="color-dropdown",
                        options=[
                            {"label": "Red", "value": "red"},
                            {"label": "Blue", "value": "blue"},
                            {"label": "Green", "value": "green"},
                            {"label": "Orange", "value": "orange"},
                            {"label": "Purple", "value": "purple"},
                            {"label": "Yellow", "value": "yellow"},
                            {"label": "Cyan", "value": "cyan"},
                            {"label": "Magenta", "value": "magenta"},
                            {"label": "Gray", "value": "gray"},
                            {"label": "Brown", "value": "brown"},
                        ],
                        placeholder="Select a color",
                    ),
                    html.Br(),
                    html.Label("Minimum Range:"),
                    dcc.Input(
                        id="min-range",
                        type="number",
                        placeholder="Enter min range",
                        style={"width": "100%"},
                    ),
                    html.Br(),
                    html.Label("Maximum Range:"),
                    dcc.Input(
                        id="max-range",
                        type="number",
                        placeholder="Enter max range",
                        style={"width": "100%"},
                    ),
                    html.Br(),
                    html.Button("Add Color", id="add-color-btn", n_clicks=0),
                ],
                style={"width": "30%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"},
            ),

            # Visualization Section
            html.Div(
                [
                    html.Label("Colormap Visualization:"),
                    dcc.Graph(id="colormap-visual", style={"height": "200px", "width": "100%"}),
                    html.Div(
                        id="color-info",
                        style={"marginTop": "20px", "fontSize": "16px", "textAlign": "left"},
                    ),
                ],
                style={"width": "65%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"},
            ),
        ],
        style={"padding": "20px"},
    )