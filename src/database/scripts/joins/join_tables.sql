SELECT
    p.product_id,
    p.model,
    b.name AS brand,
    p.sale_price,
    p.stock_quantity
FROM public.products AS p
INNER JOIN public.brands AS b
    ON p.brand_id = b.brand_id
ORDER BY b.name, p.model;