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

CREATE TABLE recording (
    recording_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    plant_id SMALLINT NOT NULL,
    botanist_id SMALLINT NOT NULL,
    origin_location_id BIGINT NOT NULL,
    last_watered DATETIME,
    image_id BIGINT,
    recording_taken DATETIME,
    soil_moisture FLOAT,
    temperature FLOAT

    CONSTRAINT fk_recording_plant
        FOREIGN KEY (plant_id)
        REFERENCES plant(plant_id)
    
    CONSTRAINT fk_recording_botanist
        FOREIGN KEY (botanist_id)
        REFERENCES botanist(botanist_id)
    
    CONSTRAINT fk_recording_origin
        FOREIGN KEY (origin_location_id)
        REFERENCES origin_location(origin_location_id)
    
    CONSTRAINT fk_recording_image
        FOREIGN KEY (image_id)
        REFERENCES plant_image(image_id)
);
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

    CONSTRAINT fk_origin_country
        FOREIGN KEY (country_id)
        REFERENCES country(country_id)
);


CREATE TABLE botanist (
    botanist_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    botanist_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(100)
);


CREATE TABLE plant (
    plant_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    plant_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255)
);


CREATE TABLE plant_image (
    image_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    licence BIGINT,
    licence_name VARCHAR(255),
    licence_url VARCHAR(255),
    thumbnail VARCHAR(500)
);

GO