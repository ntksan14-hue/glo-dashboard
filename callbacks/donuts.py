from dash import Input, Output
import plotly.express as px


def register_donuts(app, df, df_clean):

    @app.callback(
        Output("dynamic-donut-chart", "figure"),
        Input("donut-year-selector", "value")
    )
    def donut_inv(year):

        dff = df_clean[df_clean["budget(inv)"] > 0]

        if year != "ALL":
            dff = dff[dff["year"] == year]

        g = dff.groupby("mod")["budget(inv)"].sum().reset_index()

        return px.pie(g, values="budget(inv)", names="mod")


    @app.callback(
        Output("dynamic-donut-cost-chart", "figure"),
        Input("donut-year-selector", "value")
    )
    def donut_cost(year):

        dff = df_clean[df_clean["budget(cost)"] > 0]

        if year != "ALL":
            dff = dff[dff["year"] == year]

        g = dff.groupby("mod")["budget(cost)"].sum().reset_index()

        return px.pie(g, values="budget(cost)", names="mod")