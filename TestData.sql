SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- DataBase: AirTicketReservationSystem
--

-- --------------------------------------------------------

--
-- Create Table: `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('CEAir'),
('Lufthansa'),
('AirChina'),
('Delta'),
('United'),
('AmericanAirlines'),
('BritishAirways'),
('Emirates');

-- --------------------------------------------------------

--
-- Create Table: `airline_staff`
--

CREATE TABLE `airline_staff` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `airline_staff`
--

INSERT INTO airline_staff 
(username, password, first_name, last_name, date_of_birth, airline_name) VALUES

-- ===== CEAir =====
('ce_admin@ceair.com', 'a0cf0de477f03ca38ae4568115907412', 'Chen', 'Liang', '1985-02-11', 'CEAir'),
('ce_ops@ceair.com',   'a0cf0de477f03ca38ae4568115907412', 'Mei', 'Zhang', '1993-07-21', 'CEAir'),
('qw2440@nyu.edu', 'a0cf0de477f03ca38ae4568115907412', 'Richael', 'Richter', '2004-10-28', 'CEAir'),

-- ===== Lufthansa =====
('lh_admin@lufthansa.com', 'a0cf0de477f03ca38ae4568115907412', 'Hans', 'Müller', '1978-11-14', 'Lufthansa'),
('lh_ops@lufthansa.com',   'a0cf0de477f03ca38ae4568115907412', 'Klara', 'Weber', '1992-03-09', 'Lufthansa'),
('rr@lufthansa.com', 'a0cf0de477f03ca38ae4568115907412', 'Richard', 'Richter', '2001-04-20', 'Lufthansa'),
('ae@lufthansa.com', 'a0cf0de477f03ca38ae4568115907412', 'Albert', 'Einstein', '1980-03-01', 'Lufthansa'),

-- ===== AirChina =====
('ac_admin@airchina.com', 'a0cf0de477f03ca38ae4568115907412', 'Wei',  'Zhao',  '1983-06-04', 'AirChina'),
('ac_ops@airchina.com',   'a0cf0de477f03ca38ae4568115907412', 'Ling', 'Sun',   '1991-09-23', 'AirChina'),

-- ===== Delta =====
('dl_admin@delta.com', 'a0cf0de477f03ca38ae4568115907412', 'John', 'Anderson', '1986-12-08', 'Delta'),
('dl_ops@delta.com',   'a0cf0de477f03ca38ae4568115907412', 'Emily', 'Brown',    '1994-04-18', 'Delta'),

-- ===== United =====
('ua_admin@united.com', 'a0cf0de477f03ca38ae4568115907412', 'Carlos', 'Martinez', '1982-05-19', 'United'),
('ua_ops@united.com',   'a0cf0de477f03ca38ae4568115907412', 'Maria',  'Lopez',     '1990-10-05', 'United'),

-- ===== American Airlines =====
('aa_admin@aa.com', 'a0cf0de477f03ca38ae4568115907412', 'James', 'Walker',  '1984-03-07', 'AmericanAirlines'),
('aa_ops@aa.com',   'a0cf0de477f03ca38ae4568115907412', 'Sophia','Green',   '1996-11-12', 'AmericanAirlines'),

-- ===== British Airways =====
('ba_admin@ba.com', 'a0cf0de477f03ca38ae4568115907412', 'Oliver', 'Smith',   '1979-08-30', 'BritishAirways'),
('ba_ops@ba.com',   'a0cf0de477f03ca38ae4568115907412', 'Amelia', 'Clarke',  '1993-02-14', 'BritishAirways'),

-- ===== Emirates =====
('ek_admin@emirates.com', 'a0cf0de477f03ca38ae4568115907412', 'Omar', 'Hassan',   '1981-07-19', 'Emirates'),
('ek_ops@emirates.com',   'a0cf0de477f03ca38ae4568115907412', 'Fatima','Ali',     '1995-09-27', 'Emirates');


-- --------------------------------------------------------

--
-- Create Table: `airplane`
--

CREATE TABLE `airplane` (
  `airline_name` varchar(50) NOT NULL,
  `airplane_id` int(11) NOT NULL,
  `seats` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_id`, `seats`) VALUES
-- CEAir
('CEAir', 1, 300),
('CEAir', 1234, 200),

-- Lufthansa
('Lufthansa', 101, 250),
('Lufthansa', 309, 50),
('Lufthansa', 888, 299),
('Lufthansa', 909, 1),

-- AirChina
('AirChina', 1, 250),
('AirChina', 2, 300),

-- Delta
('Delta', 1, 220),
('Delta', 2, 260),

-- United
('United', 1, 240),
('United', 2, 280),

-- American Airlines
('AmericanAirlines', 1, 230),
('AmericanAirlines', 2, 270),

-- British Airways
('BritishAirways', 1, 250),
('BritishAirways', 2, 310),

-- Emirates
('Emirates', 1, 300),
('Emirates', 2, 350);

-- --------------------------------------------------------

--
-- Create Table: `airport`
--

CREATE TABLE `airport` (
  `airport_name` varchar(50) NOT NULL,
  `airport_city` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

ALTER TABLE `airport`
  ADD PRIMARY KEY (`airport_name`);

--
-- Insert Data: `airport`
--

INSERT INTO airport (airport_name, airport_city) VALUES
('BER', 'Berlin'),
('DUS', 'Duesseldorf'),
('FRA', 'Frankfurt'),
('MUC', 'Munich'),
('PEK', 'Beijing'),
('PVG', 'Shanghai'),
('TXL', 'Berlin'),
('ORD', 'Chicago'),
('MDW', 'Chicago'),
('SHA', 'Shanghai'),
('TFU', 'Chengdu'),
('CTU', 'Chengdu'),
('PKX', 'Beijing'),
('JFK', 'New York'),
('LGA', 'New York');

--
-- Create Table: `city_airport_map`
--

CREATE TABLE `city_airport_map` (
    `city_alias` VARCHAR(50) NOT NULL,
    `airport_name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`city_alias`, `airport_name`),
    FOREIGN KEY (`airport_name`) REFERENCES `airport` (`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;


--
-- Insert Data: `city_airport_map`
--

INSERT INTO city_airport_map VALUES
-- Berlin
('Berlin', 'BER'),
('Berlin', 'TXL'),

-- Dusseldorf
('Dusseldorf', 'DUS'),
('Duesseldorf', 'DUS'),

-- Frankfurt
('Frankfurt', 'FRA'),

-- Munich (no umlaut, safe for latin1)
('Munich', 'MUC'),
('Munchen', 'MUC'),

-- Chicago
('Chicago', 'ORD'),
('Chicago', 'MDW'),
('CHI', 'ORD'),
('CHI', 'MDW'),

-- New York
('New York', 'JFK'),
('New York', 'LGA'),
('NYC', 'JFK'),
('NYC', 'LGA'),
('NY',  'JFK'),
('NY',  'LGA'),

-- Shanghai
('Shanghai', 'PVG'),
('Shanghai', 'SHA'),
('SH', 'PVG'),
('SH', 'SHA'),

-- Chengdu
('Chengdu', 'TFU'),
('Chengdu', 'CTU'),
('CD', 'TFU'),
('CD', 'CTU'),

-- Beijing
('Beijing', 'PEK'),
('Beijing', 'PKX'),
('BJ', 'PEK'),
('BJ', 'PKX');

-- --------------------------------------------------------

--
-- Create Table: `booking_agent`
--

CREATE TABLE `booking_agent` (
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `booking_agent_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `booking_agent`
--

INSERT INTO `booking_agent` (`email`, `password`, `booking_agent_id`) VALUES
('rebecca@nyu.edu',       'a0cf0de477f03ca38ae4568115907412', 1),
('agent.john@example.com','a0cf0de477f03ca38ae4568115907412', 2),
('lisa.broker@travel.com','a0cf0de477f03ca38ae4568115907412', 3),
('michael.sales@agency.org','a0cf0de477f03ca38ae4568115907412', 4),
('anna.reservations@flynow.com','a0cf0de477f03ca38ae4568115907412', 5),
('kevin.agent@tickets.net','a0cf0de477f03ca38ae4568115907412', 6);

-- --------------------------------------------------------

--
-- Create Table: `booking_agent_work_for`
--

CREATE TABLE `booking_agent_work_for` (
  `email` varchar(50) NOT NULL,
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `booking_agent_work_for`
--
INSERT INTO booking_agent_work_for (email, airline_name) VALUES
-- Agent 1: rebecca
('rebecca@nyu.edu', 'CEAir'),
('rebecca@nyu.edu', 'Lufthansa'),
('rebecca@nyu.edu', 'AirChina'),
('rebecca@nyu.edu', 'Delta'),

-- Agent 2: John
('agent.john@example.com', 'CEAir'),
('agent.john@example.com', 'United'),

-- Agent 3: Lisa
('lisa.broker@travel.com', 'Lufthansa'),
('lisa.broker@travel.com', 'AmericanAirlines'),
('lisa.broker@travel.com', 'BritishAirways'),

-- Agent 4: Michael
('michael.sales@agency.org', 'Lufthansa'),
('michael.sales@agency.org', 'Emirates'),

-- Agent 5: Anna
('anna.reservations@flynow.com', 'CEAir'),
('anna.reservations@flynow.com', 'AirChina'),
('anna.reservations@flynow.com', 'BritishAirways'),

-- Agent 6: Kevin
('kevin.agent@tickets.net', 'CEAir'),
('kevin.agent@tickets.net', 'United'),
('kevin.agent@tickets.net', 'Emirates');

-- --------------------------------------------------------

--
-- Create Table: `customer`
--

CREATE TABLE `customer` (
  `email` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `building_number` varchar(30) NOT NULL,
  `street` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `phone_number` int(11) NOT NULL,
  `passport_number` varchar(30) NOT NULL,
  `passport_expiration` date NOT NULL,
  `passport_country` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `customer`
--

INSERT INTO `customer` 
(`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, 
 `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`)
VALUES
('jac32@nyu.edu',      'Alex Johnson',  'a0cf0de477f03ca38ae4568115907412', '1',  'Downing Street',     'London',   'UK',     12345, 'EM7200212',   '2035-05-01', 'UK',     '1984-04-10'),
('ml9007@nyu.edu',     'Adelyn Li',    'a0cf0de477f03ca38ae4568115907412', '8',  'West Gaoqing Road',  'Shanghai', 'China',  12121, 'EM76543321',  '2055-05-10', 'China',  '2005-04-16'),
('qw2440@nyu.edu',     'Qiuyi Wang',   'a0cf0de477f03ca38ae4568115907412', '6',  'HuoXiang Road',      'Shanghai', 'China',  12345, 'EM1234567',   '2040-12-04', 'China',  '2004-10-28'),
('sarah.jones@example.com',  'Sarah Jones',      'a0cf0de477f03ca38ae4568115907412', '22', 'Maple Street',      'New York',    'USA',    3478901234, 'US99887766', '2032-11-20', 'USA',    '1990-07-14'),
('michael.chen@outlook.com', 'Michael Chen',     'a0cf0de477f03ca38ae4568115907412', '55', '2nd Avenue',       'Beijing',     'China',  13855667788,'CN55443322', '2042-03-12', 'China',  '1995-01-08'),
('emma.wilson@gmail.com',    'Emma Wilson',      'a0cf0de477f03ca38ae4568115907412', '10', 'Riverbank Road',   'Sydney',      'Australia', 612443355, 'AU33445566', '2038-09-01', 'Australia','1988-12-05'),
('hassan.ali@protonmail.com','Hassan Ali',       'a0cf0de477f03ca38ae4568115907412', '41', 'King Faisal St',   'Riyadh',      'Saudi Arabia', 501223344, 'SA22113344','2031-01-17','Saudi Arabia','1982-06-11'),
('lucas.martin@gmail.com',   'Lucas Martin',     'a0cf0de477f03ca38ae4568115907412', '82', 'Rue de Lyon',      'Paris',       'France',  33155667788,'FR99882211', '2044-06-15','France', '1993-04-23'),
('sofia.romero@hotmail.com', 'Sofia Romero',     'a0cf0de477f03ca38ae4568115907412', '19', 'Calle Mayor',      'Madrid',      'Spain',   34911223344,'ES44332211', '2037-10-07','Spain',  '1997-11-29'),
('kevin.brown@yahoo.com',    'Kevin Brown',      'a0cf0de477f03ca38ae4568115907412', '77', 'Pine Street',      'Toronto',     'Canada',  16478889900,'CA11223344', '2041-12-25','Canada', '1985-03-16'),
('yuki.tanaka@gmail.com',    'Yuki Tanaka',      'a0cf0de477f03ca38ae4568115907412', '13', 'Shibuya Crossing', 'Tokyo',       'Japan',   81344557799,'JP55664433', '2039-08-18','Japan',  '1998-02-02');

-- --------------------------------------------------------

--
-- Create Table: `flight`
--

CREATE TABLE `flight` (
  `airline_name` varchar(50) NOT NULL,
  `flight_num` int(11) NOT NULL,
  `departure_airport` varchar(50) NOT NULL,
  `departure_time` datetime NOT NULL,
  `arrival_airport` varchar(50) NOT NULL,
  `arrival_time` datetime NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `status` varchar(50) NOT NULL,
  `airplane_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `flight`
--

INSERT INTO flight 
(airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id)
VALUES
-- ===== CEAir =====
('CEAir', 2001, 'PVG', '2025-07-02 09:00:00', 'SHA', '2025-07-02 10:00:00', 300, 'upcoming', 1),
('CEAir', 2002, 'PVG', '2025-09-15 13:30:00', 'PKX', '2025-09-15 17:10:00', 1200, 'upcoming', 1234),
('CEAir', 2003, 'SHA', '2025-11-01 06:45:00', 'FRA', '2025-11-01 17:00:00', 5200, 'upcoming', 1234),
('CEAir', 2004, 'PEK', '2025-12-20 21:10:00', 'PVG', '2025-12-20 23:40:00', 600, 'delayed', 1),
('CEAir', 129, 'PVG', '2025-06-13 00:05:00', 'FRA', '2025-06-13 12:05:00', 5050, 'upcoming', 1234),
('CEAir', 1234, 'PVG', '2025-05-10 10:00:00', 'PEK', '2025-05-10 12:30:00', 800, 'upcoming', 1),

-- ===== Lufthansa =====
('Lufthansa', 321, 'PVG', '2025-07-11 10:00:00', 'MUC', '2025-07-11 22:00:00', 15000, 'upcoming', 909),
('Lufthansa', 510, 'PVG', '2025-08-13 15:00:00', 'FRA', '2025-08-13 20:05:00', 4999, 'upcoming', 101),
('Lufthansa', 517, 'FRA', '2025-05-17 07:45:00', 'BER', '2025-05-17 09:45:00', 400, 'upcoming', 888),
('Lufthansa', 525, 'MUC', '2025-05-13 08:30:00', 'FRA', '2025-05-13 09:45:00', 450, 'delayed', 101),
('Lufthansa', 902, 'BER', '2025-06-28 14:30:00', 'PVG', '2025-06-29 15:30:00', 7500, 'cancelled', 888),

-- ===== AirChina =====
('AirChina', 3001, 'PEK', '2025-05-20 08:00:00', 'SHA', '2025-05-20 10:10:00', 800, 'upcoming', 1),
('AirChina', 3002, 'CTU', '2025-07-05 14:20:00', 'PEK', '2025-07-05 17:10:00', 900, 'upcoming', 1),
('AirChina', 3003, 'PEK', '2025-10-11 09:30:00', 'PVG', '2025-10-11 12:00:00', 780, 'upcoming', 1),

-- ===== Delta =====
('Delta', 4001, 'JFK', '2025-06-10 07:30:00', 'LGA', '2025-06-10 08:00:00', 150, 'upcoming', 1),
('Delta', 4002, 'JFK', '2025-08-03 11:00:00', 'ORD', '2025-08-03 12:50:00', 350, 'on-time', 1),
('Delta', 4003, 'ORD', '2025-11-27 18:40:00', 'FRA', '2025-11-28 08:50:00', 3200, 'upcoming', 1),

-- ===== United =====
('United', 5001, 'LGA', '2025-05-18 13:05:00', 'ORD', '2025-05-18 14:55:00', 280, 'upcoming', 1),
('United', 5002, 'ORD', '2025-10-08 16:10:00', 'MUC', '2025-10-09 06:10:00', 4500, 'upcoming', 1),

-- ===== American Airlines =====
('AmericanAirlines', 6001, 'JFK', '2025-09-09 09:25:00', 'BER', '2025-09-09 22:30:00', 3800, 'upcoming', 1),
('AmericanAirlines', 6002, 'ORD', '2025-12-01 19:15:00', 'TXL', '2026-01-02 10:20:00', 3900, 'delayed', 1),

-- ===== British Airways =====
('BritishAirways', 7001, 'LGA', '2025-07-14 12:30:00', 'FRA', '2025-07-15 02:20:00', 4100, 'upcoming', 1),
('BritishAirways', 7002, 'FRA', '2025-10-21 15:00:00', 'PKX', '2025-10-22 08:10:00', 4600, 'on-time', 1),

-- ===== Emirates =====
('Emirates', 8001, 'FRA', '2025-11-30 23:20:00', 'PVG', '2025-12-01 16:00:00', 6500, 'upcoming', 1),
('Emirates', 8002, 'MUC', '2025-06-25 09:45:00', 'PEK', '2026-06-25 20:55:00', 5700, 'upcoming', 1);


-- --------------------------------------------------------

--
-- Create Table: `permission`
--

CREATE TABLE `permission` (
  `username` varchar(50) NOT NULL,
  `permission_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `permission`
--

INSERT INTO permission (username, permission_type) VALUES
-- ===== CEAir =====
('ce_admin@ceair.com', 'Admin'),
('ce_ops@ceair.com',   'Operator'),
('qw2440@nyu.edu',      'Admin'),

-- ===== Lufthansa =====
('lh_admin@lufthansa.com', 'Admin'),
('lh_ops@lufthansa.com',   'Operator'),
('rr@lufthansa.com',        'Admin'),
('ae@lufthansa.com',        'Admin'),
('ae@lufthansa.com',        'Operator'),

-- ===== AirChina =====
('ac_admin@airchina.com', 'Admin'),
('ac_ops@airchina.com',   'Operator'),

-- ===== Delta =====
('dl_admin@delta.com', 'Admin'),
('dl_ops@delta.com',   'Operator'),

-- ===== United =====
('ua_admin@united.com', 'Admin'),
('ua_ops@united.com',   'Operator'),

-- ===== American Airlines =====
('aa_admin@aa.com', 'Admin'),
('aa_ops@aa.com',   'Operator'),

-- ===== British Airways =====
('ba_admin@ba.com', 'Admin'),
('ba_ops@ba.com',   'Operator'),

-- ===== Emirates =====
('ek_admin@emirates.com', 'Admin'),
('ek_ops@emirates.com',   'Operator');

-- --------------------------------------------------------

--
-- Create Table: `purchases`
--

CREATE TABLE `purchases` (
  `ticket_id` int(11) NOT NULL,
  `customer_email` varchar(50) NOT NULL,
  `booking_agent_id` int(11) DEFAULT NULL,
  `purchase_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

INSERT INTO purchases (ticket_id, customer_email, booking_agent_id, purchase_date) VALUES
(1,  'ml9007@nyu.edu',             2,   '2025-05-05'),
(2,  'sarah.jones@example.com',    NULL,'2025-05-10'),
(3,  'emma.wilson@gmail.com',      1,   '2025-05-12'),
(4,  'yuki.tanaka@gmail.com',      NULL,'2025-05-15'),
(5,  'kevin.brown@yahoo.com',      4,   '2025-05-18'),
(6,  'qw2440@nyu.edu',             NULL,'2025-05-20'),
(7,  'jac32@nyu.edu',              3,   '2025-04-01'),
(8,  'lucas.martin@gmail.com',     NULL,'2025-03-25'),
(9,  'hassan.ali@protonmail.com',  6,   '2025-03-10'),
(10, 'sofia.romero@hotmail.com',   NULL,'2025-03-02'),
(11,'michael.chen@outlook.com',    5,   '2025-02-28'),
(12,'ml9007@nyu.edu',              NULL,'2025-02-22');

-- --------------------------------------------------------

--
-- Create Table: `ticket`
--

CREATE TABLE `ticket` (
  `ticket_id` int(11) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `flight_num` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `ticket`
--

INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES
(1, 'CEAir', 2001),
(2, 'CEAir', 2002),
(3, 'CEAir', 2003),
(4, 'CEAir', 2004),
(5, 'Lufthansa', 321),
(6, 'Lufthansa', 510),
(7, 'Lufthansa', 517),
(8, 'Lufthansa', 525),
(9, 'AirChina', 3001),
(10, 'Delta', 4001),
(11, 'United', 5001),
(12, 'Emirates', 8001);

--
-- Export the index of the table
--

--
-- Table index: `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Table index: `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Table index: `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airline_name`,`airplane_id`);

--
-- Table index: `booking_agent`
--
ALTER TABLE `booking_agent`
  ADD PRIMARY KEY (`email`);

--
-- Table index: `booking_agent_work_for`
--
ALTER TABLE `booking_agent_work_for`
  ADD PRIMARY KEY (`email`,`airline_name`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Table index: `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Table index: `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`airline_name`,`flight_num`),
  ADD KEY `airline_name` (`airline_name`,`airplane_id`),
  ADD KEY `departure_airport` (`departure_airport`),
  ADD KEY `arrival_airport` (`arrival_airport`);

--
-- Table index: `permission`
--
ALTER TABLE `permission`
  ADD PRIMARY KEY (`username`,`permission_type`);

--
-- Table index: `purchases`
--
ALTER TABLE `purchases`
  ADD PRIMARY KEY (`ticket_id`,`customer_email`),
  ADD KEY `customer_email` (`customer_email`);

--
-- Table index: `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_id`),
  ADD KEY `airline_name` (`airline_name`,`flight_num`);

--
-- Export the constraints of the table
--

--
-- Table constraint: `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Table constraint: `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Table constraint: `booking_agent_work_for`
--
ALTER TABLE `booking_agent_work_for`
  ADD CONSTRAINT `booking_agent_work_for_ibfk_1` FOREIGN KEY (`email`) REFERENCES `booking_agent` (`email`),
  ADD CONSTRAINT `booking_agent_work_for_ibfk_2` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Table constraint: `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`,`airplane_id`) REFERENCES `airplane` (`airline_name`, `airplane_id`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`departure_airport`) REFERENCES `airport` (`airport_name`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`arrival_airport`) REFERENCES `airport` (`airport_name`);

--
-- Table constraint: `permission`
--
ALTER TABLE `permission`
  ADD CONSTRAINT `permission_ibfk_1` FOREIGN KEY (`username`) REFERENCES `airline_staff` (`username`);

--
-- Table constraint: `purchases`
--
ALTER TABLE `purchases`
  ADD CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`),
  ADD CONSTRAINT `purchases_ibfk_2` FOREIGN KEY (`customer_email`) REFERENCES `customer` (`email`);

--
-- Table constraint: `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`airline_name`,`flight_num`) REFERENCES `flight` (`airline_name`, `flight_num`);
COMMIT;
