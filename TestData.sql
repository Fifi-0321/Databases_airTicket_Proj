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
('LuftHansa');

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

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`) VALUES
('ae@lufthansa.com', 'a0cf0de477f03ca38ae4568115907412', 'Albert', 'Einstein', '1980-03-01', 'Lufthansa'),
('qw2440@nyu.edu', 'a0cf0de477f03ca38ae4568115907412', 'Richael', 'Richter', '2004-10-28', 'CEAir'),
('rr@lufthansa.com', 'a0cf0de477f03ca38ae4568115907412', 'Richard', 'Richter', '2001-04-20', 'Lufthansa'),
('xg7@nyu.edu', 'a0cf0de477f03ca38ae4568115907412', 'Xianbin', 'Gu', '2000-01-12', 'CEAir');

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
('CEAir', 1, 300),
('CEAir', 1234, 200),
('LuftHansa', 101, 250),
('Lufthansa', 309, 50),
('Lufthansa', 888, 299),
('Lufthansa', 909, 1);

-- --------------------------------------------------------

--
-- Create Table: `airport`
--

CREATE TABLE `airport` (
  `airport_name` varchar(50) NOT NULL,
  `airport_city` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Insert Data: `airport`
--

INSERT INTO `airport` (`airport_name`, `airport_city`) VALUES
('BER', 'Berlin'),
('DUS', 'Düsseldorf'),
('FRA', 'Frankfurt'),
('MUC', 'München'),
('PEK', 'Beijing'),
('PVG', 'Shanghai'),
('TXL', 'Berlin');

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
('rebecca@nyu.edu', 'a0cf0de477f03ca38ae4568115907412', 1);

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

INSERT INTO `booking_agent_work_for` (`email`, `airline_name`) VALUES
('rebecca@nyu.edu', 'CEAir'),
('rebecca@nyu.edu', 'Lufthansa');

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

INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('jac32@nyu.edu', 'Alex Crosse', 'a0cf0de477f03ca38ae4568115907412', '1', 'Downing Street', 'London', 'UK', 12345, 'EM7200212', '2035-05-01', 'UK', '1984-04-10'),
('ml9007@nyu.edu', 'Adelyn Li', 'a0cf0de477f03ca38ae4568115907412', '8', 'West Gaoqing Road', 'Shanghai', 'China', 12121, 'EM76543321', '2055-05-10', 'China', '2005-04-16'),
('qw2440@nyu.edu', 'Qiuyi Wang', 'a0cf0de477f03ca38ae4568115907412', '6', 'HuoXiang Road', 'Shanghai', 'China', 12345, 'EM1234567', '2040-12-04', 'China', '2004-10-28');

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

INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES
('CEAir', 129, 'PVG', '2025-06-13 00:05:00', 'FRA', '2025-06-13 12:05:00', 5050, 'upcoming', 1234),
('CEAir', 1234, 'PVG', '2025-05-10 10:00:00', 'PEK', '2025-05-10 12:30:00', 800, 'upcoming', 1),
('Lufthansa', 321, 'PVG', '2025-07-11 10:00:00', 'MUC', '2025-07-11 22:00:00', 15000, 'upcoming', 909),
('Lufthansa', 510, 'PVG', '2025-08-13 15:00:00', 'FRA', '2025-08-13 20:05:00', 4999, 'upcoming', 101),
('Lufthansa', 517, 'FRA', '2025-05-17 07:45:00', 'BER', '2025-05-17 09:45:00', 400, 'upcoming', 888),
('Lufthansa', 525, 'MUC', '2025-05-13 08:30:00', 'FRA', '2025-05-13 09:45:00', 450, 'delayed', 101),
('Lufthansa', 902, 'BER', '2025-06-28 14:30:00', 'PVG', '2025-06-29 15:30:00', 7500, 'cancelled', 888);

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

INSERT INTO `permission` (`username`, `permission_type`) VALUES
('ae@lufthansa.com', 'Admin'),
('ae@lufthansa.com', 'Operator'),
('qw2440@nyu.edu', 'Admin'),
('rr@lufthansa.com', 'Admin');

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

--
-- Insert Data: `purchases`
--

INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES
(2, 'jac32@nyu.edu', NULL, '2025-05-01'),
(3, 'jac32@nyu.edu', NULL, '2025-05-01'),
(4, 'jac32@nyu.edu', NULL, '2025-04-17'),
(6, 'ml9007@nyu.edu', NULL, '2025-05-01'),
(7, 'jac32@nyu.edu', NULL, '2025-03-01'),
(9, 'qw2440@nyu.edu', NULL, '2025-05-10'),
(10, 'qw2440@nyu.edu', NULL, '2025-05-10'),
(11, 'jac32@nyu.edu', 1, '2025-05-10'),
(16, 'jac32@nyu.edu', NULL, '2025-05-12'),
(17, 'jac32@nyu.edu', NULL, '2025-05-12'),
(18, 'qw2440@nyu.edu', NULL, '2025-05-12'),
(19, 'qw2440@nyu.edu', NULL, '2025-05-12'),
(20, 'qw2440@nyu.edu', NULL, '2025-05-12');

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

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES
(1, 'CEAir', 129),
(2, 'CEAir', 129),
(15, 'CEAir', 129),
(16, 'CEAir', 129),
(18, 'CEAir', 129),
(19, 'CEAir', 129),
(3, 'CEAir', 1234),
(6, 'CEAir', 1234),
(9, 'CEAir', 1234),
(10, 'CEAir', 1234),
(17, 'Lufthansa', 321),
(14, 'Lufthansa', 510),
(20, 'Lufthansa', 510),
(11, 'Lufthansa', 517),
(4, 'Lufthansa', 525),
(5, 'Lufthansa', 525),
(12, 'Lufthansa', 525),
(7, 'Lufthansa', 902),
(8, 'Lufthansa', 902),
(13, 'Lufthansa', 902);

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
-- Table index: `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`airport_name`);

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
