import streamlit as st
import plotly.express as px
from utils.preprocessing import carregar_dados

st.set_page_config(layout="wide")

# --- Título ---
st.title("📊 Dashboard Interativo de Vendas - Supermercado")

# --- Carregar Dados ---
df = carregar_dados("data/supermarket_sales.csv")

# --- Filtros ---
st.sidebar.header("Filtros")
ano = st.sidebar.selectbox("Ano", sorted(df["Year"].unique()))
mes = st.sidebar.selectbox("Mês", sorted(df["Month"].unique()))
cidade = st.sidebar.multiselect("Cidade", options=df["City"].unique(), default=df["City"].unique())

df_filtrado = df[(df["Year"] == ano) & (df["Month"] == mes) & (df["City"].isin(cidade))]

# --- Métricas principais ---
st.markdown("### Métricas Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Vendas", f"R$ {df_filtrado['Total'].sum():,.2f}")
col2.metric("Quantidade de Vendas", df_filtrado.shape[0])
col3.metric("Ticket Médio", f"R$ {df_filtrado['Total'].mean():.2f}")

# --- Gráfico por Categoria ---
fig_categoria = px.bar(df_filtrado, x="Product line", y="Total", color="Product line",
                       title="Vendas por Categoria de Produto")
st.plotly_chart(fig_categoria, use_container_width=True)

# --- Top 10 Produtos ---
top_produtos = df_filtrado.groupby("Product line")["Total"].sum().sort_values(ascending=False).head(10)
fig_top = px.bar(top_produtos, x=top_produtos.index, y=top_produtos.values,
                 labels={"x": "Produto", "y": "Total"}, title="Top 10 Produtos por Vendas")
st.plotly_chart(fig_top, use_container_width=True)

# --- Vendas por Cidade com Geolocalização (simples) ---
vendas_por_cidade = df_filtrado.groupby("City")["Total"].sum().reset_index()
fig_mapa = px.scatter_geo(vendas_por_cidade,
                          locations="City",
                          locationmode="country names",
                          size="Total",
                          color="Total",
                          title="Distribuição de Vendas por Cidade",
                          scope="world")
st.plotly_chart(fig_mapa, use_container_width=True)
