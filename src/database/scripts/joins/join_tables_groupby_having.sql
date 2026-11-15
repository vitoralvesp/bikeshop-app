SELECT
    b.name AS brand,
    COUNT(p.product_id) AS number_of_models,
    SUM(p.stock_quantity) AS total_units_in_stock
FROM public.brands AS b
INNER JOIN public.products AS p
    ON b.brand_id = p.brand_id
WHERE p.is_active = TRUE
GROUP BY b.name
HAVING SUM(p.stock_quantity) > 10
ORDER BY total_units_in_stock DESC;