IF DB_ID('lmnh_plants') IS NOT NULL
BEGIN
    ALTER DATABASE lmnh_plants;
    DROP DATABASE lmnh_plants;
END;
GO

CREATE DATABASE lmnh_plants;
GO

USE lmnh_plants;
GO

CREATE TABLE country (
    country_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL
);


CREATE TABLE origin_location (
    origin_location_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    origin_city_name VARCHAR(100) NOT NULL,
    country_id SMALLINT NOT NULL,
    longitude FLOAT,
    latitude FLOAT
)