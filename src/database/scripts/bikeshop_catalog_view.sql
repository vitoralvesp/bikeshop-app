CREATE VIEW public.bikeshop_catalog_view
WITH (security_invoker = true)
AS
SELECT
    p.product_id,
    p.model,
    b.name AS brand,
    b.country_of_origin,
    c.name AS category,
    p.cost_price,
    p.sale_price,
    p.stock_quantity,
    p.is_active,

    p.cost_price * p.stock_quantity AS stock_value_at_cost,

    p.sale_price * p.stock_quantity AS stock_value_at_sale_price,

    p.sale_price - p.cost_price AS gross_profit_per_unit,

    ROUND(100.0 * (p.sale_price - p.cost_price) / NULLIF(p.sale_price, 0), 2) AS gross_margin_percentage

FROM public.products AS p
INNER JOIN public.brands AS b
    ON p.brand_id = b.brand_id
INNER JOIN public.categories AS c
    ON p.category_id = c.category_id;

COMMIT;