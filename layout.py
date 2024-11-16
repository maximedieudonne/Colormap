from dash import html, dcc

def create_layout():
    return html.Div(
        style={
            "fontFamily": "Arial, sans-serif",
            "backgroundColor": "#f4f4f4",
            "padding": "20px",
        },
        children=[
            # Header
            html.Div(
                style={
                    "textAlign": "center",
                    "backgroundColor": "#3e4c6d",
                    "padding": "15px",
                    "color": "white",
                    "borderRadius": "8px",
                    "marginBottom": "20px",
                },
                children=[
                    html.H1(
                        "Interactive Colormap Builder",
                        style={"margin": "0", "fontWeight": "bold", "fontSize": "28px"},
                    ),
                    html.P("Advanced visualization and customization tool for colormaps"),
                ],
            ),

            # Main content
            html.Div(
                style={
                    "display": "flex",
                    "flexDirection": "row",
                    "justifyContent": "space-between",
                },
                children=[
                    # Left panel: Options
                    html.Div(
                        style={
                            "width": "30%",
                            "backgroundColor": "#ffffff",
                            "padding": "15px",
                            "borderRadius": "8px",
                            "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        },
                        children=[
                            # Section: Background Color
                            html.Div(
                                style={
                                    "marginBottom": "20px",
                                    "paddingBottom": "15px",
                                    "borderBottom": "1px solid #d3d3d3",
                                },
                                children=[
                                    html.Label(
                                        "Background Color",
                                        style={"fontWeight": "bold", "fontSize": "16px"},
                                    ),
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
                                        style={
                                            "marginTop": "10px",
                                            "padding": "5px",
                                            "fontSize": "14px",
                                        },
                                    ),
                                ],
                            ),
                            # Section: Add Color
                            html.Div(
                                style={
                                    "marginBottom": "20px",
                                    "paddingBottom": "15px",
                                    "borderBottom": "1px solid #d3d3d3",
                                },
                                children=[
                                    html.Label(
                                        "Add Color Range",
                                        style={"fontWeight": "bold", "fontSize": "16px"},
                                    ),
                                    html.Div(
                                        style={"marginTop": "10px"},
                                        children=[
                                            html.Label(
                                                "Select Color:",
                                                style={"fontSize": "14px"},
                                            ),
                                            dcc.Dropdown(
                                                id="color-dropdown",
                                                options=[
                                                    {"label": c.title(), "value": c}
                                                    for c in [
                                                        "red",
                                                        "blue",
                                                        "green",
                                                        "orange",
                                                        "purple",
                                                        "yellow",
                                                        "cyan",
                                                        "magenta",
                                                        "gray",
                                                        "brown",
                                                    ]
                                                ],
                                                placeholder="Select a color",
                                                style={
                                                    "marginTop": "5px",
                                                    "padding": "5px",
                                                    "fontSize": "14px",
                                                },
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        style={"marginTop": "10px"},
                                        children=[
                                            html.Label(
                                                "Minimum Range:",
                                                style={"fontSize": "14px"},
                                            ),
                                            dcc.Input(
                                                id="min-range",
                                                type="number",
                                                placeholder="Enter min range",
                                                style={
                                                    "width": "100%",
                                                    "padding": "5px",
                                                    "fontSize": "14px",
                                                },
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        style={"marginTop": "10px"},
                                        children=[
                                            html.Label(
                                                "Maximum Range:",
                                                style={"fontSize": "14px"},
                                            ),
                                            dcc.Input(
                                                id="max-range",
                                                type="number",
                                                placeholder="Enter max range",
                                                style={
                                                    "width": "100%",
                                                    "padding": "5px",
                                                    "fontSize": "14px",
                                                },
                                            ),
                                        ],
                                    ),
                                    html.Button(
                                        "Add Color",
                                        id="add-color-btn",
                                        n_clicks=0,
                                        style={
                                            "marginTop": "15px",
                                            "padding": "10px 15px",
                                            "fontSize": "14px",
                                            "backgroundColor": "#3e4c6d",
                                            "color": "white",
                                            "border": "none",
                                            "borderRadius": "4px",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ],
                            ),
                            # Section: Save and Load
                            html.Div(
                                children=[
                                    html.Label(
                                        "Save & Load Colormaps",
                                        style={"fontWeight": "bold", "fontSize": "16px"},
                                    ),
                                    html.Div(
                                        style={"marginTop": "10px"},
                                        children=[
                                            html.Button(
                                                "Save Colormap",
                                                id="save-colormap-btn",
                                                n_clicks=0,
                                                style={
                                                    "padding": "10px 15px",
                                                    "fontSize": "14px",
                                                    "backgroundColor": "#3e4c6d",
                                                    "color": "white",
                                                    "border": "none",
                                                    "borderRadius": "4px",
                                                    "cursor": "pointer",
                                                    "marginRight": "10px",
                                                },
                                            ),
                                            html.Span(
                                                id="save-status",
                                                style={
                                                    "fontSize": "14px",
                                                    "color": "green",
                                                },
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        style={"marginTop": "15px"},
                                        children=[
                                            html.Label(
                                                "My Colormaps:",
                                                style={"fontSize": "14px"},
                                            ),
                                            dcc.Dropdown(
                                                id="colormap-dropdown",
                                                placeholder="Select a colormap to load",
                                                style={
                                                    "marginTop": "5px",
                                                    "padding": "5px",
                                                    "fontSize": "14px",
                                                },
                                            ),
                                        ],
                                    ),
                                    html.Button(
                                        "Reset Colormap",
                                        id="reset-colormap-btn",
                                        n_clicks=0,
                                        style={
                                            "marginTop": "15px",
                                            "padding": "10px 15px",
                                            "fontSize": "14px",
                                            "backgroundColor": "#d9534f",
                                            "color": "white",
                                            "border": "none",
                                            "borderRadius": "4px",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Right panel: Visualization
                    html.Div(
                        style={
                            "width": "65%",
                            "backgroundColor": "#ffffff",
                            "padding": "15px",
                            "borderRadius": "8px",
                            "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                        },
                        children=[
                            html.Label(
                                "Colormap Visualization",
                                style={
                                    "fontWeight": "bold",
                                    "fontSize": "16px",
                                    "marginBottom": "10px",
                                    "display": "block",
                                },
                            ),
                            dcc.Graph(id="colormap-visual"),
                            html.Div(
                                id="color-info",
                                style={
                                    "marginTop": "20px",
                                    "fontSize": "14px",
                                    "lineHeight": "1.5",
                                    "color": "#333",
                                },
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
