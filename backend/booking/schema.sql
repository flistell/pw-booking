DROP TABLE IF EXISTS userprofile;
CREATE TABLE userprofile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    common_name TEXT NOT NULL,
    family_name TEXT NOT NULL,
    mail_address UNIQUE NOT NULL,
    tax_id TEXT UNIQUE NOT NULL,
    payment_method TEXT
);

INSERT INTO userprofile (username, password, common_name, family_name, mail_address, tax_id, payment_method) VALUES
('mrossi', 'password01', 'Mario', 'Rossi', 'mario.rossi@example.com', 'ABC12345678', 'paypal'),
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
    item_type TEXT NOT NULL,
    item_owner_id INTEGER NOT NULL, 
    item_location_id INTEGER NOT NULL,
    item_price_weight INTEGER NOT NULL,
    item_details TEXT NOT NULL,
    FOREIGN KEY (item_owner_id) REFERENCES owner (id)
    FOREIGN KEY (item_location_id) REFERENCES location (id)
);
INSERT INTO catalog (item_type, item_owner_id, item_location_id, item_price_weight, item_details) VALUES
('car', 1, 1, 90,
    '{ 
        "brand": "Fiat", "model": "Panda", "year": 2020, "horsepower": 51, "emission": 95, "min_age": 18, "reg_id": "AB123CD", "photo": "39962524-83c1-46d6-846e-a3f520f96ce0.webp","fuel_consumption": 5.2,
        "description": "Lorem ipsum odor amet, consectetuer adipiscing elit. Pretium vitae justo aptent nunc adipiscing suspendisse augue rhoncus ullamcorper. Finibus molestie eget accumsan libero lacus in eu. Ac placerat aliquet urna, urna lacinia fusce. Sociosqu imperdiet conubia imperdiet; lacinia integer ultricies. Pulvinar congue aptent non elit gravida volutpat dis ullamcorper. Magnis praesent imperdiet tincidunt lorem mollis tellus ipsum curae."
    }'),
('car', 1, 2, 90, 
    '{ 
        "brand": "Fiat", "model": "Punto", "year": 2018, "horsepower": 64, "emission": 95, "min_age": 18, "reg_id": "AB124CD", "photo": "931199af-d6ec-43a5-864c-76d76ca15443.webp",
        "description": "Nisl eleifend nunc in, luctus non efficitur. Justo sodales litora iaculis orci; et quam id. Suspendisse ultricies consectetur lacus vehicula consequat in ligula convallis. Suscipit risus conubia pretium magna; libero dapibus. Magna quisque ridiculus himenaeos euismod, at sapien tellus posuere. Inceptos hendrerit vivamus libero at vestibulum cursus laoreet dictumst. Vulputate duis libero efficitur sit sed euismod nullam. Etiam nec class cubilia aenean per nisl faucibus luctus.", 
        "fuel_consumption": 6.1
    }'),
('car', 2, 4, 110, 
    '{ "brand": "Volkswagen", "model": "Golf", "year": 2019, "horsepower": 85, "emission": 110, "min_age": 18, "reg_id": "EF456GH", "photo": "9144947d-46bd-4178-8ee6-1d83e4944697.webp",
        "description": "Varius augue placerat integer mollis a malesuada, dictumst tortor amet. Nunc ex cursus dolor purus netus turpis pharetra nisi. Scelerisque suscipit nisi iaculis neque sapien morbi. Suspendisse ullamcorper lobortis lobortis tempor fermentum fames vestibulum. Mollis phasellus aliquet etiam velit malesuada condimentum per. Tincidunt sodales amet in feugiat erat molestie parturient taciti. Molestie fringilla imperdiet libero nibh ornare. Tincidunt id et augue nunc scelerisque rutrum.",
        "fuel_consumption": 6.1
    }'),
('car', 3, 5, 80,
    '{ "brand": "Toyota", "model": "Yaris", "year": 2021, "horsepower": 67, "emission": 89, "min_age": 18, "reg_id": "IJ789KL", "photo": "07f8b186-951e-41b1-9c18-7a6f7406ebea.webp", 
        "description": "Pellentesque molestie eleifend nisl sollicitudin gravida sollicitudin eleifend faucibus faucibus. Interdum est tristique lorem; nec vehicula erat fames. Pellentesque accumsan elementum duis taciti scelerisque integer erat ad etiam! Nam est augue fames sed nostra integer leo per praesent. Tempus lacinia per proin inceptos semper tempor. Dapibus efficitur efficitur lectus ut; quisque nascetur lectus vehicula. Purus venenatis at tempus posuere ipsum convallis. Amet maximus volutpat cursus ornare neque aliquam luctus mauris. Posuere amet dui duis maximus vestibulum primis.",
        "fuel_consumption": 4.8 
    }'),
('car', 3, 5, 110,
    '{ "brand": "Ford", "model": "Focus", "year": 2018, "horsepower": 92, "emission": 115, "min_age": 18, "reg_id": "MN012OP", "photo": "a548c786-94b9-4983-8052-da220c77e787.webp",
        "description": "Tristique magna justo sollicitudin torquent penatibus malesuada nibh ipsum. Dis varius finibus aliquet ex est elementum placerat enim. Netus venenatis viverra velit cursus consectetur imperdiet. Pharetra ultricies urna curae etiam dictumst, nec sollicitudin. Fusce velit accumsan ligula justo urna mollis. Phasellus cubilia egestas ligula, purus tempus varius purus. Class litora blandit odio laoreet mollis.",
        "fuel_consumption": 5.6
    }'),
('car', 3, 5, 90,
    '{ "brand": "Renault", "model": "Clio", "year": 2020, "horsepower": 65, "emission": 97, "min_age": 18, "reg_id": "QR345ST", "photo": "4b831f1f-cece-4c07-a654-a66bde1c217d.webp", 
        "description": "In maximus sed felis; mus eleifend himenaeos integer himenaeos. Orci nullam pellentesque ante ante penatibus gravida urna. Posuere vulputate sodales ante ac imperdiet. Maximus hendrerit vivamus nam venenatis sodales auctor porta nulla. Netus a augue eu nec risus vitae habitant duis. Sociosqu aliquam vehicula mattis ut libero cubilia. Enim volutpat in sapien morbi luctus mattis nisl scelerisque euismod. Ullamcorper hendrerit enim cursus pharetra class phasellus eleifend.",
       "fuel_consumption": 5.0 
    }'),
('car', 3, 5, 120,
    '{ "brand": "BMW", "model": "Series 3", "year": 2017, "horsepower": 110, "emission": 125, "min_age": 21, "reg_id": "UV678WX", "photo": "88abd4c6-8996-4c7e-bc06-96076792f9d1.webp",
        "description": "Lorem ipsum odor amet, consectetuer adipiscing elit. Pretium vitae justo aptent nunc adipiscing suspendisse augue rhoncus ullamcorper. Finibus molestie eget accumsan libero lacus in eu. Ac placerat aliquet urna, urna lacinia fusce. Sociosqu imperdiet conubia imperdiet; lacinia integer ultricies. Pulvinar congue aptent non elit gravida volutpat dis ullamcorper. Magnis praesent imperdiet tincidunt lorem mollis tellus ipsum curae.",
        "fuel_consumption": 6.7
    }'),
('car', 2, 4, 130,
    '{ "brand": "Mercedes", "model": "C-Class", "year": 2019, "horsepower": 120, "emission": 130, "min_age": 21, "reg_id": "YZ901AB", "photo": "4ff860bf-24a1-491b-8d62-b9139cf4a21a.webp",
        "description": "Nisl eleifend nunc in, luctus non efficitur. Justo sodales litora iaculis orci; et quam id. Suspendisse ultricies consectetur lacus vehicula consequat in ligula convallis. Suscipit risus conubia pretium magna; libero dapibus. Magna quisque ridiculus himenaeos euismod, at sapien tellus posuere. Inceptos hendrerit vivamus libero at vestibulum cursus laoreet dictumst. Vulputate duis libero efficitur sit sed euismod nullam. Etiam nec class cubilia aenean per nisl faucibus luctus.",
        "fuel_consumption": 6.7
    }'),
('car', 1, 1, 100,
    '{ "brand": "Audi", "model": "A3", "year": 2021, "horsepower": 100, "emission": 105, "min_age": 18, "reg_id": "CD234EF", "photo": "d1c6f41a-62b1-4098-b106-29c3f6591506.webp",
        "description": "Varius augue placerat integer mollis a malesuada, dictumst tortor amet. Nunc ex cursus dolor purus netus turpis pharetra nisi. Scelerisque suscipit nisi iaculis neque sapien morbi. Suspendisse ullamcorper lobortis lobortis tempor fermentum fames vestibulum. Mollis phasellus aliquet etiam velit malesuada condimentum per. Tincidunt sodales amet in feugiat erat molestie parturient taciti. Molestie fringilla imperdiet libero nibh ornare. Tincidunt id et augue nunc scelerisque rutrum.",
       "fuel_consumption": 5.4 
    }'),
('car', 1, 2, 90,
    '{ "brand": "Peugeot", "model": "208", "year": 2020, "horsepower": 75, "emission": 98, "min_age": 18, "reg_id": "GH567IJ", "photo": "32351763-4475-4f64-941b-c47e28a9c1f6.webp",
        "description": "Pellentesque molestie eleifend nisl sollicitudin gravida sollicitudin eleifend faucibus faucibus. Interdum est tristique lorem; nec vehicula erat fames. Pellentesque accumsan elementum duis taciti scelerisque integer erat ad etiam! Nam est augue fames sed nostra integer leo per praesent. Tempus lacinia per proin inceptos semper tempor. Dapibus efficitur efficitur lectus ut; quisque nascetur lectus vehicula. Purus venenatis at tempus posuere ipsum convallis. Amet maximus volutpat cursus ornare neque aliquam luctus mauris. Posuere amet dui duis maximus vestibulum primis.",
       "fuel_consumption": 5.1 
    }'),
('car', 1, 3, 50,
    '{ "brand": "Tesla", "model": "Model 3", "year": 2022, "horsepower": 150, "emission": 0, "min_age": 21, "reg_id": "KL890MN", "photo": "bc67f176-45a1-4c1d-ad66-72b0928338c4.webp",
        "description": "Tristique magna justo sollicitudin torquent penatibus malesuada nibh ipsum. Dis varius finibus aliquet ex est elementum placerat enim. Netus venenatis viverra velit cursus consectetur imperdiet. Pharetra ultricies urna curae etiam dictumst, nec sollicitudin. Fusce velit accumsan ligula justo urna mollis. Phasellus cubilia egestas ligula, purus tempus varius purus. Class litora blandit odio laoreet mollis.",
        "fuel_consumption": 0.0
        }');


-- DROP TABLE IF EXISTS booking_status;
-- CREATE TABLE booking_status (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     status TEXT UNIQUE NOT NULL,
--     description TEXT
-- ) ;

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
(1, 'Italia', 'Piemonte', 'Novara', 'Via XX Settembre, 34', 'Scala A, Piano 1', '28100'),
(1, 'Italia', 'Piemonte', 'Alessandria', 'Corso Roma, 12', 'Piano Terra', '15121'),
(1, 'Italia', 'Piemonte', 'Torino', 'Corso Vittorio Emanuele II, 8', 'Piano Terra', '10128'),
(2, 'Italia', 'Lazio', 'Roma', 'Via del Corso, 22', 'Interno 3', '00187'),
(3, 'Italia', 'Veneto', 'Venezia', 'Calle Larga XXII Marzo, 15', 'Piano 1', '30124'),
(4, 'Italia', 'Toscana', 'Firenze', 'Piazza della Signoria, 5', 'Appartamento B', '50122'),
(5, 'Italia', 'Campania', 'Napoli', 'Via Toledo, 50', 'Scala B, Piano 3', '80134'),
(6, 'Italia', 'Lombardia', 'Milano', 'Via Roma, 10', 'Scala A, Piano 2', '20121'),
(7, 'Italia', 'Sicilia', 'Palermo', 'Via Maqueda, 7', 'Interno 2', '90133'),
(8, 'Italia', 'Emilia-Romagna', 'Bologna', 'Via Indipendenza, 45', 'Scala C, Piano 4', '40121'),
(9, 'Italia', 'Liguria', 'Genova', 'Via Garibaldi, 12', 'Piano 1', '16124'),
(10, 'Italia', 'Puglia', 'Bari', 'Corso Cavour, 18', 'Appartamento A', '70121'),
(11, 'Italia', 'Sardegna', 'Cagliari', 'Via Roma, 3', 'Scala A, Piano 1', '09123');


DROP TABLE IF EXISTS booking;
CREATE TABLE booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    booked_item_id INTEGER NOT NULL,
    booking_start DATETIME NOT NULL,
    booking_end DATETIME NOT NULL,
    booking_status TEXT NOT NULL,
    delivery_address_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userprofile (id),
    FOREIGN KEY (booked_item_id) REFERENCES catalog (id),
    FOREIGN KEY (delivery_address_id) REFERENCES location (id)
);