import httpx
import streamlit as st
from postgrest.exceptions import APIError

from src.dashboard.catalog import CatalogAnalytics, SupabaseCatalogRepository
from src.dashboard.settings import VIEW_NAME, get_setting
from src.dashboard.ui import DashboardUI


PAGE_TITLE = "BikeShop | Estoque"
PAGE_ICON = "🚲"
PAGE_LAYOUT = "wide"
DASHBOARD_TITLE = "BikeShop | Dashboard de Estoque"
DASHBOARD_CAPTION = "Visão do catálogo, disponibilidade e valor do estoque."
REFRESH_BUTTON_LABEL = "Atualizar dados"
SUPABASE_URL_SETTING = "SUPABASE_URL"
SUPABASE_KEY_SETTING = "SUPABASE_KEY"
CONFIGURATION_ERROR = (
    "Configure {url_setting} e {key_setting} nas variáveis de ambiente "
    "ou em .streamlit/secrets.toml para conectar ao Supabase."
)
CONNECTION_ERROR = (
    "Não foi possível carregar o catálogo do Supabase. "
    "Verifique a conexão, a view public.{view_name} e as permissões RLS. "
    "Detalhe: {error}"
)
EMPTY_CATALOG_WARNING = (
    "Nenhum produto foi retornado. Verifique se os scripts do catálogo "
    "foram executados e se a chave possui acesso de leitura pela RLS."
)
EMPTY_FILTERED_CATALOG_INFO = "Nenhum produto corresponde aos filtros selecionados."


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)
    st.title(DASHBOARD_TITLE)
    st.caption(DASHBOARD_CAPTION)

    if st.button(REFRESH_BUTTON_LABEL):
        SupabaseCatalogRepository.clear_cache()

    supabase_url = get_setting(SUPABASE_URL_SETTING)
    supabase_key = get_setting(SUPABASE_KEY_SETTING)
    if not supabase_url or not supabase_key:
        st.error(
            CONFIGURATION_ERROR.format(
                url_setting=SUPABASE_URL_SETTING,
                key_setting=SUPABASE_KEY_SETTING,
            )
        )
        return

    repository = SupabaseCatalogRepository(supabase_url, supabase_key)
    try:
        catalog = repository.load()
    except (APIError, httpx.HTTPError) as error:
        st.error(
            CONNECTION_ERROR.format(view_name=VIEW_NAME, error=error)
        )
        return

    if catalog.empty:
        st.warning(EMPTY_CATALOG_WARNING)
        return

    filtered_catalog, low_stock_limit = DashboardUI.render_filters(catalog)
    if filtered_catalog.empty:
        st.info(EMPTY_FILTERED_CATALOG_INFO)
        return

    DashboardUI.render(CatalogAnalytics(filtered_catalog), low_stock_limit)


if __name__ == "__main__":
    main()
