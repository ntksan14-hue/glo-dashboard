from dash import Input, Output, dcc
import plotly.graph_objects as go
import plotly.express as px


def register_tab3(app, df, df_clean):

    @app.callback(
        Output("tab3-sankey", "figure"),
        Input("tab3-year-filter", "value")
    )
    def sankey(year):

        dff = df_clean.copy()

        if year != "ALL":
            dff = dff[dff["year"] == year]

        flow = dff.groupby(["budget(cost)", "mod"])["total_budget"].sum().reset_index()

        return go.Figure()