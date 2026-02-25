CREATE TABLE IF NOT EXISTS city (
    cityId SERIAL PRIMARY KEY,
    cityName VARCHAR(100),
    stateName VARCHAR(100),
    countryName VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE IF NOT EXISTS pollution (
    cityId INT,
    datetime TIMESTAMP,
    ts BIGINT,
    aqius INT,
    mainus VARCHAR(50),
    aqicn INT,
    maincn VARCHAR(50),
    PRIMARY KEY (cityId, datetime),
    FOREIGN KEY (cityId) REFERENCES city(cityId)
);