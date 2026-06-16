CREATE TABLE prices (
    date DATE,
    price_usd_brent NUMERIC,
    price_usd_wti NUMERIC,
    PRIMARY KEY (date)
);

CREATE TABLE production (
    date DATE,
    country VARCHAR,
    production_kbd NUMERIC,
    PRIMARY KEY (date, country)
);

CREATE TABLE inventories (
    date DATE,
    location VARCHAR,
    stocks_kb NUMERIC,
    PRIMARY KEY (date, location)
);
