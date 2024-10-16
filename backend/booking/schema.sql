DROP TABLE IF EXISTS userprofile;
CREATE TABLE userprofile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    common_name TEXT NOT NULL,
    family_name TEXT NOT NULL,
    mail_address UNIQUE NOT NULL,
    tax_id TEXT UNIQUE NOT NULL,
    payment_method TEX
);

INSERT INTO userprofile (username, password, common_name, family_name, mail_address, tax_id, payment_method) VALUES
('mrossi', 'password01', 'Mario', 'Rossi', 'mario.rossi@example.com', 'ABC12345678', 'payplal'),
('lbianchi', 'password02', 'Luigi', 'Bianchi', 'luigi.bianchi@example.com', 'DEF23456789', 'paypal'),
('averdi', 'password03', 'Anna', 'Verdi', 'anna.verdi@example.com', 'GHI34567890', 'paypal'),
('sneri', 'password04', 'Sara', 'Neri', 'sara.neri@example.com', 'JKL45678901', 'paypal'),
('pgialli', 'password05', 'Paolo', 'Gialli', 'paolo.gialli@example.com', 'MNO56789012', 'paypal'),
('fmarroni', 'password06', 'Francesca', 'Marroni', 'francesca.marroni@example.com', 'PQR67890123', 'paypal'),
('gazzurri', 'password07', 'Giovanni', 'Azzurri', 'giovanni.azzurri@example.com', 'STU78901234', 'paypal'),
('lferri', 'password08', 'Luca', 'Ferri', 'luca.ferri@example.com', 'VWX89012345', 'paypal'),
('srubini', 'password09', 'Sofia', 'Rubini', 'sofia.rubini@example.com', 'YZA90123456', 'paypal'),
('eblu', 'password10', 'Elena', 'Blu', 'elena.blu@example.com', 'BCD01234567', 'paypal'),
('vviola', 'password11', 'Vittorio', 'Viola',' vittoviola@example.com', 'VVL01234567', 'paypal');


DROP TABLE IF EXISTS owner;
CREATE TABLE owner (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES userprofile (id)
);
INSERT INTO owner (user_id) VALUES
(1),
(2),
(3);

DROP TABLE IF EXISTS catalog;
CREATE TABLE catalog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_type TEXT UNIQUE NOT NULL,
    item_owner_id INTEGER NOT NULL, 
    item_location_id INTEGER NOT NULL,
    item_details TEXT NOT NULL,
    FOREIGN KEY (item_owner_id) REFERENCES owner (id)
    FOREIGN KEY (item_location_id) REFERENCES location (id)
);
INSERT INTO catalog (item_type, item_owner_id, item_location_id, item_details) VALUES
('car', 1, 2, '{ "brand": "Fiat", "model": "Panda", "year": 2020, "horsepower": 51, "emission": 95, "min_age": 18, "reg_id": "AB123CD" }'),
('car', 1, 2, '{ "brand": "Fiat", "model": "Punto", "year": 2018, "horsepower": 64, "emission": 95, "min_age": 18, "reg_id": "AB124CD" }'),
('car', 1, 2, '{ "brand": "Volkswagen", "model": "Golf", "year": 2019, "horsepower": 85, "emission": 110, "min_age": 18, "reg_id": "EF456GH" }'),
('car', 1, 2, '{ "brand": "Toyota", "model": "Yaris", "year": 2021, "horsepower": 67, "emission": 89, "min_age": 18, "reg_id": "IJ789KL" }'),
('car', 1, 2, '{ "brand": "Ford", "model": "Focus", "year": 2018, "horsepower": 92, "emission": 115, "min_age": 18, "reg_id": "MN012OP" }'),
('car', 1, 2, '{ "brand": "Renault", "model": "Clio", "year": 2020, "horsepower": 65, "emission": 97, "min_age": 18, "reg_id": "QR345ST" }'),
('car', 1, 2, '{ "brand": "BMW", "model": "Series 3", "year": 2017, "horsepower": 110, "emission": 125, "min_age": 21, "reg_id": "UV678WX" }'),
('car', 1, 2, '{ "brand": "Mercedes", "model": "C-Class", "year": 2019, "horsepower": 120, "emission": 130, "min_age": 21, "reg_id": "YZ901AB" }'),
('car', 1, 2, '{ "brand": "Audi", "model": "A3", "year": 2021, "horsepower": 100, "emission": 105, "min_age": 18, "reg_id": "CD234EF" }'),
('car', 1, 2, '{ "brand": "Peugeot", "model": "208", "year": 2020, "horsepower": 75, "emission": 98, "min_age": 18, "reg_id": "GH567IJ" }'),
('car', 1, 2, '{ "brand": "Tesla", "model": "Model 3", "year": 2022, "horsepower": 150, "emission": 0, "min_age": 21, "reg_id": "KL890MN" }');


DROP TABLE IF EXISTS booking_status;
CREATE TABLE booking_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT UNIQUE NOT NULL,
    description TEXT
) ;

DROP TABLE IF EXISTS location;
CREATE TABLE location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    country TEXT NOT NULL,
    state TEXT NOT NULL,
    city TEXT NOT NULL,
    address_line1 TEXT NOT NULL,
    address_line2 TEXT NOT NULL,
    zip TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userprofile (id)
);
INSERT INTO location (user_id, country, state, city, address_line1, address_line2, zip) VALUES
(1, 'Italy', 'Piemonte', 'Novara', 'Via XX Settembre, 34', 'Scala A, Piano 1', '28100'),
(1, 'Italy', 'Piemonte', 'Alessandria', 'Corso Roma, 12', 'Piano Terra', '15121'),
(1, 'Italy', 'Piemonte', 'Torino', 'Corso Vittorio Emanuele II, 8', 'Piano Terra', '10128'),
(2, 'Italy', 'Lazio', 'Roma', 'Via del Corso, 22', 'Interno 3', '00187'),
(3, 'Italy', 'Veneto', 'Venezia', 'Calle Larga XXII Marzo, 15', 'Piano 1', '30124'),
(4, 'Italy', 'Toscana', 'Firenze', 'Piazza della Signoria, 5', 'Appartamento B', '50122'),
(5, 'Italy', 'Campania', 'Napoli', 'Via Toledo, 50', 'Scala B, Piano 3', '80134'),
(6, 'Italy', 'Lombardia', 'Milano', 'Via Roma, 10', 'Scala A, Piano 2', '20121'),
(7, 'Italy', 'Sicilia', 'Palermo', 'Via Maqueda, 7', 'Interno 2', '90133'),
(8, 'Italy', 'Emilia-Romagna', 'Bologna', 'Via Indipendenza, 45', 'Scala C, Piano 4', '40121'),
(9, 'Italy', 'Liguria', 'Genova', 'Via Garibaldi, 12', 'Piano 1', '16124'),
(10, 'Italy', 'Puglia', 'Bari', 'Corso Cavour, 18', 'Appartamento A', '70121'),
(11, 'Italy', 'Sardegna', 'Cagliari', 'Via Roma, 3', 'Scala A, Piano 1', '09123');


DROP TABLE IF EXISTS booking;
CREATE TABLE booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    booked_item_id INTEGER NOT NULL,
    booking_start TIMESTAMP NOT NULL,
    booking_end TIMESTAMP NOT NULL,
    booking_status_id INTEGER NOT NULL,
    delivery_address_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userprofile (id),
    FOREIGN KEY (booked_item_id) REFERENCES catalog (id),
    FOREIGN KEY (booking_status_id) REFERENCES booking_status (id),
    FOREIGN KEY (delivery_address_id) REFERENCES location (id)
);