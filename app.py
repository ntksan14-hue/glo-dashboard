import dash
from dash import html, dcc

from data import df, df_clean
from config import SO_COLORS, SO_LABELS, MOD_COLORS, DONUT_COLOR_MAP

from callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Div(id="tab-content"),
    dcc.Tabs(id="navigation-tabs", value="tab-1", children=[
        dcc.Tab(label="Tab 1", value="tab-1"),
        dcc.Tab(label="Tab 2", value="tab-2"),
        dcc.Tab(label="Tab 3", value="tab-3"),
        dcc.Tab(label="Tab 4", value="tab-4"),
    ])
])

register_callbacks(app, df, df_clean)

server = app.server   # 🔥 สำคัญสำหรับ Render

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)