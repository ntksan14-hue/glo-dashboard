from dash import Input, Output


def register_tab4(app, df, df_clean):

    @app.callback(
        Output("drilldown-table", "data"),
        [
            Input("filter-year", "value"),
            Input("filter-mod", "value"),
            Input("filter-so", "value"),
            Input("search-name", "value"),
        ]
    )
    def filter_table(years, mods, sos, search):

        dff = df.copy()

        if years:
            dff = dff[dff["year"].isin(years)]
        if mods:
            dff = dff[dff["mod"].isin(mods)]
        if sos:
            dff = dff[dff["so_goal"].isin(sos)]
        if search:
            dff = dff[dff["ap_name_cleaned"].str.contains(search, case=False, na=False)]

        return dff.to_dict("records")