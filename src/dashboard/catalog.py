import pandas as pd
import streamlit as st
from supabase import Client, create_client

from src.dashboard.settings import VIEW_NAME


@st.cache_data(ttl=300)
def _fetch_catalog(supabase_url: str, supabase_key: str) -> list[dict]:
    client: Client = create_client(supabase_url, supabase_key)
    response = client.table(VIEW_NAME).select("*").order("model").execute()
    return response.data


class SupabaseCatalogRepository:
    def __init__(self, supabase_url: str, supabase_key: str) -> None:
        self._supabase_url = supabase_url
        self._supabase_key = supabase_key

    def load(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(
            _fetch_catalog(self._supabase_url, self._supabase_key)
        )

    @staticmethod
    def clear_cache() -> None:
        _fetch_catalog.clear()


class CatalogAnalytics:
    def __init__(self, products: pd.DataFrame) -> None:
        self.products = products

    @property
    def model_count(self) -> int:
        return len(self.products)

    @property
    def unit_count(self) -> int:
        return int(self.products["stock_quantity"].sum())

    @property
    def potential_stock_value(self) -> float:
        return float(self.products["stock_value_at_sale_price"].sum())

    @property
    def model_chart_height(self) -> int:
        return max(320, min(720, self.model_count * 28))

    def stock_by_brand(self) -> pd.DataFrame:
        return self.products.groupby("brand", as_index=False)["stock_quantity"].sum()

    def average_sale_by_category(self) -> pd.DataFrame:
        return (
            self.products.groupby("category", as_index=False)["sale_price"]
            .mean()
            .rename(columns={"sale_price": "average_sale_price"})
        )

    def models_by_brand(self) -> pd.DataFrame:
        return (
            self.products.groupby("brand", as_index=False)["product_id"]
            .count()
            .rename(columns={"product_id": "model_count"})
        )

    def models_by_category(self) -> pd.DataFrame:
        return (
            self.products.groupby("category", as_index=False)["product_id"]
            .count()
            .rename(columns={"product_id": "model_count"})
        )

    def sale_value_by_brand(self) -> pd.DataFrame:
        return self.products.groupby("brand", as_index=False)[
            "stock_value_at_sale_price"
        ].sum()

    def cost_value_by_category(self) -> pd.DataFrame:
        return self.products.groupby("category", as_index=False)[
            "stock_value_at_cost"
        ].sum()

    def stock_by_brand_category(self) -> pd.DataFrame:
        return self.products.groupby(
            ["brand", "category"], as_index=False
        )["stock_quantity"].sum()

    def lowest_stock(self) -> pd.DataFrame:
        return self.products.sort_values(
            ["stock_quantity", "model"], ascending=[True, True]
        )

    def price_by_model(self) -> pd.DataFrame:
        return self.products.sort_values("sale_price", ascending=False)

    def margin_by_model(self) -> pd.DataFrame:
        return self.products.sort_values("gross_margin_percentage", ascending=False)
