from dash import Dash
from layout import create_layout
from callbacks import register_callbacks

# Initialize Dash app
app = Dash(__name__)
app.title = "Interactive Colormap Builder"

# Define the layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
