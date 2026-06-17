from dash import Input, Output, html, dcc, dash_table
import plotly.graph_objects as go
import plotly.express as px


# =====================================================
# MAIN REGISTER FUNCTION
# =====================================================
def register_callbacks(app, df):

    # clean once (สำคัญมาก กัน Render ช้า + bug)
    df_clean = df[df["sp"] == 0].copy()


    # =====================================================
    # TAB SWITCH RENDER
    # =====================================================
    @app.callback(
        Output("tab-content", "children"),
        Input("navigation-tabs", "value")
    )
    def render_tab(tab):

        if tab == "tab-1":
            return build_tab1(df_clean)

        elif tab == "tab-2":
            return build_tab2()

        elif tab == "tab-3":
            return build_tab3()

        elif tab == "tab-4":
            return build_tab4(df)

        return html.Div("No Tab Found")


# =====================================================
# TAB 1
# =====================================================
def build_tab1(df_clean):

    df_3yr = df_clean[df_clean["year"].isin([2567, 2568, 2569])]

    total_budget = df_3yr["total_budget"].sum()
    total_cost = df_3yr["budget(cost)"].sum()
    total_inv = df_3yr["budget(inv)"].sum()

    fig = go.Figure()

    return html.Div([
        html.H3("Tab 1 Dashboard"),
        dcc.Graph(figure=fig)
    ])


# =====================================================
# TAB 2 (layout only, graphs handled by callback below)
# =====================================================
def build_tab2():

    return html.Div([
        html.H3("SO Deep Dive"),

        dcc.RadioItems(
            id="tab2-year-selector",
            options=[{"label": y, "value": y} for y in [2567, 2568, 2569]],
            value=2569,
            inline=True
        ),

        html.Hr(),

        *[
            html.Div([
                html.H4(f"SO{i}"),
                dcc.RadioItems(
                    id=f"tab2-budget-selector-so{i}",
                    options=[
                        {"label": "Cost", "value": "cost"},
                        {"label": "Inv", "value": "inv"},
                        {"label": "All", "value": "total"},
                    ],
                    value="total",
                    inline=True
                ),
                dcc.Graph(id={"type": "tab2-graph", "index": i}),
                dash_table.DataTable(
                    id={"type": "tab2-table", "index": i},
                    page_size=8
                )
            ]) for i in [1, 2, 3]
        ]
    ])


# =====================================================
# TAB 3
# =====================================================
def build_tab3():

    return html.Div([
        html.H3("Sankey + Module Ranking"),

        dcc.RadioItems(
            id="tab3-year-filter",
            options=[
                {"label": "ALL", "value": "ALL"},
                {"label": "2567", "value": 2567},
                {"label": "2568", "value": 2568},
                {"label": "2569", "value": 2569},
            ],
            value="ALL",
            inline=True
        ),

        dcc.Graph(id="tab3-sankey"),
        dcc.Graph(id="tab3-top-module")
    ])


# =====================================================
# TAB 4
# =====================================================
def build_tab4(df):

    return html.Div([
        html.H3("Drilldown Table"),

        html.Div([
            dcc.Dropdown(
                id="filter-year",
                options=[{"label": y, "value": y} for y in sorted(df["year"].unique())],
                multi=True
            ),

            dcc.Dropdown(
                id="filter-mod",
                options=[{"label": m, "value": m} for m in sorted(df["mod"].unique())],
                multi=True
            ),

            dcc.Dropdown(
                id="filter-so",
                options=[{"label": s, "value": s} for s in sorted(df["so_goal"].unique())],
                multi=True
            ),

            dcc.Input(id="search-name", type="text")
        ]),

        dash_table.DataTable(
            id="drilldown-table",
            page_size=10
        )
    ])


# =====================================================
# TAB 4 FILTER CALLBACK
# =====================================================
@app.callback(
    Output("drilldown-table", "data"),
    [
        Input("filter-year", "value"),
        Input("filter-mod", "value"),
        Input("filter-so", "value"),
        Input("search-name", "value")
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


# =====================================================
# TAB 2 COMBINED CALLBACK (NO INDENT BUG VERSION)
# =====================================================
@app.callback(
    Output({"type": "tab2-graph", "index": 1}, "figure"),
    Output({"type": "tab2-graph", "index": 2}, "figure"),
    Output({"type": "tab2-graph", "index": 3}, "figure"),
    Output({"type": "tab2-table", "index": 1}, "data"),
    Output({"type": "tab2-table", "index": 2}, "data"),
    Output({"type": "tab2-table", "index": 3}, "data"),
    Input("tab2-year-selector", "value"),
    Input("tab2-budget-selector-so1", "value"),
    Input("tab2-budget-selector-so2", "value"),
    Input("tab2-budget-selector-so3", "value"),
)
def update_tab2(year, b1, b2, b3):

    SO_MAP = {
        1: b1,
        2: b2,
        3: b3
    }

    figs = []
    tables = []

    for so in [1, 2, 3]:

        fig = go.Figure()
        figs.append(fig)

        tables.append([])

    return figs[0], figs[1], figs[2], tables[0], tables[1], tables[2]


# =====================================================
# TAB 3 CALLBACKS
# =====================================================
@app.callback(
    Output("tab3-sankey", "figure"),
    Input("tab3-year-filter", "value")
)
def update_sankey(year):
    fig = go.Figure()
    return fig


@app.callback(
    Output("tab3-top-module", "figure"),
    Input("tab3-year-filter", "value")
)
def update_top_module(year):
    fig = go.Figure()
    return fig