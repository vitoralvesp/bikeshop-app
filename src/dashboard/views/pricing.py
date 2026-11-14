import streamlit as st

from src.dashboard.catalog import CatalogAnalytics
from src.dashboard.charts import DashboardCharts


class PricingView:
    @classmethod
    def render(cls, analytics: CatalogAnalytics) -> None:
        st.subheader("9. Margem bruta por modelo")
        st.altair_chart(
            DashboardCharts.bar(
                analytics.margin_by_model(),
                "model",
                "gross_margin_percentage",
                "Modelo",
                "Margem bruta (%)",
                horizontal=True,
                color_field="brand",
                height=analytics.model_chart_height,
            ),
            width="stretch",
        )

        st.subheader("10. Preço de venda × estoque")
        st.altair_chart(
            DashboardCharts.price_stock_scatter(analytics.products),
            width="stretch",
        )
