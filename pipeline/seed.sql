CREATE TABLE cleaned_data (
    plant_id SMALLINT,
    plant_name VARCHAR(255),
    scientific_name VARCHAR(255),
    botanist_name VARCHAR(255),
    botanist_email TEXT,
    botanist_phone VARCHAR(255),
    origin_city VARCHAR(255),
    origin_country VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    license BIGINT,
    license_name VARCHAR(255),
    license_url TEXT,
    thumbnail TEXT
);

BULK INSERT cleaned_data
FROM 'C:pipeline/cleaned_data.csv'
WITH (
    FORMAT='CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    MAXERRORS = 10,
    ERRORFILE = 'C:pipeline\ImportErrors.csv'
);

INSERT INTO botanist (botanist_name, email, phone)
SELECT DISTINCT
    c.botanist_name,
    c.botanist_email,
    c.botanist_phone
FROM cleaned_data c 
WHERE NOT EXISTS (
    SELECT 1
    FROM botanist b 
    WHERE b.email = c.botanist_email
);

INSERT INTO plant (common_name, scientific_name)
SELECT DISTINCT
    c.plant_name,
    c.scientific_name
FROM cleaned_data c 
WHERE NOT EXISTS (
    SELECT 1
    FROM plant p
    WHERE p.scientific_name = c.scientific_name
);

INSERT INTO country (country_name)
SELECT DISTINCT
    c.country_name
FROM cleaned_data c 
WHERE NOT EXISTS (
    SELECT 1
    FROM country co 
    WHERE co.country_name = c.country_name
);

INSERT INTO origin_location (origin_city_name, longitude, latitude)
SELECT DISTINCT
    c.origin_city,
    c.longitude,
    c.latitude
FROM cleaned_data c 
WHERE NOT EXISTS (
    SELECT 1
    FROM origin_location ol 
    WHERE ol.longitude = c.longitude AND ol.latitude = c.latitude
);

--