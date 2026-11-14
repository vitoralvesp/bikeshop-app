import os

import streamlit as st


VIEW_NAME = "bikeshop_catalog_view"


def get_setting(name: str) -> str | None:
    value = os.getenv(name)
    if value:
        return value

    try:
        return st.secrets[name]
    except (KeyError, FileNotFoundError):
        return None


def format_brl(value: float) -> str:
    formatted = f"{value:,.2f}".translate(str.maketrans({",": ".", ".": ","}))
    return f"R$ {formatted}"
