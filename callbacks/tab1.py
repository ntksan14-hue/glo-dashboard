from dash import Input, Output, html, dcc
import plotly.graph_objects as go
import plotly.express as px


def register_tab1(app, df, df_clean):

    @app.callback(
        Output("tab-content", "children"),
        Input("navigation-tabs", "value")
    )
    def render_tab1(tab):

        if tab != "tab-1":
            return None

        df_3yr = df_clean[df_clean["year"].isin([2567, 2568, 2569])]

        total_budget = df_3yr["total_budget"].sum()
        total_cost = df_3yr["budget(cost)"].sum()
        total_inv = df_3yr["budget(inv)"].sum()

        fig = go.Figure()

        yearly = df_clean.groupby("year")[["budget(cost)", "budget(inv)"]].sum().reset_index()

        fig.add_bar(x=yearly["year"], y=yearly["budget(cost)"], name="Cost")
        fig.add_bar(x=yearly["year"], y=yearly["budget(inv)"], name="Inv")

        fig.update_layout(barmode="stack", template="plotly_white")

        return html.Div([
            html.H3("Tab 1 Dashboard"),
            dcc.Graph(figure=fig),
            html.H4(f"Total: {total_budget:,.0f}")
        ])