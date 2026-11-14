import pandas as pd
import streamlit as st

from src.dashboard.catalog import CatalogAnalytics
from src.dashboard.charts import DashboardCharts


class InventoryView:
    @classmethod
    def render(cls, analytics: CatalogAnalytics, low_stock_limit: int) -> None:
        chart_columns = st.columns(2)
        with chart_columns[0]:
            st.subheader("1. Estoque por marca")
            cls._show_bar(
                analytics.stock_by_brand(),
                "brand",
                "stock_quantity",
                "Marca",
                "Unidades",
            )
        with chart_columns[1]:
            st.subheader("5. Valor potencial do estoque por marca")
            cls._show_bar(
                analytics.sale_value_by_brand(),
                "brand",
                "stock_value_at_sale_price",
                "Marca",
                "Valor potencial (R$)",
            )

        chart_columns = st.columns(2)
        with chart_columns[0]:
            st.subheader("6. Valor do estoque a custo por categoria")
            cls._show_bar(
                analytics.cost_value_by_category(),
                "category",
                "stock_value_at_cost",
                "Categoria",
                "Valor a custo (R$)",
            )
        with chart_columns[1]:
            st.subheader("7. Produtos com menor estoque")
            cls._show_bar(
                analytics.lowest_stock(),
                "model",
                "stock_quantity",
                "Modelo",
                "Unidades",
                horizontal=True,
                sort_order="ascending",
                color_field="brand",
                height=analytics.model_chart_height,
            )

        st.subheader("12. Estoque por marca e categoria")
        st.altair_chart(
            DashboardCharts.stacked_stock(analytics.stock_by_brand_category()),
            width="stretch",
        )
        cls._render_low_stock(analytics.products, low_stock_limit)

    @staticmethod
    def _show_bar(
        data: pd.DataFrame,
        category_field: str,
        value_field: str,
        category_title: str,
        value_title: str,
        *,
        horizontal: bool = False,
        sort_order: str = "descending",
        color_field: str | None = None,
        height: int = 320,
    ) -> None:
        chart = DashboardCharts.bar(
            data,
            category_field,
            value_field,
            category_title,
            value_title,
            horizontal=horizontal,
            sort_order=sort_order,
            color_field=color_field,
            height=height,
        )
        st.altair_chart(chart, width="stretch")

    @staticmethod
    def _render_low_stock(products: pd.DataFrame, limit: int) -> None:
        low_stock = products[products["stock_quantity"] <= limit]
        st.subheader(f"Produtos com estoque baixo (até {limit} unidades)")
        if low_stock.empty:
            st.success("Nenhum produto abaixo do limite de estoque selecionado.")
            return

        st.dataframe(
            low_stock[["model", "brand", "category", "stock_quantity"]].rename(
                columns={
                    "model": "Modelo",
                    "brand": "Marca",
                    "category": "Categoria",
                    "stock_quantity": "Unidades",
                }
            ),
            hide_index=True,
            width="stretch",
        )
