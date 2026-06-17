from dash import Input, Output, html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go


SO_GROUPS = {
    1: ['sp', 'sm', 'cm'],
    2: ['csr', 'cg'],
    3: ['dt', 'hr', 'km', 'im']
}


def register_tab2(app, df, df_clean):

    @app.callback(
        [
            Output({'type': 'tab2-graph', 'index': i}, 'figure') for i in [1,2,3]
        ] +
        [
            Output({'type': 'tab2-table', 'index': i}, 'data') for i in [1,2,3]
        ],
        [
            Input('tab2-year-selector', 'value'),
            Input('tab2-budget-selector-so1', 'value'),
            Input('tab2-budget-selector-so2', 'value'),
            Input('tab2-budget-selector-so3', 'value'),
        ]
    )
    def update_tab2(year, b1, b2, b3):

        budget_map = {1:b1, 2:b2, 3:b3}

        graphs = []
        tables = []

        for so in [1,2,3]:

            dff = df_clean[
                (df_clean["year"] == year) &
                (df_clean["so_goal"] == so) &
                (df_clean["sp"] == 0)
            ]

            if dff.empty:
                graphs.append(go.Figure())
                tables.append([])
                continue

            val = "total_budget"
            if budget_map[so] == "cost":
                val = "budget(cost)"
            elif budget_map[so] == "inv":
                val = "budget(inv)"

            g = dff.groupby("mod")[val].sum().reset_index()

            fig = px.bar(g, x="mod", y=val, text=val)

            graphs.append(fig)

            tables.append(
                dff.sort_values(val, ascending=False)
                .head(10)
                .to_dict("records")
            )

        return graphs + tables