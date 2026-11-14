import altair as alt
import pandas as pd


class DashboardCharts:
    @staticmethod
    def bar(
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
    ) -> alt.Chart:
        sort = alt.SortField(field=value_field, order=sort_order)
        if horizontal:
            encodings = {
                "x": alt.X(f"{value_field}:Q", title=value_title),
                "y": alt.Y(
                    f"{category_field}:N",
                    title=category_title,
                    sort=sort,
                ),
            }
        else:
            encodings = {
                "x": alt.X(
                    f"{category_field}:N",
                    title=category_title,
                    sort=sort,
                    axis=alt.Axis(labelAngle=-35),
                ),
                "y": alt.Y(f"{value_field}:Q", title=value_title),
            }

        if color_field:
            encodings["color"] = alt.Color(f"{color_field}:N", title=color_field)

        encodings["tooltip"] = [
            alt.Tooltip(f"{category_field}:N", title=category_title),
            alt.Tooltip(f"{value_field}:Q", title=value_title, format=",.2f"),
        ]

        return alt.Chart(data).mark_bar().encode(**encodings).properties(height=height)

    @staticmethod
    def stacked_stock(data: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X("brand:N", title="Marca"),
                y=alt.Y("stock_quantity:Q", title="Unidades", stack="zero"),
                color=alt.Color("category:N", title="Categoria"),
                tooltip=[
                    alt.Tooltip("brand:N", title="Marca"),
                    alt.Tooltip("category:N", title="Categoria"),
                    alt.Tooltip("stock_quantity:Q", title="Unidades"),
                ],
            )
            .properties(height=350)
        )

    @staticmethod
    def price_histogram(data: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(
                    "sale_price:Q",
                    bin=alt.Bin(maxbins=10),
                    title="Faixa de Preço de Venda (R$)",
                ),
                y=alt.Y("count():Q", title="Modelos"),
                tooltip=[alt.Tooltip("count():Q", title="Modelos")],
            )
            .properties(height=350)
        )

    @staticmethod
    def price_stock_scatter(data: pd.DataFrame) -> alt.Chart:
        return (
            alt.Chart(data)
            .mark_circle(size=90, opacity=0.8)
            .encode(
                x=alt.X("sale_price:Q", title="Preço de Venda (R$)"),
                y=alt.Y("stock_quantity:Q", title="Unidades em estoque"),
                color=alt.Color("category:N", title="Categoria"),
                tooltip=[
                    alt.Tooltip("model:N", title="Modelo"),
                    alt.Tooltip(
                        "sale_price:Q",
                        title="Preço de Venda",
                        format=",.2f",
                    ),
                    alt.Tooltip("stock_quantity:Q", title="Unidades"),
                    alt.Tooltip("category:N", title="Categoria"),
                ],
            )
            .properties(height=400)
        )
