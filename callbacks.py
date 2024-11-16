import json
import base64
from dash import Input, Output, State, ctx, html, no_update
import plotly.graph_objects as go
from matplotlib.colors import to_hex, to_rgba

# Store colormap data
colormap_data = [{"color": "white", "min": 0, "max": 100}]

# Function to convert color names to hex
def color_to_hex(color_name):
    try:
        return to_hex(to_rgba(color_name))
    except ValueError:
        return "#FFFFFF"

def split_existing_intervals(new_entry):
    global colormap_data
    new_min, new_max, new_color = new_entry["min"], new_entry["max"], new_entry["color"]
    updated_data = []

    for entry in colormap_data:
        entry_min, entry_max, entry_color = entry["min"], entry["max"], entry["color"]

        if entry_max <= new_min or entry_min >= new_max:
            updated_data.append(entry)
        elif entry_min < new_min < entry_max:
            updated_data.append({"color": entry_color, "min": entry_min, "max": new_min})
        if entry_min < new_max < entry_max:
            updated_data.append({"color": entry_color, "min": new_max, "max": entry_max})

    updated_data.append(new_entry)
    return updated_data

def ensure_white_intervals():
    global colormap_data
    colormap_data.sort(key=lambda x: x["min"])
    filled_data = []

    for i in range(len(colormap_data) - 1):
        filled_data.append(colormap_data[i])
        if colormap_data[i]["max"] < colormap_data[i + 1]["min"]:
            filled_data.append({"color": "white", "min": colormap_data[i]["max"], "max": colormap_data[i + 1]["min"]})

    filled_data.append(colormap_data[-1])
    colormap_data = filled_data

def generate_colormap():
    fig = go.Figure()
    transitions = sorted(set([entry["min"] for entry in colormap_data] + [entry["max"] for entry in colormap_data]))

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
            tickvals=transitions,
            ticktext=[str(val) for val in transitions],
            tickangle=0,  # Make tick labels straight
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(visible=False),
        height=250,  # Increase height for more visibility
        margin=dict(l=20, r=20, t=20, b=50),  # Adjust margins for readability
    )
    return fig

def format_colormap_info():
    return [{"color": color_to_hex(entry["color"]), "range": [entry["min"], entry["max"]]} for entry in colormap_data]

def save_colormap_to_file():
    with open("colormap.json", "w") as f:
        json.dump(colormap_data, f)

def load_colormap_from_file(contents):
    global colormap_data
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    colormap_data = json.loads(decoded.decode('utf-8'))
    ensure_white_intervals()

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
            Input("upload-colormap", "contents"),
        ],
        [
            State("color-dropdown", "value"),
            State("min-range", "value"),
            State("max-range", "value"),
        ],
    )
    def update_colormap(n_clicks_add, n_clicks_save, uploaded_contents, color, min_range, max_range):
        global colormap_data
        save_status = ""

        if ctx.triggered_id == "add-color-btn" and color and min_range is not None and max_range is not None:
            new_entry = {"color": color, "min": min_range, "max": max_range}
            colormap_data = split_existing_intervals(new_entry)
            ensure_white_intervals()

        if ctx.triggered_id == "save-colormap-btn":
            save_colormap_to_file()
            save_status = "Colormap sauvegardée"

        if ctx.triggered_id == "upload-colormap" and uploaded_contents:
            load_colormap_from_file(uploaded_contents)

        colormap_figure = generate_colormap()
        colormap_info = [
            f"Color: {entry['color']}, Range: [{entry['min']}, {entry['max']}]"
            for entry in colormap_data
        ]

        return (
            colormap_figure,
            [html.Div(info) for info in colormap_info],
            save_status if save_status else no_update,
        )
