IF OBJECT_ID('beta.country', 'U') IS NOT NULL
    DROP TABLE beta.country;
GO

CREATE TABLE beta.country (
    country_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL
);


IF OBJECT_ID('beta.botanist', 'U') IS NOT NULL
    DROP TABLE beta.botanist;
GO

CREATE TABLE beta.botanist (
    botanist_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    botanist_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(100)
);

IF OBJECT_ID('beta.plant', 'U') IS NOT NULL
    DROP TABLE beta.plant;
GO


CREATE TABLE beta.plant (
    plant_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    common_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255)
);


IF OBJECT_ID('beta.plant_image', 'U') IS NOT NULL
    DROP TABLE beta.plant_image;
GO


CREATE TABLE beta.plant_image (
    image_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    licence BIGINT,
    licence_name VARCHAR(255),
    licence_url VARCHAR(255),
    thumbnail VARCHAR(500)
);


IF OBJECT_ID('beta.origin_location', 'U') IS NOT NULL
    DROP TABLE beta.origin_location;
GO

CREATE TABLE beta.origin_location (
    origin_location_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    origin_city_name VARCHAR(100) NOT NULL,
    country_id SMALLINT NOT NULL,
    longitude FLOAT,
    latitude FLOAT,
    CONSTRAINT fk_origin_country FOREIGN KEY (country_id) REFERENCES beta.country(country_id)
);


IF OBJECT_ID('beta.recording', 'U') IS NOT NULL
    DROP TABLE beta.recording;
GO


CREATE TABLE beta.recording (
    recording_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    plant_id SMALLINT NOT NULL,
    botanist_id SMALLINT NOT NULL,
    origin_location_id BIGINT NOT NULL,
    last_watered DATETIME,
    image_id SMALLINT,
    recording_taken DATETIME,
    soil_moisture FLOAT,
    temperature FLOAT,
    CONSTRAINT fk_recording_plant FOREIGN KEY (plant_id) REFERENCES beta.plant(plant_id),
    CONSTRAINT fk_recording_botanist FOREIGN KEY (botanist_id) REFERENCES beta.botanist(botanist_id),
    CONSTRAINT fk_recording_origin FOREIGN KEY (origin_location_id) REFERENCES beta.origin_location(origin_location_id),
    CONSTRAINT fk_recording_image FOREIGN KEY (image_id) REFERENCES beta.plant_image(image_id)
);

GO