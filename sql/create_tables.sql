DROP TABLE IF EXISTS person;

CREATE TABLE person (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    gender TEXT,
    email TEXT,
    nat VARCHAR(2),
    name_title VARCHAR(4),
    name_first TEXT,
    name_last TEXT,
    location_street_number INTEGER,
    location_street_name TEXT,
    location_city TEXT,
    location_state TEXT,
    location_country TEXT,
    location_postcode TEXT,
    location_coordinates_latitude REAL,
    location_coordinates_longitude REAL,
    location_timezone_offset INTEGER,
    location_timezone_description TEXT,
    dob_date TIMESTAMP,
    dob_age INTEGER,
    id_name TEXT,
    id_value TEXT,
    picture_large TEXT,
    picture_medium TEXT,
    picture_thumbnail TEXT
);