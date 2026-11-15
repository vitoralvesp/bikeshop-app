SELECT
    p.product_id,
    p.model,
    b.name AS brand,
    c.name AS category,
    p.sale_price
FROM public.products AS p
INNER JOIN public.brands AS b
    ON p.brand_id = b.brand_id
INNER JOIN public.categories AS c
    ON p.category_id = c.category_id
WHERE p.is_active = TRUE
  AND p.sale_price > (
      SELECT AVG(p2.sale_price)
      FROM public.products AS p2
      WHERE p2.category_id = p.category_id
        AND p2.is_active = TRUE
  )
ORDER BY c.name, p.sale_price DESC;