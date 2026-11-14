import pandas as pd
import streamlit as st

from src.dashboard.catalog import CatalogAnalytics
from src.dashboard.charts import DashboardCharts


class CatalogView:
    @classmethod
    def render(cls, analytics: CatalogAnalytics) -> None:
        chart_columns = st.columns(2)
        with chart_columns[0]:
            st.subheader("2. Preço médio por categoria")
            cls._show_bar(
                analytics.average_sale_by_category(),
                "category",
                "average_sale_price",
                "Categoria",
                "Preço médio (R$)",
            )
        with chart_columns[1]:
            st.subheader("3. Modelos por marca")
            cls._show_bar(
                analytics.models_by_brand(),
                "brand",
                "model_count",
                "Marca",
                "Modelos",
            )

        chart_columns = st.columns(2)
        with chart_columns[0]:
            st.subheader("4. Modelos por categoria")
            cls._show_bar(
                analytics.models_by_category(),
                "category",
                "model_count",
                "Categoria",
                "Modelos",
            )
        with chart_columns[1]:
            st.subheader("8. Preço de venda por modelo")
            cls._show_bar(
                analytics.price_by_model(),
                "model",
                "sale_price",
                "Modelo",
                "Preço de venda (R$)",
                horizontal=True,
                color_field="brand",
                height=analytics.model_chart_height,
            )

        st.subheader("11. Distribuição de preços")
        st.altair_chart(
            DashboardCharts.price_histogram(analytics.products),
            width="stretch",
        )

    @staticmethod
    def _show_bar(
        data: pd.DataFrame,
        category_field: str,
        value_field: str,
        category_title: str,
        value_title: str,
        *,
        horizontal: bool = False,
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
            color_field=color_field,
            height=height,
        )
        st.altair_chart(chart, width="stretch")
