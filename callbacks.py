from dash import Input, Output
import plotly.graph_objects as go
import plotly.express as px

def register_callbacks(app, df, df_clean):

    @app.callback(
        Output("tab-content", "children"),
        Input("navigation-tabs", "value")
    )

@app.callback(
        Output("tab-content", "children"),
        Input("navigation-tabs", "value")
    )
    def render_tab_content(tab):
        df_clean = df[df["sp"] == 0]
        df_3yr = df_clean[df_clean["year"].isin([2567, 2568, 2569])]
        
        if tab == "tab-1":
            total_budget_3yr = df_3yr["total_budget"].sum()
            total_cost = df_3yr["budget(cost)"].sum()
            total_inv = df_3yr["budget(inv)"].sum()
            so_sums = df_3yr.groupby("so_goal")["total_budget"].sum()
            
            # 1.1 Yearly Budget Trend
            yearly_summary = df_clean.groupby("year").agg({'budget(cost)': 'sum', 'budget(inv)': 'sum', 'total_budget': 'sum'}).reset_index()
            fig_trend = go.Figure()
            df_past = yearly_summary[yearly_summary['year'] <= 2569]
            fig_trend.add_trace(go.Bar(x=df_past['year'], y=df_past['budget(cost)'], name='งบทำการ', marker_color='#aec7e8'))
            fig_trend.add_trace(go.Bar(x=df_past['year'], y=df_past['budget(inv)'], name='งบลงทุน', marker_color='#1f77b4'))
            
            df_70 = yearly_summary[yearly_summary['year'] == 2570]
            fig_trend.add_trace(go.Bar(
                x=df_70['year'], y=df_70['total_budget'], 
                name='ปี 2570 Approved (Target)', 
                marker_color='rgba(26, 54, 93, 0.4)',
                marker_line=dict(color='#1a365d', width=2),
                marker_pattern_shape="/"
            ))
            fig_trend.update_layout(
                title="<b>Yearly budget proportions (2567-2569)</b>",
                barmode='stack', template='plotly_white', legend=dict(orientation="h", y=1.1)
            )
            
            # 1.2 SO Distribution by Year
            so_year = df_clean.groupby(['year', 'so_goal'])['total_budget'].sum().reset_index()
            so_year['Strategic Goal'] = so_year['so_goal'].map(SO_LABELS)
            COLOR_MAP_LABEL = {SO_LABELS[k]: v for k, v in SO_COLORS.items()}
            
            fig_so_year = px.bar(
                so_year, x='year', y='total_budget', color='Strategic Goal',
                color_discrete_map=COLOR_MAP_LABEL, title="<b>Strategic Objectives by Year</b>",
                labels={'total_budget': 'งบประมาณรวม (ล้านบาท)', 'Strategic Goal': 'SO'}
            )
            fig_so_year.update_layout(barmode='stack', template='plotly_white')
            
            return html.Div([
                # KPI Cards Row
                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}, children=[
                    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'width': '30%', 'textAlign': 'center'}, children=[
                        html.H5("Total Clean Budget (3 ปี)", style={'color': '#666', 'margin': '0'}),
                        html.H2(f"{total_budget_3yr:,.1f} ลบ.", style={'color': '#1a365d', 'margin': '10px 0 0 0'}),
                        html.P("กรองตัวเลขซ้ำซ้อนเรียบร้อย (sp=0)", style={'fontSize': '11px', 'color': 'green', 'margin': '0'})
                    ]),
                    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'width': '30%', 'textAlign': 'center'}, children=[
                        html.H5("Budget Mix (Cost vs Inv)", style={'color': '#666', 'margin': '0'}),
                        html.H2(f"{total_cost/total_budget_3yr*100:.1f}% / {total_inv/total_budget_3yr*100:.1f}%", style={'color': '#1a365d', 'margin': '10px 0 0 0'}),
                        html.P(f"Cost: {total_cost:.1f}M | Inv: {total_inv:.1f}M", style={'fontSize': '12px', 'margin': '0', 'color': '#666'})
                    ]),
                    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'width': '30%', 'textAlign': 'center'}, children=[
                        html.H5("Strategic Share (SO1 / SO2 / SO3)", style={'color': '#666', 'margin': '0'}),
                        html.H2(style={'color': '#1a365d', 'margin': '10px 0 0 0'}, children=[
                            html.Span(f"{so_sums.get(1,0)/total_budget_3yr*100:.0f}%", style={'color': '#D35400'}), " / ",
                            html.Span(f"{so_sums.get(2,0)/total_budget_3yr*100:.0f}%", style={'color': '#9B51E0'}), " / ",
                            html.Span(f"{so_sums.get(3,0)/total_budget_3yr*100:.0f}%", style={'color': '#F4D03F'}),
                        ]),
                        html.P("High-Contrast Color Mode ปรับปรุงใหม่", style={'fontSize': '11px', 'color': '#666', 'margin': '0'})
                    ]),
                ]),
                
                # Upper Visualizations Grid
                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}, children=[
                    html.Div([dcc.Graph(figure=fig_trend)], style={'width': '48%', 'backgroundColor': 'white', 'padding': '10px', 'borderRadius': '8px'}),
                    html.Div([dcc.Graph(figure=fig_so_year)], style={'width': '48%', 'backgroundColor': 'white', 'padding': '10px', 'borderRadius': '8px'})
                ]),
                
                # Lower Section: Donut Charts คู่ขนาน
                html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, children=[
                    html.Div(style={'marginBottom': '20px', 'padding': '10px', 'backgroundColor': '#f8fafc', 'borderRadius': '6px'}, children=[
                        html.Label("📅 เลือกตัวเลือกปีงบประมาณเพื่อสืบค้นงบประมาณแผนปฏิบัติการทั้งหมด:", style={'fontWeight': 'bold', 'marginRight': '15px'}),
                        dcc.RadioItems(
                            id='donut-year-selector',
                            options=[
                                {'label': ' ภาพรวมทั้งหมด (2567-2569) ', 'value': 'ALL'},
                                {'label': ' ปี 2567 ', 'value': 2567},
                                {'label': ' ปี 2568 ', 'value': 2568},
                                {'label': ' ปี 2569 ', 'value': 2569}
                            ],
                            value='ALL',
                            labelStyle={'display': 'inline-block', 'marginRight': '20px', 'cursor': 'pointer'}
                        )
                    ]),
                    
                    html.Div(style={'display': 'flex', 'justifyContent': 'space-between'}, children=[
                        html.Div([
                            html.H3("⚙️ โครงสร้างสัดส่วนงบลงทุน (Investment)", style={'color': '#1a365d', 'fontSize': '16px', 'textAlign': 'center', 'margin': '0'}),
                            dcc.Graph(id='dynamic-donut-chart')
                        ], style={'width': '49%'}),
                        
                        html.Div([
                            html.H3("💼 โครงสร้างสัดส่วนงบทำการ (Operating Cost)", style={'color': '#1a365d', 'fontSize': '16px', 'textAlign': 'center', 'margin': '0'}),
                            dcc.Graph(id='dynamic-donut-cost-chart')
                        ], style={'width': '49%'})
                    ])
                ])
            ])
    
        elif tab == "tab-2":
    
            return html.Div([
                html.H3("🎯 Strategic Objective Deep-Dive (SO1 / SO2 / SO3)",
                        style={'color': '#1a365d', 'marginBottom': '20px'}),
        
                # =========================
                # 🔥 GLOBAL FILTER (YEAR)
                # =========================
                html.Div([
                    html.Label("📍 ปีงบประมาณ (Global Filter)",
                                style={'fontWeight': 'bold'}),
        
                    dcc.RadioItems(
                        id='tab2-year-selector',
                        options=[{'label': y, 'value': y} for y in [2567, 2568, 2569]],
                        value=2569,
                        inline=True
                    )
                ], style={
                    'backgroundColor': '#f8f9fa',
                    'padding': '10px',
                    'borderRadius': '8px',
                    'marginBottom': '20px'
                }),
        
                # =========================
                # 🟠 SO1
                # =========================
                html.Div([
                    html.H4("🟠 SO1: Growth & Product Expansion"),
        
                    html.Label("📊 ประเภทงบ SO1"),
        
                    dcc.RadioItems(
                        id='tab2-budget-selector-so1',
                        options=[
                            {'label': 'งบทำการ', 'value': 'cost'},
                            {'label': 'งบลงทุน', 'value': 'inv'},
                            {'label': 'ทั้งหมด', 'value': 'total'}
                        ],
                        value='total',
                        inline=True
                    ),
        
                    html.Div([
                        dcc.Graph(id={'type': 'tab2-graph', 'index': 1}),
                        html.H5("📋 รายชื่อแผนงาน SO1"),
                        dash_table.DataTable(
                            id={'type': 'tab2-table', 'index': 1},
                            page_size=8
                        )
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '10px',
                        'borderRadius': '8px'
                    })
                ]),
        
                html.Hr(),
        
                # =========================
                # 🟣 SO2
                # =========================
                html.Div([
                    html.H4("🟣 SO2: ESG & Public Trust"),
        
                    html.Label("📊 ประเภทงบ SO2"),
        
                    dcc.RadioItems(
                        id='tab2-budget-selector-so2',
                        options=[
                            {'label': 'งบทำการ', 'value': 'cost'},
                            {'label': 'งบลงทุน', 'value': 'inv'},
                            {'label': 'ทั้งหมด', 'value': 'total'}
                        ],
                        value='total',
                        inline=True
                    ),
        
                    html.Div([
                        dcc.Graph(id={'type': 'tab2-graph', 'index': 2}),
                        html.H5("📋 รายชื่อแผนงาน SO2"),
                        dash_table.DataTable(
                            id={'type': 'tab2-table', 'index': 2},
                            page_size=8
                        )
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '10px',
                        'borderRadius': '8px'
                    })
                ]),
        
                html.Hr(),
        
                # =========================
                # 🟢 SO3
                # =========================
                html.Div([
                    html.H4("🟢 SO3: Digital & Capability"),
        
                    html.Label("📊 ประเภทงบ SO3"),
        
                    dcc.RadioItems(
                        id='tab2-budget-selector-so3',
                        options=[
                            {'label': 'งบทำการ', 'value': 'cost'},
                            {'label': 'งบลงทุน', 'value': 'inv'},
                            {'label': 'ทั้งหมด', 'value': 'total'}
                        ],
                        value='total',
                        inline=True
                    ),
        
                    html.Div([
                        dcc.Graph(id={'type': 'tab2-graph', 'index': 3}),
                        html.H5("📋 รายชื่อแผนงาน SO3"),
                        dash_table.DataTable(
                            id={'type': 'tab2-table', 'index': 3},
                            page_size=8
                        )
                    ], style={
                        'backgroundColor': 'white',
                        'padding': '10px',
                        'borderRadius': '8px'
                    })
                ])
            ])
    
        elif tab == "tab-3":
    
            df_s = df[df["sp"] == 0].copy()
            df_s["year"] = df_s["year"].astype(str)
        
            # =========================
            # SANKEY DATA (UNCHANGED LOGIC)
            # =========================
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
        
            year_budget = df_m.groupby(["year", "budget_type"])["value"].sum().reset_index()
            budget_mod = df_m.groupby(["budget_type", "mod"])["value"].sum().reset_index()
        
            years = df_m["year"].unique().tolist()
            budgets = ["งบทำการ", "งบลงทุน"]
            mods = df_m["mod"].unique().tolist()
        
            labels = years + budgets + mods
        
            def idx(x):
                return labels.index(x)
        
            source, target, value = [], [], []
        
            for _, r in year_budget.iterrows():
                source.append(idx(r["year"]))
                target.append(idx(r["budget_type"]))
                value.append(r["value"])
        
            for _, r in budget_mod.iterrows():
                source.append(idx(r["budget_type"]))
                target.append(idx(r["mod"]))
                value.append(r["value"])
        
            fig_sankey = go.Figure(data=[go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=15,
                    thickness=18,
                    line=dict(color="black", width=0.3),
                    label=labels
                ),
                link=dict(source=source, target=target, value=value)
            )])
        
            fig_sankey.update_layout(
                title="<b>Sankey: Year → Budget Type → Module</b>",
                template="plotly_white",
                font_size=12
            )
        
            # =========================
            # 🔥 NEW: YEAR FILTER (TOP MODULE)
            # =========================
            year_options = sorted(df_s["year"].unique().tolist())
        
            year_radio = dcc.RadioItems(
                id="tab3-year-filter",
                options=[{"label": y, "value": y} for y in year_options] +
                        [{"label": "ทั้งหมด", "value": "ALL"}],
                value="ALL",
                inline=True
            )
        
            # default filter
            dff_top = df_s.copy()
    
            top_mod = (
                dff_top.groupby("mod", as_index=False)["total_budget"]
                .sum()
                .sort_values("total_budget", ascending=True)
                .tail(10)
            )
            
            fig_top = px.bar(
                top_mod,
                x="total_budget",
                y="mod",
                orientation="h",
                text="total_budget",
                title="Top Modules (ALL YEARS)"
            )
            
            # =========================
            # FIX TEXT CUT + READABILITY
            # =========================
            fig_top.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="auto",
                textfont=dict(size=12)
            )
            
            # =========================
            # FIX LAYOUT (IMPORTANT)
            # =========================
            max_val = top_mod["total_budget"].max()
            
            fig_top.update_layout(
                template="plotly_white",
                height=500,
                margin=dict(l=120, r=80, t=60, b=30),
                xaxis=dict(range=[0, max_val * 1.15])
            )
        
            return html.Div([
                dcc.Graph(id="tab3-sankey", style={'height': '800px'}),
        
                html.Hr(),
        
                html.Div([
                    html.H5("📊 Top Modules by Year"),
                    html.Div([
                        html.Label("เลือกปีงบประมาณ:"),
                        year_radio
                    ], style={'marginBottom': '10px'}),
        
                    dcc.Graph(id="tab3-top-module")
                ], style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '8px'})
            ])
    
        elif tab == "tab-4":
            return html.Div([
                html.H3("🔍 ระบบเจาะลึกสืบค้นข้อมูลแผนงานระดับปฏิบัติการ (Dynamic Table)", style={'color': '#1a365d'}),
                
                html.Div(style={'display': 'flex', 'gap': '20px', 'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'marginBottom': '20px'}, children=[
                    html.Div(style={'width': '25%'}, children=[
                        html.Label("กรองปีงบประมาณ (year)", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(id='filter-year', options=[{'label': str(y), 'value': y} for y in sorted(df['year'].unique())], multi=True, placeholder="เลือกปีทั้งหมด")
                    ]),
                    html.Div(style={'width': '25%'}, children=[
                        html.Label("กรองตามเล่มแผน (mod)", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(id='filter-mod', options=[{'label': m, 'value': m} for m in sorted(df['mod'].unique())], multi=True, placeholder="เล่มแผนทั้งหมด")
                    ]),
                    html.Div(style={'width': '25%'}, children=[
                        html.Label("กรองเป้าหมายยุทธศาสตร์ (so_goal)", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(id='filter-so', options=[{'label': f"SO {s}", 'value': s} for s in sorted(df['so_goal'].unique())], multi=True, placeholder="ยุทธศาสตร์ทั้งหมด")
                    ]),
                    html.Div(style={'width': '25%'}, children=[
                        html.Label("กล่องค้นหาแบบพิมพ์ทันที (Search Box)", style={'fontWeight': 'bold'}),
                        dcc.Input(id='search-name', type='text', placeholder='พิมพ์ระบุเช่น ERP, สลาก, GLO...', style={'width': '100%', 'padding': '7px', 'borderRadius': '4px', 'border': '1px solid #ccc'})
                    ]),
                ]),
                
                html.Div(style={'textAlign': 'right', 'marginBottom': '10px'}, children=[
                    html.Button("📥 Export to Excel (Native UI Active)", id="btn-export", style={'backgroundColor': '#2196F3', 'color': 'white', 'border': 'none', 'padding': '8px 15px', 'borderRadius': '4px', 'fontWeight':'bold'}),
                ]),
                
                html.Div(style={'backgroundColor': 'white', 'padding': '10px', 'borderRadius': '8px'}, children=[
                    dash_table.DataTable(
                        id='drilldown-table',
                        columns=[
                            {"name": "ปี (year)", "id": "year"},
                            {"name": "เล่มแผน (mod)", "id": "mod"},
                            {"name": "ลำดับ (#)", "id": "#"},
                            {"name": "รหัสแผน (ap_id)", "id": "ap_id"},
                            {"name": "ชื่อแผนงาน (ap_name_cleaned)", "id": "ap_name_cleaned"},
                            {"name": "งบดำเนินงาน (budget(cost))", "id": "budget(cost)"},
                            {"name": "งบลงทุน (budget(inv))", "id": "budget(inv)"},
                            {"name": "งบรวม (total_budget)", "id": "total_budget"},
                            {"name": "สถานะคุมซ้ำ (sp)", "id": "sp"},
                            {"name": "รหัส SO (so_goal)", "id": "so_goal"}
                        ],
                        data=df.to_dict('records'),
                        page_size=10,
                        sort_action="native",
                        filter_action="native",
                        style_header={'backgroundColor': '#1a365d', 'color': 'white', 'fontWeight': 'bold', 'textAlign': 'center'},
                        style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Sarabun'},
                        style_data_conditional=[
                            {'if': {'column_id': 'sp', 'filter_query': '{sp} eq 1'}, 'backgroundColor': '#ffebee', 'color': '#c62828'}
                        ]
                    )
                ])
            ])
    
    # ==========================================
    # 4. INDEPENDENT TOP-LEVEL CALLBACKS FOR DONUT CHARTS (TAB 1)
    # ==========================================
    @app.callback(
        Output('dynamic-donut-chart', 'figure'),
        Input('donut-year-selector', 'value')
    )
    def update_donut_chart(selected_year):
        if not selected_year:
            return go.Figure()
            
        dff = df[(df['sp'] == 0) & (df['budget(inv)'] > 0)].copy()
        
        if selected_year != 'ALL':
            dff = dff[dff['year'] == selected_year]
        else:
            dff = dff[dff['year'].isin([2567, 2568, 2569])]
            
        dff['Investment_Category'] = 'แผน ' + dff['mod'].str.strip().str.lower()
        chart_data = dff.groupby('Investment_Category')['budget(inv)'].sum().reset_index()
        chart_data = chart_data.sort_values(by='budget(inv)', ascending=False)
        
        pull_values = [0.05 if i == 0 else 0 for i in range(len(chart_data))]
        
        fig = px.pie(chart_data, values='budget(inv)', names='Investment_Category', hole=0.6, 
                     color='Investment_Category', color_discrete_map=DONUT_COLOR_MAP) # 🌟 ดึงสีจากพจนานุกรม Donut Global
        
        fig.update_traces(
            rotation=90, direction='clockwise', pull=pull_values, textposition='auto',
            texttemplate='%{percent:.1%}', hovertemplate="<b>%{label}</b><br>งบลงทุนสุทธิ: %{value:,.2f} ล้านบาท<br>สัดส่วน: %{percent}"
        )
        fig.update_layout(
            title=dict(text=f"<b>สัดส่วนงบลงทุนรายแผนงาน ({selected_year if selected_year != 'ALL' else 'รวม 67-69'})</b>", y=0.95, x=0.5, xanchor='center', font=dict(size=14)),
            margin=dict(t=60, b=20, l=20, r=20), showlegend=True, template='plotly_white',
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor='center')
        )
        return fig
    
    
    @app.callback(
        Output('dynamic-donut-cost-chart', 'figure'),
        Input('donut-year-selector', 'value')
    )
    def update_donut_cost_chart(selected_year):
        if not selected_year:
            return go.Figure()
    
        dff = df[(df['sp'] == 0) & (df['budget(cost)'] > 0)].copy()
        
        if selected_year != 'ALL':
            dff = dff[dff['year'] == selected_year]
        else:
            dff = dff[dff['year'].isin([2567, 2568, 2569])]
            
        dff['Cost_Category'] = 'แผน ' + dff['mod'].str.strip().str.lower()
        chart_data = dff.groupby('Cost_Category')['budget(cost)'].sum().reset_index()
        chart_data = chart_data.sort_values(by='budget(cost)', ascending=False)
        
        pull_values = [0.05 if i == 0 else 0 for i in range(len(chart_data))]
        
        fig = px.pie(chart_data, values='budget(cost)', names='Cost_Category', hole=0.6, 
                     color='Cost_Category', color_discrete_map=DONUT_COLOR_MAP) # 🌟 ดึงสีจากพจนานุกรม Donut Global
        
        fig.update_traces(
            rotation=90, direction='clockwise', pull=pull_values, textposition='auto',
            texttemplate='%{percent:.1%}', hovertemplate="<b>%{label}</b><br>งบดำเนินงานสุทธิ: %{value:,.2f} ล้านบาท<br>สัดส่วน: %{percent}"
        )
        fig.update_layout(
            title=dict(text=f"<b>สัดส่วนงบดำเนินงานรายแผนงาน ({selected_year if selected_year != 'ALL' else 'รวม 67-69'})</b>", y=0.95, x=0.5, xanchor='center', font=dict(size=14)),
            margin=dict(t=60, b=20, l=20, r=20), showlegend=True, template='plotly_white',
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor='center')
        )
        return fig
    
    
    # Callback สำหรับแท็บ 4 (Table Filter)
    @app.callback(
        Output('drilldown-table', 'data'),
        [Input('filter-year', 'value'),
         Input('filter-mod', 'value'),
         Input('filter-so', 'value'),
         Input('search-name', 'value')]
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
    
    
    @app.callback(
        [Output({'type': 'tab2-graph', 'index': i}, 'figure') for i in [1, 2, 3]] +
        [Output({'type': 'tab2-table', 'index': i}, 'data') for i in [1, 2, 3]],
        [
            Input('tab2-year-selector', 'value'),
            Input('tab2-budget-selector-so1', 'value'),
            Input('tab2-budget-selector-so2', 'value'),
            Input('tab2-budget-selector-so3', 'value'),
        ]
    )
    def update_tab2_all(selected_year, budget_so1, budget_so2, budget_so3):
    
        SO_GROUPS = {
            1: ['sp', 'sm', 'cm'],
            2: ['csr', 'cg'],
            3: ['dt', 'hr', 'km', 'im']
        }
    
        budget_map = {
            1: budget_so1,
            2: budget_so2,
            3: budget_so3
        }
    
        outputs_graph = []
        outputs_table = []
    
        for so in [1, 2, 3]:
    
            mods = SO_GROUPS[so]
            budget_type = budget_map[so]
    
            # =========================
            # FILTER
            # =========================
            dff = df_clean[
                (df_clean['year'] == selected_year) &
                (df_clean['so_goal'] == so) &
                (df_clean['sp'] == 0) &
                (df_clean['mod'].str.lower().isin(mods))
            ].copy()
    
            # =========================
            # EMPTY HANDLE
            # =========================
            if dff.empty:
                outputs_graph.append(go.Figure().update_layout(title=f"SO{so} - No Data"))
                outputs_table.append([])
                continue
    
            # =========================
            # SELECT VALUE COLUMN
            # =========================
            if budget_type == 'cost':
                val_col = 'budget(cost)'
            elif budget_type == 'inv':
                val_col = 'budget(inv)'
            else:
                dff['total'] = dff['budget(cost)'] + dff['budget(inv)']
                val_col = 'total'
    
            # =========================
            # GRAPH (FIXED → SINGLE BAR)
            # =========================
            g = dff.groupby('mod')[val_col].sum().reset_index()
    
            fig = px.bar(
                g,
                x='mod',
                y=val_col,
                text=val_col,
                color='mod',
                color_discrete_map=MOD_COLORS,
                title=f"SO{so} Budget ({budget_type}) - {selected_year}"
            )
    
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='inside')
    
            fig.update_layout(
                template='plotly_white',
                showlegend=False
            )
    
            outputs_graph.append(fig)
    
            # =========================
            # TABLE (FIXED → USE SAME FILTER + SORT BY SELECTED TYPE)
            # =========================
            dff['calc_val'] = dff[val_col]
    
            table = dff.sort_values('calc_val', ascending=False)[
                ['ap_name_cleaned', 'mod', 'budget(cost)', 'budget(inv)', 'total_budget']
            ].head(10).to_dict('records')
    
            outputs_table.append(table)
    
        return outputs_graph + outputs_table
    
    @app.callback(
        Output("tab3-sankey", "figure"),
        Input("tab3-year-filter", "value")
    )
    def update_tab3(year):
    
        df_s = df[df["sp"] == 0].copy()
    
        # =========================
        # FIX TYPE FIRST
        # =========================
        df_s["year"] = df_s["year"].astype(str)
    
        # =========================
        # FILTER YEAR
        # =========================
        if year != "ALL":
            df_s = df_s[df_s["year"] == str(year)]
    
        # =========================
        # MELT
        # =========================
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
    
        # =========================
        # AGGREGATE FLOW (ONLY Budget → Mod)
        # =========================
        flow = df_m.groupby(["budget_type", "mod"], as_index=False)["value"].sum()
    
        # =========================
        # BUILD NODES (SAFE UNIQUE)
        # =========================
        budgets = ["งบทำการ", "งบลงทุน"]
        mods = sorted(flow["mod"].unique())
    
        labels = budgets + mods
    
        idx = {k: i for i, k in enumerate(labels)}
    
        # =========================
        # LINKS
        # =========================
        source = flow["budget_type"].map(idx).tolist()
        target = flow["mod"].map(idx).tolist()
        value = flow["value"].tolist()
    
        total = sum(value) if len(value) > 0 else 0
    
        # hover % + บาท
        hover = [
            f"{b} → {m}<br>บาท: {v:,.0f}<br>%: {(v/total*100 if total else 0):.2f}%"
            for b, m, v in zip(flow["budget_type"], flow["mod"], flow["value"])
        ]
    
        # =========================
        # COLORS (simple)
        # =========================
        node_colors = ["#666666", "#999999"] + ["#4C78A8"] * len(mods)
    
        link_colors = ["rgba(76,120,168,0.5)"] * len(flow)
    
        # =========================
        # FIGURE
        # =========================
        fig = go.Figure(data=[go.Sankey(
            arrangement="snap",
            node=dict(
                pad=15,
                thickness=18,
                label=labels,
                color=node_colors
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color=link_colors,
                customdata=hover,
                hovertemplate="%{customdata}<extra></extra>"
            )
        )])
    
        fig.update_layout(
            title=f"Sankey: Budget → Module (Year: {year})",
            template="plotly_white",
            font_size=12
        )
    
        return fig
    
    
    @app.callback(
        Output("tab3-top-module", "figure"),
        Input("tab3-year-filter", "value")
    )
    def update_top_module(year):
    
        dff = df[df["sp"] == 0].copy()
    
        # =========================
        # FIX TYPE
        # =========================
        dff["year"] = dff["year"].astype(str)
    
        if year != "ALL":
            dff = dff[dff["year"] == str(year)]
    
        # =========================
        # FIX NULL / ZERO SAFETY
        # =========================
        dff["total_budget"] = (
            dff["budget(cost)"].fillna(0) +
            dff["budget(inv)"].fillna(0)
        )
    
        # =========================
        # GROUP
        # =========================
        top_mod = (
            dff.groupby("mod")["total_budget"]
            .sum()
            .reset_index()
        )
    
        # 🔥 กัน empty data
        if top_mod.empty or top_mod["total_budget"].sum() == 0:
            fig = go.Figure()
            fig.update_layout(
                title=f"No Data for Year {year}",
                template="plotly_white"
            )
            return fig
    
        top_mod = top_mod.nlargest(10, "total_budget")
    
        # =========================
        # PLOT
        # =========================
        fig = px.bar(
            top_mod,
            x="total_budget",
            y="mod",
            orientation="h",
            text="total_budget",
            title=f"Top Modules ({year})"
        )
    
        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='inside'
        )
    
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Budget",
            yaxis_title="Module",
            yaxis=dict(categoryorder="total ascending")
        )
    
        return fig