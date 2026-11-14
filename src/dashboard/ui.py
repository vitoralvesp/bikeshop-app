import pandas as pd
import streamlit as st

from src.dashboard.catalog import CatalogAnalytics
from src.dashboard.settings import format_brl
from src.dashboard.views.catalog import CatalogView
from src.dashboard.views.inventory import InventoryView
from src.dashboard.views.pricing import PricingView


class DashboardUI:
    @staticmethod
    def render_filters(catalog: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        with st.sidebar:
            st.header("Filtros")
            brands = sorted(catalog["brand"].dropna().unique().tolist())
            categories = sorted(catalog["category"].dropna().unique().tolist())
            selected_brands = st.multiselect("Marcas", brands, default=brands)
            selected_categories = st.multiselect(
                "Categorias", categories, default=categories
            )
            active_only = st.checkbox("Somente Produtos Ativos", value=True)
            low_stock_limit = st.number_input(
                "Alerta de Estoque Baixo (Unidades)",
                min_value=0,
                value=2,
                step=1,
            )

        filtered = catalog[
            catalog["brand"].isin(selected_brands)
            & catalog["category"].isin(selected_categories)
        ]
        if active_only:
            filtered = filtered[filtered["is_active"]]
        return filtered, low_stock_limit

    @classmethod
    def render(cls, analytics: CatalogAnalytics, low_stock_limit: int) -> None:
        cls._render_metrics(analytics)
        inventory_tab, catalog_tab, price_tab = st.tabs(
            ["Estoque e Reposição", "Catálogo e Preços", "Preço e Margem"]
        )
        with inventory_tab:
            InventoryView.render(analytics, low_stock_limit)
        with catalog_tab:
            CatalogView.render(analytics)
        with price_tab:
            PricingView.render(analytics)

        cls._render_catalog_table(analytics.products)
        st.caption(
            "Os dados representam o catálogo e o estoque atuais. Não há histórico "
            "de vendas ou datas para calcular faturamento, produtos mais vendidos "
            "ou evolução mensal."
        )

    @staticmethod
    def _render_metrics(analytics: CatalogAnalytics) -> None:
        metric_columns = st.columns(3)
        metric_columns[0].metric(
            "Modelos", f"{analytics.model_count:,}".replace(",", ".")
        )
        metric_columns[1].metric(
            "Unidades em Estoque", f"{analytics.unit_count:,}".replace(",", ".")
        )
        metric_columns[2].metric(
            "Valor potencial do Estoque",
            format_brl(analytics.potential_stock_value),
        )
        st.caption(
            "Valores estimados com os preços cadastrados; "
            "não representam vendas realizadas."
        )

    @staticmethod
    def _render_catalog_table(products: pd.DataFrame) -> None:
        st.subheader("Catálogo filtrado")
        display_catalog = products[
            [
                "model",
                "brand",
                "category",
                "cost_price",
                "sale_price",
                "stock_quantity",
                "gross_margin_percentage",
                "is_active",
            ]
        ].rename(
            columns={
                "model": "Modelo",
                "brand": "Marca",
                "category": "Categoria",
                "cost_price": "Preço de custo",
                "sale_price": "Preço de venda",
                "stock_quantity": "Unidades",
                "gross_margin_percentage": "Margem bruta (%)",
                "is_active": "Ativo",
            }
        )
        st.dataframe(
            display_catalog,
            hide_index=True,
            width="stretch",
            column_config={
                "Preço de custo": st.column_config.NumberColumn(format="R$ %.2f"),
                "Preço de venda": st.column_config.NumberColumn(format="R$ %.2f"),
                "Margem bruta (%)": st.column_config.NumberColumn(format="%.2f%%"),
            },
        )
