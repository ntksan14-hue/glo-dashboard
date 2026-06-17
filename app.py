from dash import Dash
from callbacks.register import register_callbacks

app = Dash(__name__)
server = app.server

df = ...
df_clean = df[df["sp"] == 0]

register_callbacks(app, df, df_clean)

if __name__ == "__main__":
    app.run_server(debug=True)