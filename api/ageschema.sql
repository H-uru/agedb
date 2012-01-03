CREATE TABLE ages (id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY, description varchar(255), creator INTEGER, fullname varchar(64), shortname varchar(32) UNIQUE);
CREATE TABLE files (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, timestamp TIMESTAMP, gamever DECIMAL(5,2), age MEDIUMINT FOREIGN KEY REFERENCES ages(id), status varchar(16), version varchar(32));

