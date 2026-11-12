import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ---------- Configuracion de pagina ----------
st.set_page_config(
    page_title="Dashboard Olist - Proyecto Integrador",
    page_icon="📦",
    layout="wide",
)

# ---------- Carga de datos ----------
@st.cache_data
def cargar_datos():
    base = Path(__file__).parent / "archive"

    orders = pd.read_csv(base / "olist_orders_dataset.csv",
                         parse_dates=["order_purchase_timestamp",
                                      "order_delivered_customer_date",
                                      "order_estimated_delivery_date"])
    items = pd.read_csv(base / "olist_order_items_dataset.csv")
    customers = pd.read_csv(base / "olist_customers_dataset.csv")
    payments = pd.read_csv(base / "olist_order_payments_dataset.csv")
    reviews = pd.read_csv(base / "olist_order_reviews_dataset.csv")
    products = pd.read_csv(base / "olist_products_dataset.csv")
    translation = pd.read_csv(base / "product_category_name_translation.csv")

    # Traducir categorias
    products = products.merge(translation, on="product_category_name", how="left")
    products["category"] = products["product_category_name_english"].fillna(
        products["product_category_name"]
    )

    # Merge principal
    df = (
        orders
        .merge(items, on="order_id", how="inner")
        .merge(customers[["customer_id", "customer_state"]], on="customer_id", how="left")
        .merge(payments.groupby("order_id").agg(
            payment_type=("payment_type", "first"),
            payment_value=("payment_value", "sum")
        ).reset_index(), on="order_id", how="left")
        .merge(reviews[["order_id", "review_score"]].drop_duplicates("order_id"),
               on="order_id", how="left")
        .merge(products[["product_id", "category"]], on="product_id", how="left")
    )

    # Variables derivadas
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    df["estimated_days"] = (
        df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    df["delay_days"] = df["delivery_days"] - df["estimated_days"]
    df["late"] = (df["delay_days"] > 0).astype(int)
    df["total_value"] = df["price"] + df["freight_value"]

    # Solo pedidos entregados con fechas validas
    delivered = df.dropna(subset=["delivery_days"]).copy()
    return delivered

df = cargar_datos()

# ---------- Sidebar: filtros ----------
st.sidebar.header("Filtros")

states = sorted(df["customer_state"].dropna().unique())
sel_states = st.sidebar.multiselect("Estado del cliente", states, default=states)

pay_types = sorted(df["payment_type"].dropna().unique())
sel_pay = st.sidebar.multiselect("Metodo de pago", pay_types, default=pay_types)

# Filtrar
mask = df["customer_state"].isin(sel_states) & df["payment_type"].isin(sel_pay)
filtered = df[mask]

# ---------- KPIs ----------
st.title("Dashboard Olist E-Commerce")
st.markdown("Proyecto Integrador — Big Data 2026-2")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Ingresos Totales (R$)", f"{filtered['total_value'].sum():,.0f}")
k2.metric("Pedidos", f"{filtered['order_id'].nunique():,}")
k3.metric("Review Promedio", f"{filtered['review_score'].mean():.2f}")
pct_on_time = (1 - filtered["late"].mean()) * 100 if len(filtered) > 0 else 0
k4.metric("Entregas a Tiempo", f"{pct_on_time:.1f}%")

st.markdown("---")

# ---------- Graficas ----------
col1, col2 = st.columns(2)

# 1 - Top 10 categorias por ingreso
with col1:
    st.subheader("Top 10 Categorias por Ingreso")
    cat_rev = (
        filtered.groupby("category")["total_value"]
        .sum()
        .nlargest(10)
        .sort_values()
        .reset_index()
    )
    fig1 = px.bar(cat_rev, x="total_value", y="category", orientation="h",
                  labels={"total_value": "Ingresos (R$)", "category": ""},
                  color="total_value", color_continuous_scale="Blues")
    fig1.update_layout(showlegend=False, coloraxis_showscale=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

# 2 - Porcentaje de retrasos por estado
with col2:
    st.subheader("Porcentaje de Entregas Tarde por Estado")
    state_delay = (
        filtered.groupby("customer_state")
        .agg(pedidos=("order_id", "count"), tarde=("late", "sum"))
        .assign(pct_tarde=lambda x: x["tarde"] / x["pedidos"] * 100)
        .sort_values("pct_tarde", ascending=True)
        .reset_index()
    )
    fig2 = px.bar(state_delay, x="pct_tarde", y="customer_state", orientation="h",
                  labels={"pct_tarde": "% Tarde", "customer_state": "Estado"},
                  color="pct_tarde", color_continuous_scale="Reds")
    fig2.update_layout(showlegend=False, coloraxis_showscale=False, height=400)
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

# 3 - Distribucion de metodos de pago
with col3:
    st.subheader("Volumen por Metodo de Pago")
    pay_vol = (
        filtered.groupby("payment_type")["payment_value"]
        .sum()
        .reset_index()
    )
    fig3 = px.pie(pay_vol, values="payment_value", names="payment_type",
                  hole=0.45, color_discrete_sequence=px.colors.qualitative.Set2)
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

# 4 - Tiempo de entrega vs review score
with col4:
    st.subheader("Tiempo de Entrega vs Review Score")
    sample = filtered.dropna(subset=["review_score", "delivery_days"])
    if len(sample) > 3000:
        sample = sample.sample(3000, random_state=42)
    fig4 = px.scatter(sample, x="delivery_days", y="review_score",
                      opacity=0.4,
                      labels={"delivery_days": "Dias de entrega",
                              "review_score": "Review Score"},
                      color="late",
                      color_discrete_map={0: "#2ecc71", 1: "#e74c3c"})
    fig4.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

# 5 - Extra: Evolucion mensual de pedidos
st.subheader("Evolucion Mensual de Pedidos")
monthly = (
    filtered
    .assign(mes=filtered["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp())
    .groupby("mes")["order_id"]
    .nunique()
    .reset_index()
    .rename(columns={"order_id": "pedidos"})
)
fig5 = px.line(monthly, x="mes", y="pedidos",
               labels={"mes": "Mes", "pedidos": "Pedidos"},
               markers=True)
fig5.update_layout(height=350)
st.plotly_chart(fig5, use_container_width=True)

st.caption("Fuente: Brazilian E-Commerce Public Dataset by Olist (Kaggle)")
