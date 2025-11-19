CREATE TABLE User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES User(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) UNIQUE,
    place_id CHAR(36) UNIQUE,
    FOREIGN KEY (user_id) REFERENCES User(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
);

CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Place_Amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
