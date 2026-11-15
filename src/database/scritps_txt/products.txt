CREATE TABLE public.products (
    product_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    model VARCHAR(150) NOT NULL,
    brand_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    cost_price NUMERIC(10, 2) NOT NULL CHECK (cost_price >= 0),
    sale_price NUMERIC(10, 2) NOT NULL CHECK (sale_price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0
        CHECK (stock_quantity >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_product_brand
        FOREIGN KEY (brand_id)
        REFERENCES public.brands (brand_id),

    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id)
        REFERENCES public.categories (category_id),

    CONSTRAINT uq_product_brand_model
        UNIQUE (brand_id, model)
);

ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

INSERT INTO public.products (
    model,
    brand_id,
    category_id,
    cost_price,
    sale_price,
    stock_quantity
)
SELECT
    data.model,
    b.brand_id,
    c.category_id,
    data.cost_price,
    data.sale_price,
    data.stock_quantity
FROM (
    VALUES
        -- model, brand, category, cost, sale price, stock
        ('Oiz M-Team',          'Orbea',      'Mountain Bike', 33500.00, 45900.00, 3),
        ('Alma H30',            'Orbea',      'Mountain Bike',  6900.00,  9900.00, 8),
        ('Orca M30',            'Orbea',      'Road Bike',     16800.00, 22900.00, 5),
        ('Terra H30',           'Orbea',      'Gravel Bike',   11500.00, 15900.00, 4),
        ('Gain M20',            'Orbea',      'Electric Bike', 27000.00, 36900.00, 3),

        ('Big Nine 500',        'Merida',     'Mountain Bike',  6800.00,  9800.00, 12),
        ('Ninety-Six RC',       'Merida',     'Mountain Bike', 18000.00, 24900.00, 6),
        ('Scultura 400',        'Merida',     'Road Bike',      7200.00, 10500.00, 7),
        ('Silex 400',           'Merida',     'Gravel Bike',    8500.00, 11900.00, 5),
        ('eBig Nine 400',       'Merida',     'Electric Bike', 17500.00, 23900.00, 2),

        ('Scale 940',           'Scott',      'Mountain Bike', 10500.00, 14900.00, 7),
        ('Spark 970',           'Scott',      'Mountain Bike', 14500.00, 19900.00, 4),
        ('Addict RC 30',        'Scott',      'Road Bike',     25500.00, 34900.00, 5),
        ('Speedster Gravel 30', 'Scott',      'Gravel Bike',    8200.00, 11500.00, 6),
        ('Sub Active eRide',    'Scott',      'Electric Bike', 15000.00, 20900.00, 2),

        ('Rockhopper Comp',     'Specialized','Mountain Bike',  5200.00,  7500.00, 10),
        ('Epic World Cup',      'Specialized','Mountain Bike', 40000.00, 54900.00, 2),
        ('Tarmac SL7 Expert',   'Specialized','Road Bike',     33500.00, 45900.00, 3),
        ('Diverge E5',          'Specialized','Gravel Bike',    9000.00, 12900.00, 10),
        ('Turbo Vado 4.0',      'Specialized','Electric Bike', 22000.00, 29900.00, 1)
) AS data (
    model,
    brand,
    category,
    cost_price,
    sale_price,
    stock_quantity
)
JOIN public.brands AS b
    ON b.name = data.brand
JOIN public.categories AS c
    ON c.name = data.category;