import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pygam import *
import statsmodels.formula.api as smf
from statsmodels.tsa.seasonal import STL
from plotly.subplots import make_subplots
import nbformat

database = pd.read_csv("Cafeteria Fictícia.csv")

# database.sample(10)

sales_summary = database.groupby(["coffee_name", "money"]).size().reset_index(name = "quantity")

figure1 = px.scatter(
    sales_summary, x = "quantity", y = "money", color = "coffee_name", trendline = "ols",
    labels = {"money": "Preço (R$)", "quantity": "Quantidade", "coffee_name": "Item"},
    title = "Análise Exploratória — Demandas Inversas", width = 1000, height = 500
)

figure1.update_layout(
    title_font_size = 18, font = dict(size = 14, family = "Arial", color = "black"),
    plot_bgcolor = "white", paper_bgcolor = "white",
    legend = dict(title = "", borderwidth = 0, font_size = 12, bgcolor = "rgba(0,0,0,0)"),
    xaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14),
    yaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14)
)

# figure1.show()

figure2 = px.violin(
    database, x = "coffee_name",  y = "money", color = "coffee_name", box = False, points = "all",
    labels = {"money": "Preço (R$)", "coffee_name": "Item"},
    title = "Análise Exploratória — Distribuições de Preços", width = 1000, height = 500
)

figure2.update_layout(
    title_font_size = 18, font = dict(size = 14, family = "Arial", color = "black"),
    plot_bgcolor = "white", paper_bgcolor = "white",
    showlegend = False,
    xaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14),
    yaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14)
)

# figure2.show()

elasticities = []

latest_prices = database.sort_values("datetime").groupby("coffee_name").tail(1)
latest_prices = latest_prices.set_index("coffee_name")["money"]

for item in sales_summary["coffee_name"].unique():
    item_data = sales_summary[sales_summary["coffee_name"] == item]

    item_data["quantity"] = np.log(item_data["quantity"])
    item_data["money"] = np.log(item_data["money"])

    log_log = smf.ols("quantity ~ money", data = item_data).fit()
    beta_0, beta_1 = log_log.params

    P0 = latest_prices[item]
    Q0 = beta_0 + beta_1 * P0

    current_elasticity = beta_1 * (P0 / Q0)

    elasticities.append({
        "coffee_name": item,
        "current_price": P0,
        "predicted_quantity": Q0,
        "current_elasticity": np.abs(current_elasticity)
    })

elasticities = pd.DataFrame(elasticities)

figure3 = px.bar(
    elasticities,
    x = "coffee_name", y = "current_elasticity", color = "coffee_name",
    labels = {"coffee_name": "Item", "current_elasticity": "Nível"},
    title = "Análise Exploratória — Elasticidades-preço da Demanda Atuais", width = 1000, height = 500
)

for index, row in elasticities.iterrows():
    figure3.add_annotation(
        x = row["coffee_name"], y = row["current_elasticity"],
        text = f"<b>{row["current_elasticity"]:.2f}</b>",
        showarrow = False, font = dict(color = "white", size = 12),
        align = "center", bordercolor = "black",
        borderwidth = 1, bgcolor = "black", opacity = 0.8
    )

figure3.update_layout(
    title_font_size = 18,
    font = dict(size = 14, family = "Arial", color = "black"),
    plot_bgcolor = "white",
    paper_bgcolor = "white",
    legend = dict(title = "", borderwidth = 0, font_size = 12, bgcolor = "rgba(0,0,0,0)"),
    xaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14),
    yaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14)
)

# figure3.show()

accumulated_revenue = (database.groupby(["date", "coffee_name"])["money"]
                 .sum().groupby(level = 1 ).cumsum().reset_index(name = "accumulated_revenue"))

accumulated_revenue["accumulated_revenue"] /= 1000

figure4 = px.line(accumulated_revenue, x = "date", y = "accumulated_revenue", color = "coffee_name",
               labels = {"date": "Data", "accumulated_revenue": "Receita acumulada (mil R$)", "coffee_name": "Item"},
               title = "Análise Exploratória — Receitas Acumuladas", width = 1000, height = 500)

figure4.update_layout(
    title_font_size = 18, font = dict(size = 14, family = "Arial", color = "black"),
    plot_bgcolor = "white", paper_bgcolor = "white",
    legend = dict(title = "", font_size = 12, bgcolor = "rgba(0,0,0,0)"),
    xaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14, tickformat = "%d/%m/%Y"),
    yaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14)
)

# figure4.show()

daily_revenue = (database.groupby(["date", "coffee_name"])["money"]
                 .sum().reset_index(name = "daily_revenue"))

figure5 = px.line(
    daily_revenue, x = "date", y = "daily_revenue", color = "coffee_name",
    labels = {"date": "Data", "daily_revenue": "Receita diária (R$)", "coffee_name": "Item"},
    title = "Análise Exploratória — Receitas Diárias", width = 1000, height = 500
)

figure5.update_layout(
    title_font_size = 18, font = dict(size = 14, family = "Arial", color = "black"),
    plot_bgcolor = "white", paper_bgcolor = "white",
    legend = dict(title = "", font_size = 12, bgcolor = "rgba(0,0,0,0)"),
    xaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14, tickformat = "%d/%m/%Y"),
    yaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14)
)

# figure5.show()

database["date"] = pd.to_datetime(database["date"])

translated_weekdays = {0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"}
database["weekday"] = database["date"].dt.dayofweek.map(translated_weekdays)

weekdays_revenue = (database.groupby(["date", "weekday"])["money"]
                   .mean().reset_index(name = "weekdays_revenue"))

weekdays_revenue["weekday"] = pd.Categorical(weekdays_revenue["weekday"], ordered = True)

figure6 = px.line(
    weekdays_revenue, x = "date", y = "weekdays_revenue", color = "weekday",
    labels = {"date": "Data", "weekdays_revenue": "Receita média (R$)", "weekday": "Dia da semana"},
    title = "Análise Exploratória — Receitas Médias por Dia da Semana", width = 1000, height = 500
)

figure6.update_layout(
    title_font_size = 18,
    font = dict(size = 14, family = "Arial", color = "black"),
    plot_bgcolor = "white",
    paper_bgcolor = "white",
    legend = dict(title = "", font_size = 12, bgcolor = "rgba(0,0,0,0)"),
    xaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14, tickformat = "%d/%m/%Y"),
    yaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14)
)

# figure6.show()

daily_revenue = (database.groupby(["date", "coffee_name"])["money"]
                 .sum().reset_index(name="daily_revenue"))

daily_revenue["date"] = pd.to_datetime(daily_revenue["date"])
daily_revenue = daily_revenue.set_index("date")

weekly_revenue = (daily_revenue.groupby("coffee_name")
                  .resample("W")["daily_revenue"]
                  .mean()
                  .reset_index())

weekly_revenue["total_week"] = weekly_revenue.groupby("date")["daily_revenue"].transform("sum")
weekly_revenue["percentage_revenue"] = weekly_revenue["daily_revenue"] / weekly_revenue["total_week"] * 100

figure7 = px.area(
    weekly_revenue, 
    x = "date", y = "percentage_revenue", color = "coffee_name",
    labels = {"date": "Data", "percentage_revenue": "Participação", "coffee_name": "Item"},
    title = "Análise Exploratória — Composição Dinâmica da Receita", width = 1000, height = 500
)

figure7.update_layout(
    title_font_size = 18,
    font = dict(size = 14, family = "Arial", color = "black"),
    plot_bgcolor = "white",
    paper_bgcolor = "white",
    legend = dict(title = "", font_size = 12, bgcolor = "rgba(0,0,0,0)"),
    xaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14, tickformat = "%d/%m/%Y"),
    yaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14, ticksuffix = "%")
)

# figure7.show()

optimal_prices = []
gam_results = {}

for item in sales_summary["coffee_name"].unique():
    item_data = sales_summary[sales_summary["coffee_name"] == item]

    price_values = item_data[["money"]].values
    quantity_values = item_data["quantity"].values

    gam = PoissonGAM(s(0, n_splines = 5, spline_order = 3, constraints = "monotonic_dec")).gridsearch(price_values, quantity_values)
    price_range = np.linspace(price_values.min(), price_values.max(), 100)

    demand_estimated = gam.predict(price_range)
    revenue_estimated = price_range * demand_estimated / 1000

    optimal_index = np.argmax(revenue_estimated)
    optimal_price = price_range[optimal_index]
    optimal_quantity = demand_estimated[optimal_index]

    optimal_prices.append({
        "coffee_name": item,
        "optimal_price": round(optimal_price, 2),
        "expected_quantity": round(optimal_quantity, 2),
        "expected_revenue": round(revenue_estimated[optimal_index], 2)
    })

    gam_results[item] = {
        "price_range": price_range,
        "demand_estimated": demand_estimated,
        "revenue_estimated": revenue_estimated,
        "optimal_price": optimal_price,
        "optimal_quantity": optimal_quantity
    }

figure8 = go.Figure()

colors = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", 
          "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF"]

for index, item in enumerate(sales_summary["coffee_name"].unique()):
    item_data = sales_summary[sales_summary["coffee_name"] == item]
    result = gam_results[item]
    color = colors[index % len(colors)]
    visible = (item == sales_summary["coffee_name"].unique()[0])

    figure8.add_trace(go.Scatter(
        x = item_data["money"], y = item_data["quantity"], 
        mode = "markers", name = "Observado",
        marker = dict(size = 8, color = color, opacity = 0.6),
        visible = visible, legendgroup = "observed", showlegend = True
    ))

    figure8.add_trace(go.Scatter(
        x = result["price_range"], y = result["demand_estimated"],
        mode = "lines", name = "Demanda estimada",
        line = dict(color = color, width = 2),
        visible = visible, legendgroup = "demand", showlegend = True
    ))

    figure8.add_trace(go.Scatter(
        x = result["price_range"], y = result["revenue_estimated"],
        mode = "lines", name = "Receita",
        line = dict(color = color, dash = "dot", width = 2),
        yaxis = "y2", visible = visible, 
        legendgroup = "revenue", showlegend = True
    ))

    figure8.add_trace(go.Scatter(
        x = [result["optimal_price"]], y = [result["optimal_quantity"]],
        mode = "markers+text", text = [f"Ótimo: R$ {result["optimal_price"]:.2f}"],
        textposition = "top center", marker = dict(color = color, size = 10),
        name = "Ótimo", visible = visible, 
        legendgroup = "optimal", showlegend = True
    ))

buttons = []

for item in sales_summary["coffee_name"].unique():
    buttons.append({
        "label": item, "method": "update",
        "args": [{"visible": [item == coffee for coffee in sales_summary["coffee_name"].unique() for _ in range(4)],
                  "title": f"Generalized Additive Model (GAM)"}]
    })

figure8.update_layout(
    title = f"Generalized Additive Model (GAM)",
    title_font_size = 18, font = dict(size = 14, family = "Arial", color = "black"),
    width = 1000, height = 500, plot_bgcolor = "white", paper_bgcolor = "white",
    xaxis = dict(title = "Preço (R$)", showgrid = True, gridcolor = "lightgrey", 
                 zeroline = False, title_font_size = 14),
    yaxis = dict(title = "Quantidade", showgrid = True, gridcolor = "lightgrey", 
                 zeroline = False, title_font_size = 14),
    yaxis2 = dict(title = "Receita (mil R$)", overlaying = "y", side = "right",
                  showgrid = False, zeroline = False, title_font_size = 14),
    legend = dict(title = "", borderwidth = 0, font_size = 12, 
                  bgcolor = "rgba(0,0,0,0)", orientation = "v", x = 1.08, y = 1),
    updatemenus = [dict(
        buttons = buttons, direction = "down", showactive = True,
        x = 1.0, xanchor = "right", y = 1.15, yanchor = "top"
    )]
)

# figure8.show()

optimal_elasticities = []

for item in sales_summary["coffee_name"].unique():
    result = gam_results[item]
    price_range = result["price_range"]
    demand_estimated = result["demand_estimated"]
    optimal_index = np.argmax(result["revenue_estimated"])

    optimal_P = price_range[optimal_index]
    optimal_Q = demand_estimated[optimal_index]

    if optimal_index > 0 and optimal_index < len(price_range) - 1:
        dP = price_range[optimal_index + 1] - price_range[optimal_index - 1]
        dQ = demand_estimated[optimal_index + 1] - demand_estimated[optimal_index - 1]
        dQ_dP = dQ / dP
    elif optimal_index == 0:
        dP = price_range[1] - price_range[0]
        dQ = demand_estimated[1] - demand_estimated[0]
        dQ_dP = dQ / dP
    else:
        dP = price_range[-1] - price_range[-2]
        dQ = demand_estimated[-1] - demand_estimated[-2]
        dQ_dP = dQ / dP

    optimal_elasticity = dQ_dP * (optimal_P / optimal_Q)

    optimal_elasticities.append({
        "coffee_name": item,
        "optimal_price": optimal_P,
        "predicted_quantity": optimal_Q,
        "optimal_elasticity": np.abs(optimal_elasticity)
    })

optimal_elasticities = pd.DataFrame(optimal_elasticities)

figure9 = px.bar(
    optimal_elasticities,
    x = "coffee_name", y = "optimal_elasticity", color = "coffee_name",
    labels = {"coffee_name": "Item", "optimal_elasticity": "Nível"},
    title = "Elasticidades-preço da Demanda Ótimas", width = 1000, height = 500
)

for index, row in optimal_elasticities.iterrows():
    figure9.add_annotation(
        x = row["coffee_name"], y = row["optimal_elasticity"],
        text = f"<b>{row["optimal_elasticity"]:.2f}</b>",
        showarrow = False, font = dict(color = "white", size = 12),
        align = "center", bordercolor = "black",
        borderwidth = 1, bgcolor = "black", opacity = 0.8
    )

figure9.update_layout(
    title_font_size = 18,
    font = dict(size = 14, family = "Arial", color = "black"),
    plot_bgcolor = "white",
    paper_bgcolor = "white",
    legend = dict(title = "", borderwidth = 0, font_size = 12, bgcolor = "rgba(0,0,0,0)"),
    xaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14),
    yaxis = dict(showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14)
)

# figure9.show()

daily_revenue = (database.groupby(["date", "coffee_name"])["money"]
                 .sum().reset_index(name = "daily_revenue"))

daily_revenue["date"] = pd.to_datetime(daily_revenue["date"])

items_list = list(sales_summary["coffee_name"].unique())

decomposition_frames = []

for index, item in enumerate(items_list):
    series = (daily_revenue.loc[daily_revenue["coffee_name"] == item, ["date", "daily_revenue"]]
                                  .set_index("date")
                                  .sort_index()
                                  .asfreq("D"))

    series["daily_revenue"] = series["daily_revenue"].fillna(0.0)

    stl = STL(series["daily_revenue"], period = 7, robust = True)
    stl_result = stl.fit()

    decomposition_frame = pd.DataFrame({
        "date": series.index,
        "coffee_name": item,
        "trend": stl_result.trend,
        "seasonal": stl_result.seasonal,
        "residual": stl_result.resid
    }).reset_index(drop = True)

    decomposition_frames.append(decomposition_frame)

decomposition_data = pd.concat(decomposition_frames, ignore_index = True)

figure10 = make_subplots(
    rows = 3, cols = 1, shared_xaxes = True, vertical_spacing = 0.08,
    subplot_titles = ("Tendência", "Sazonalidade", "Resíduo")
)

trace_visibility = []

for index, item in enumerate(items_list):
    color = colors[index % len(colors)]
    slice = decomposition_data[decomposition_data["coffee_name"] == item]

    is_visible = (index == 0)

    figure10.add_trace(
        go.Scatter(
            x = slice["date"], y = slice["trend"],
            mode = "lines", name = "Tendência",
            line = dict(width = 2, color = color),
            visible = is_visible,
            showlegend = True
        ),
        row = 1, col = 1
    )
    trace_visibility.append(is_visible)

    figure10.add_trace(
        go.Scatter(
            x = slice["date"], y = slice["seasonal"],
            mode = "lines", name = "Sazonalidade",
            line = dict(width = 2, color = color),
            visible = is_visible,
            showlegend = True
        ),
        row = 2, col = 1
    )
    trace_visibility.append(is_visible)

    figure10.add_trace(
        go.Scatter(
            x = slice["date"], y = slice["residual"],
            mode = "lines", name = "Resíduo",
            line = dict(width = 2, color = color, dash = "dot"),
            visible = is_visible,
            showlegend = True
        ),
        row = 3, col = 1
    )
    trace_visibility.append(is_visible)

buttons = []
traces_per_item = 3
total_traces = traces_per_item * len(items_list)

for index, item in enumerate(items_list):
    visibility_mask = [False] * total_traces
    start = index * traces_per_item
    for k in range(traces_per_item):
        visibility_mask[start + k] = True

    buttons.append(dict(
        label = item,
        method = "update",
        args = [
            {"visible": visibility_mask},
            {"title": f"Decomposição de Receita — {item}"}
        ]
    ))

figure10.update_layout(
    title = f"Tendência, Sazonalidade e Resíduo",
    title_font_size = 18,
    font = dict(size = 14, family = "Arial", color = "black"),
    width = 1000, height = 700,
    plot_bgcolor = "white", paper_bgcolor = "white",
    legend = dict(title = "", borderwidth = 0, font_size = 12, bgcolor = "rgba(0,0,0,0)"),
    updatemenus = [dict(
        buttons = buttons, direction = "down", showactive = True,
        x = 1.0, xanchor = "right", y = 1.15, yanchor = "top"
    )]
)

figure10.update_xaxes(
    showgrid = True, gridcolor = "lightgrey", zeroline = False, title_font_size = 14,
    tickformat = "%d/%m/%Y", row = 3, col = 1, title_text = "Data"
)
figure10.update_xaxes(
    showgrid = True, gridcolor = "lightgrey", zeroline = False, tickformat = "%d/%m/%Y", row = 1, col = 1
)
figure10.update_xaxes(
    showgrid = True, gridcolor = "lightgrey", zeroline = False, tickformat = "%d/%m/%Y", row = 2, col = 1
)

figure10.update_yaxes(title_text = "Nível", showgrid = True, gridcolor = "lightgrey",
                     zeroline = False, title_font_size = 14, row = 1, col = 1)
figure10.update_yaxes(title_text = "Nível", showgrid = True, gridcolor = "lightgrey",
                     zeroline = False, title_font_size = 14, row = 2, col = 1)
figure10.update_yaxes(title_text = "Nível", showgrid = True, gridcolor = "lightgrey",
                     zeroline = False, title_font_size = 14, row = 3, col = 1)

# figure10.show()

comparison_table = pd.DataFrame(optimal_prices)

comparison_table["current_price"] = comparison_table["coffee_name"].map(latest_prices)
comparison_table["percent_difference"] = (comparison_table["optimal_price"] - comparison_table["current_price"]) / comparison_table["current_price"] * 100
comparison_table["estimated_revenue"] = comparison_table["optimal_price"] * comparison_table["expected_quantity"]

comparison_table = comparison_table[[
    "coffee_name",
    "current_price",
    "optimal_price",
    "percent_difference",
    "expected_quantity",
    "estimated_revenue"
]]

comparison_table.columns = [
    "Item",
    "Preço atual (R$)",
    "Preço ótimo (R$)",
    "Diferença (%)",
    "Quantidade estimada",
    "Receita estimada (R$)"
]

# comparison_table.to_csv("Entregável - Tabela de Comparação.csv", sep = ";", decimal = ",", index = False, encoding = "utf-8-sig")

# revision = pd.read_csv("Entregável - Tabela de Comparação.csv", sep = ";", decimal = ",")
# revision.sample(5)

with open("Script Consolidado (26-08-2025 23h45min K).ipynb", "r", encoding = "utf-8") as f:
    nb = nbformat.read(f, as_version = 4)

code = ""
for cell in nb.cells:
    if cell.cell_type == "code":
        code += cell.source + "\n\n"

with open("Conector.py", "w", encoding="utf-8") as f:
    f.write(code)


