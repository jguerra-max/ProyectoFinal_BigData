from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="Olist Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "olist_analitico_limpio.csv"

COLORS = {
    "blue": "#1687D9",
    "navy": "#172033",
    "green": "#55B96B",
    "lime": "#A8D746",
    "yellow": "#F4C95D",
    "orange": "#F59E5B",
    "red": "#EF635B",
    "ink": "#354052",
    "grid": "#E8EDF3",
}


st.markdown(
    """
    <style>
    :root {
        --olist-blue: #1687D9;
        --olist-navy: #172033;
        --olist-ink: #354052;
        --olist-muted: #718096;
        --olist-canvas: #E9EDF2;
    }

    .stApp {
        background: var(--olist-canvas);
        color: var(--olist-ink);
    }

    [data-testid="stHeader"] { background: transparent; }

    [data-testid="stMainBlockContainer"] {
        max-width: 1500px;
        padding-top: 1.25rem;
        padding-bottom: 2.5rem;
    }

    section[data-testid="stSidebar"] {
        background: var(--olist-navy);
        border-right: 0;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding-top: 1.4rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #F7FAFC !important;
    }

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #AAB6C8 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #222E44;
        border-color: #3A4860;
        color: #FFFFFF;
    }

    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #1687D9;
    }

    .brand {
        color: #FFFFFF;
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.1rem;
    }

    .brand span { color: #5BB7F0; font-weight: 500; }

    .sidebar-rule {
        border: 0;
        border-top: 1px solid #354258;
        margin: 1.1rem 0 1.4rem;
    }

    .app-header {
        align-items: center;
        background: #FFFFFF;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08);
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding: 1.2rem 1.45rem;
    }

    .app-header h1 {
        color: var(--olist-ink);
        font-size: clamp(1.55rem, 2.2vw, 2.15rem);
        font-weight: 750;
        letter-spacing: -0.025em;
        line-height: 1.15;
        margin: 0 0 0.35rem;
    }

    .app-header p {
        color: var(--olist-muted);
        font-size: 0.95rem;
        margin: 0;
    }

    .data-badge {
        align-items: center;
        background: #EAF6FD;
        border-radius: 999px;
        color: #0B6FAE;
        display: inline-flex;
        font-size: 0.78rem;
        font-weight: 650;
        gap: 0.45rem;
        padding: 0.45rem 0.75rem;
        white-space: nowrap;
    }

    .data-badge::before {
        background: #38A169;
        border-radius: 50%;
        content: "";
        height: 0.48rem;
        width: 0.48rem;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08);
        min-height: 118px;
        padding: 1.05rem 1.15rem;
    }

    [data-testid="stMetricLabel"] p {
        color: var(--olist-muted);
        font-size: 0.82rem;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: var(--olist-ink);
        font-size: clamp(1.45rem, 2.3vw, 2rem);
        font-variant-numeric: tabular-nums;
        font-weight: 750;
        letter-spacing: -0.025em;
    }

    [data-testid="stColumn"] > [data-testid="stVerticalBlock"] >
    [data-testid="stLayoutWrapper"]:has(.section-heading) {
        background: #FFFFFF;
        border: 0 !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08);
        padding: 0.8rem 1rem 0.45rem;
    }

    .section-heading {
        color: var(--olist-ink);
        font-size: 1rem;
        font-weight: 750;
        letter-spacing: -0.01em;
        margin: 0.4rem 0 0.1rem;
    }

    .section-copy {
        color: var(--olist-muted);
        font-size: 0.8rem;
        margin: 0 0 0.35rem;
    }

    .footer-note {
        color: #64748B;
        font-size: 0.78rem;
        margin-top: 1rem;
        text-align: center;
    }

    a, a:visited { color: #0B78BE; text-underline-offset: 0.18em; }

    *:focus-visible {
        outline: 3px solid rgba(22, 135, 217, 0.38) !important;
        outline-offset: 2px !important;
    }

    ::selection { background: #BDE4FA; color: #172033; }

    @media (max-width: 780px) {
        [data-testid="stMainBlockContainer"] {
            padding-left: 0.85rem;
            padding-right: 0.85rem;
        }

        .app-header {
            align-items: flex-start;
            flex-direction: column;
            gap: 0.9rem;
        }

        .data-badge { white-space: normal; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Cargando datos de Olist...")
def load_data(path: Path) -> pd.DataFrame:
    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    data = pd.read_csv(path, parse_dates=date_columns, low_memory=False)

    text_columns = [
        "customer_state",
        "dominant_product_category",
        "primary_payment_type",
        "order_status",
    ]
    for column in text_columns:
        data[column] = data[column].fillna("unknown").astype(str)

    numeric_columns = [
        "payment_value",
        "freight_value",
        "delivery_days",
        "delay_days",
        "review_score",
    ]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    for column in ["late_delivery", "not_delivered"]:
        if data[column].dtype != bool:
            data[column] = (
                data[column]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin(["true", "1"])
            )

    return data


def compact_currency(value: float) -> str:
    if value >= 1_000_000:
        return f"R$ {value / 1_000_000:.2f} M"
    if value >= 1_000:
        return f"R$ {value / 1_000:.1f} mil"
    return f"R$ {value:,.2f}"


def panel_heading(title: str, description: str) -> None:
    st.markdown(
        f'<p class="section-heading">{title}</p>'
        f'<p class="section-copy">{description}</p>',
        unsafe_allow_html=True,
    )


def style_figure(fig: go.Figure, height: int = 350) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=20, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color=COLORS["ink"], size=12),
        hoverlabel=dict(bgcolor="#172033", font_color="#FFFFFF", bordercolor="#172033"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(
        automargin=True,
        gridcolor=COLORS["grid"],
        linecolor=COLORS["grid"],
        zeroline=False,
    )
    fig.update_yaxes(
        automargin=True,
        gridcolor=COLORS["grid"],
        linecolor=COLORS["grid"],
        zeroline=False,
    )
    return fig


def render_figure(fig: go.Figure, key: str) -> None:
    st.plotly_chart(
        fig,
        width="stretch",
        key=key,
        theme=None,
        config={"displayModeBar": False, "responsive": True},
    )


st.sidebar.markdown(
    '<div class="brand">OLIST <span>ANALYTICS</span></div>'
    '<p style="color:#AAB6C8;margin:0;font-size:.8rem;">Control logístico y comercial</p>'
    '<hr class="sidebar-rule">',
    unsafe_allow_html=True,
)

if not DATA_FILE.exists():
    st.error(
        "No se encontró data/olist_analitico_limpio.csv. "
        "Ubique el archivo dentro de la carpeta data y vuelva a ejecutar la aplicación."
    )
    st.stop()

df = load_data(DATA_FILE)

st.sidebar.subheader("Filtros del análisis")
st.sidebar.caption("Cada selección actualiza los indicadores y gráficos.")

state_options = sorted(df["customer_state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "Estados del cliente",
    options=state_options,
    default=state_options,
)

category_options = sorted(df["dominant_product_category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox(
    "Categoría de producto",
    options=["Todas"] + category_options,
)

payment_options = sorted(df["primary_payment_type"].dropna().unique().tolist())
selected_payments = st.sidebar.multiselect(
    "Medios de pago",
    options=payment_options,
    default=payment_options,
)

filtered = df[
    df["customer_state"].isin(selected_states)
    & df["primary_payment_type"].isin(selected_payments)
].copy()

if selected_category != "Todas":
    filtered = filtered[filtered["dominant_product_category"] == selected_category].copy()

if filtered.empty:
    st.warning(
        "No hay registros para esta combinación. Seleccione al menos un estado "
        "y un medio de pago, o cambie la categoría."
    )
    st.stop()

st.markdown(
    """
    <div class="app-header">
        <div>
            <h1>Optimización logística y ventas</h1>
            <p>Desempeño de entregas, satisfacción, categorías y medios de pago en Olist.</p>
        </div>
        <div class="data-badge">Dataset analítico depurado</div>
    </div>
    """,
    unsafe_allow_html=True,
)

valid_deliveries = filtered[
    (filtered["order_status"] == "delivered")
    & filtered["delivery_days"].notna()
].copy()

total_orders = filtered["order_id"].nunique()
total_sales = filtered["payment_value"].sum()
late_rate = (
    valid_deliveries["late_delivery"].mean() * 100
    if not valid_deliveries.empty
    else 0.0
)
average_review = filtered["review_score"].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Pedidos analizados", f"{total_orders:,}")
kpi2.metric("Ingresos", compact_currency(total_sales))
kpi3.metric("Entregas tardías", f"{late_rate:.2f}%")
kpi4.metric(
    "Calificación promedio",
    f"{average_review:.2f} / 5" if pd.notna(average_review) else "Sin datos",
)

st.markdown("<div style='height:.35rem'></div>", unsafe_allow_html=True)

donut_left, donut_right = st.columns(2)

with donut_left:
    with st.container(border=True):
        panel_heading(
            "Cumplimiento de entregas",
            "Participación de pedidos entregados a tiempo y con retraso.",
        )
        late_orders = int(valid_deliveries["late_delivery"].sum())
        on_time_orders = int(len(valid_deliveries) - late_orders)
        delivery_summary = pd.DataFrame(
            {
                "Resultado": ["A tiempo", "Con retraso"],
                "Pedidos": [on_time_orders, late_orders],
            }
        )
        fig_delivery = px.pie(
            delivery_summary,
            names="Resultado",
            values="Pedidos",
            hole=0.68,
            color="Resultado",
            color_discrete_map={
                "A tiempo": COLORS["green"],
                "Con retraso": COLORS["red"],
            },
        )
        fig_delivery.update_traces(
            textinfo="percent",
            textposition="inside",
            marker=dict(line=dict(color="#FFFFFF", width=3)),
            hovertemplate="%{label}<br>%{value:,} pedidos<br>%{percent}<extra></extra>",
        )
        fig_delivery.add_annotation(
            text=f"<b>{late_rate:.1f}%</b><br><span style='font-size:12px'>tarde</span>",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=21, color=COLORS["ink"]),
        )
        render_figure(style_figure(fig_delivery, 315), "delivery_donut")

with donut_right:
    with st.container(border=True):
        panel_heading(
            "Satisfacción del cliente",
            "Distribución de reseñas entre una y cinco estrellas.",
        )
        review_distribution = (
            filtered.dropna(subset=["review_score"])
            .assign(review_score=lambda data: data["review_score"].round().astype(int))
            .groupby("review_score", as_index=False)
            .agg(Pedidos=("order_id", "nunique"))
        )
        review_distribution["Calificación"] = review_distribution["review_score"].map(
            lambda score: f"{score} estrella" if score == 1 else f"{score} estrellas"
        )
        rating_colors = {
            "1 estrella": COLORS["red"],
            "2 estrellas": COLORS["orange"],
            "3 estrellas": COLORS["yellow"],
            "4 estrellas": COLORS["lime"],
            "5 estrellas": COLORS["green"],
        }
        fig_reviews = px.pie(
            review_distribution,
            names="Calificación",
            values="Pedidos",
            hole=0.68,
            color="Calificación",
            color_discrete_map=rating_colors,
            category_orders={"Calificación": list(rating_colors)},
        )
        fig_reviews.update_traces(
            textinfo="percent",
            textposition="inside",
            marker=dict(line=dict(color="#FFFFFF", width=3)),
            hovertemplate="%{label}<br>%{value:,} pedidos<br>%{percent}<extra></extra>",
        )
        fig_reviews.add_annotation(
            text=f"<b>{average_review:.2f}</b><br><span style='font-size:12px'>de 5</span>",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=21, color=COLORS["ink"]),
        )
        render_figure(style_figure(fig_reviews, 315), "review_donut")

state_logistics = (
    valid_deliveries.groupby("customer_state", as_index=False)
    .agg(
        pedidos=("order_id", "nunique"),
        porcentaje_tarde=("late_delivery", "mean"),
        tiempo_promedio=("delivery_days", "mean"),
    )
)
state_logistics["porcentaje_tarde"] *= 100
state_logistics = state_logistics.nlargest(10, "porcentaje_tarde").sort_values("porcentaje_tarde")

category_sales = (
    filtered.groupby("dominant_product_category", as_index=False)
    .agg(
        ingresos=("payment_value", "sum"),
        pedidos=("order_id", "nunique"),
    )
    .nlargest(10, "ingresos")
    .sort_values("ingresos")
)

middle_left, middle_right = st.columns(2)

with middle_left:
    with st.container(border=True):
        panel_heading(
            "Estados con mayor retraso",
            "Porcentaje de entregas tardías en los diez estados más críticos.",
        )
        fig_states = px.bar(
            state_logistics,
            x="porcentaje_tarde",
            y="customer_state",
            orientation="h",
            custom_data=["pedidos", "tiempo_promedio"],
            labels={
                "customer_state": "Estado",
                "porcentaje_tarde": "Entregas tardías (%)",
            },
        )
        fig_states.update_traces(
            marker_color=COLORS["blue"],
            marker_cornerradius=5,
            hovertemplate=(
                "%{y}<br>%{x:.2f}% tarde<br>%{customdata[0]:,} pedidos"
                "<br>%{customdata[1]:.1f} días promedio<extra></extra>"
            ),
        )
        style_figure(fig_states, 390)
        fig_states.update_layout(margin=dict(l=45, r=18, t=20, b=68))
        fig_states.update_xaxes(title_standoff=20)
        fig_states.update_yaxes(title_standoff=14)
        render_figure(fig_states, "state_delays")

with middle_right:
    with st.container(border=True):
        panel_heading(
            "Categorías con mayores ingresos",
            "Las diez categorías que concentran mayor valor de ventas.",
        )
        fig_categories = px.bar(
            category_sales,
            x="ingresos",
            y="dominant_product_category",
            orientation="h",
            custom_data=["pedidos"],
            labels={
                "ingresos": "Ingresos (R$)",
                "dominant_product_category": "Categoría",
            },
        )
        fig_categories.update_traces(
            marker_color=COLORS["lime"],
            marker_cornerradius=5,
            hovertemplate=(
                "%{y}<br>R$ %{x:,.2f}<br>%{customdata[0]:,} pedidos<extra></extra>"
            ),
        )
        style_figure(fig_categories, 390)
        fig_categories.update_layout(margin=dict(l=155, r=18, t=20, b=68))
        fig_categories.update_xaxes(title_standoff=20)
        fig_categories.update_yaxes(title_standoff=14)
        render_figure(fig_categories, "category_sales")

satisfaction = filtered.dropna(subset=["delivery_days", "review_score"]).copy()
if len(satisfaction) > 4_000:
    satisfaction = satisfaction.sample(4_000, random_state=42)
satisfaction["Estado de entrega"] = satisfaction["late_delivery"].map(
    {False: "A tiempo", True: "Con retraso"}
)

payment_risk = (
    filtered.groupby("primary_payment_type", as_index=False)
    .agg(
        volumen=("payment_value", "sum"),
        tasa_no_entregado=("not_delivered", "mean"),
        pedidos=("order_id", "nunique"),
    )
    .sort_values("volumen", ascending=False)
)
payment_risk["tasa_no_entregado"] *= 100

bottom_left, bottom_right = st.columns(2)

with bottom_left:
    with st.container(border=True):
        panel_heading(
            "Tiempo de entrega y calificación",
            "Relación entre la duración logística y la reseña del comprador.",
        )
        fig_satisfaction = px.scatter(
            satisfaction,
            x="delivery_days",
            y="review_score",
            color="Estado de entrega",
            opacity=0.42,
            color_discrete_map={
                "A tiempo": COLORS["blue"],
                "Con retraso": COLORS["red"],
            },
            labels={
                "delivery_days": "Tiempo real de entrega (días)",
                "review_score": "Calificación",
            },
        )
        fig_satisfaction.update_traces(
            marker=dict(size=7),
            hovertemplate="%{x:.1f} días<br>Calificación: %{y:.0f}<extra></extra>",
        )
        style_figure(fig_satisfaction, 390)
        fig_satisfaction.update_layout(margin=dict(l=62, r=18, t=24, b=78))
        fig_satisfaction.update_xaxes(title_standoff=22)
        fig_satisfaction.update_yaxes(title_standoff=18)
        render_figure(fig_satisfaction, "delivery_satisfaction")

with bottom_right:
    with st.container(border=True):
        panel_heading(
            "Volumen y riesgo por medio de pago",
            "Ingresos comparados con la tasa de pedidos no entregados.",
        )
        fig_payments = make_subplots(specs=[[{"secondary_y": True}]])
        fig_payments.add_trace(
            go.Bar(
                x=payment_risk["primary_payment_type"],
                y=payment_risk["volumen"],
                name="Volumen",
                marker_color=COLORS["blue"],
                marker_cornerradius=5,
                customdata=payment_risk[["pedidos"]],
                hovertemplate=(
                    "%{x}<br>R$ %{y:,.2f}<br>%{customdata[0]:,} pedidos<extra></extra>"
                ),
            ),
            secondary_y=False,
        )
        fig_payments.add_trace(
            go.Scatter(
                x=payment_risk["primary_payment_type"],
                y=payment_risk["tasa_no_entregado"],
                name="No entregados",
                mode="lines+markers",
                line=dict(color=COLORS["red"], width=3),
                marker=dict(size=8),
                hovertemplate="%{x}<br>%{y:.2f}% no entregado<extra></extra>",
            ),
            secondary_y=True,
        )
        style_figure(fig_payments, 390)
        fig_payments.update_layout(margin=dict(l=78, r=78, t=24, b=82))
        fig_payments.update_yaxes(
            title_text="Volumen (R$)",
            title_standoff=18,
            secondary_y=False,
        )
        fig_payments.update_yaxes(
            title_text="No entregados (%)",
            title_standoff=18,
            secondary_y=True,
        )
        fig_payments.update_xaxes(title_text="Medio de pago", title_standoff=22)
        render_figure(fig_payments, "payment_risk")

st.markdown(
    """
    <p class="footer-note">
        Fuente: Brazilian E-Commerce Public Dataset by Olist (Kaggle).
        Los indicadores se recalculan con los filtros laterales.
    </p>
    """,
    unsafe_allow_html=True,
)
