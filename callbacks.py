from dash import Input, Output, html, dcc, dash_table
import plotly.graph_objects as go
import plotly.express as px


# =====================================================
# MAIN REGISTRATION
# =====================================================
def register_callbacks(app, df, df_clean):

    # =================================================
    # TAB SWITCH ROUTER
    # =================================================
    @app.callback(
        Output("tab-content", "children"),
        Input("navigation-tabs", "value")
    )
    def render_tab_content(tab):

        df_clean_local = df[df["sp"] == 0]
        df_3yr = df_clean_local[df_clean_local["year"].isin([2567, 2568, 2569])]

        # =========================
        # TAB 1
        # =========================
        if tab == "tab-1":

            total_budget_3yr = df_3yr["total_budget"].sum()
            total_cost = df_3yr["budget(cost)"].sum()
            total_inv = df_3yr["budget(inv)"].sum()
            so_sums = df_3yr.groupby("so_goal")["total_budget"].sum()

            yearly_summary = df_clean_local.groupby("year").agg({
                'budget(cost)': 'sum',
                'budget(inv)': 'sum',
                'total_budget': 'sum'
            }).reset_index()

            fig_trend = go.Figure()
            df_past = yearly_summary[yearly_summary['year'] <= 2569]

            fig_trend.add_trace(go.Bar(
                x=df_past['year'],
                y=df_past['budget(cost)'],
                name='งบทำการ'
            ))

            fig_trend.add_trace(go.Bar(
                x=df_past['year'],
                y=df_past['budget(inv)'],
                name='งบลงทุน'
            ))

            fig_trend.update_layout(
                barmode='stack',
                template='plotly_white'
            )

            fig_so_year = px.bar(
                df_3yr.groupby(['year', 'so_goal'])['total_budget'].sum().reset_index(),
                x='year',
                y='total_budget',
                color='so_goal',
                barmode='stack'
            )

            return html.Div([
                html.H3("TAB 1")
            ])


        # =========================
        # TAB 2 (PLACEHOLDER SAFE)
        # =========================
        if tab == "tab-2":
            return html.Div([
                html.H3("TAB 2 READY")
            ])

        # =========================
        # TAB 3
        # =========================
        if tab == "tab-3":
            df_s = df[df["sp"] == 0].copy()
            df_s["year"] = df_s["year"].astype(str)

            df_m = df_s.melt(
                id_vars=["year", "mod"],
                value_vars=["budget(cost)", "budget(inv)"],
                var_name="budget_type",
                value_name="value"
            )

            df_m["budget_type"] = df_m["budget_type"].map({
                "budget(cost)": "งบทำการ",
                "budget(inv)": "งบลงทุน"
            })

            flow = df_m.groupby(["budget_type", "mod"], as_index=False)["value"].sum()

            labels = ["งบทำการ", "งบลงทุน"] + sorted(flow["mod"].unique())
            idx = {k: i for i, k in enumerate(labels)}

            fig = go.Figure(data=[go.Sankey(
                node=dict(label=labels),
                link=dict(
                    source=flow["budget_type"].map(idx),
                    target=flow["mod"].map(idx),
                    value=flow["value"]
                )
            )])

            return html.Div([
                dcc.Graph(figure=fig)
            ])


        # =========================
        # TAB 4 (SAFE MINIMAL)
        # =========================
        if tab == "tab-4":
            return html.Div([
                html.H3("DRILLDOWN READY"),
                dash_table.DataTable(
                    data=df.to_dict("records"),
                    page_size=10
                )
            ])


    # =====================================================
    # TAB 4 FILTER CALLBACK
    # =====================================================
    @app.callback(
        Output('drilldown-table', 'data'),
        Input('filter-year', 'value'),
        Input('filter-mod', 'value'),
        Input('filter-so', 'value'),
        Input('search-name', 'value')
    )
    def filter_table(years, mods, sos, search_term):

        dff = df.copy()

        if years:
            dff = dff[dff['year'].isin(years)]
        if mods:
            dff = dff[dff['mod'].isin(mods)]
        if sos:
            dff = dff[dff['so_goal'].isin(sos)]
        if search_term:
            dff = dff[dff['ap_name_cleaned'].str.contains(search_term, case=False, na=False)]

        return dff.to_dict('records')


    # =====================================================
    # SAFE TAB2 CALLBACK (NO CRASH VERSION)
    # =====================================================
    @app.callback(
        Output({'type': 'tab2-graph', 'index': 1}, 'figure'),
        Output({'type': 'tab2-graph', 'index': 2}, 'figure'),
        Output({'type': 'tab2-graph', 'index': 3}, 'figure'),
        Output({'type': 'tab2-table', 'index': 1}, 'data'),
        Output({'type': 'tab2-table', 'index': 2}, 'data'),
        Output({'type': 'tab2-table', 'index': 3}, 'data'),
        Input('tab2-year-selector', 'value')
    )
    def update_tab2(selected_year):

        figs = []
        tables = []

        for so in [1, 2, 3]:

            dff = df_clean[
                (df_clean['year'] == selected_year) &
                (df_clean['so_goal'] == so) &
                (df_clean['sp'] == 0)
            ]

            if dff.empty:
                figs.append(go.Figure())
                tables.append([])
                continue

            g = dff.groupby("mod")["total_budget"].sum().reset_index()

            fig = px.bar(g, x="mod", y="total_budget")

            figs.append(fig)

            tables.append(
                dff.head(10)[["ap_name_cleaned", "mod", "total_budget"]].to_dict("records")
            )

        return figs[0], figs[1], figs[2], tables[0], tables[1], tables[2]


    # =====================================================
    # DONUT CHART SAFE
    # =====================================================
    @app.callback(
        Output('dynamic-donut-chart', 'figure'),
        Output('dynamic-donut-cost-chart', 'figure'),
        Input('donut-year-selector', 'value')
    )
    def update_donuts(selected_year):

        dff = df[df["sp"] == 0]

        if selected_year != "ALL":
            dff = dff[dff["year"] == selected_year]

        inv = dff.groupby("mod")["budget(inv)"].sum().reset_index()
        cost = dff.groupby("mod")["budget(cost)"].sum().reset_index()

        fig1 = px.pie(inv, names="mod", values="budget(inv)", hole=0.5)
        fig2 = px.pie(cost, names="mod", values="budget(cost)", hole=0.5)

        return fig1, fig2