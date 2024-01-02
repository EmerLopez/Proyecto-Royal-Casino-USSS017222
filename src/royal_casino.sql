-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-01-2024 a las 01:35:11
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `royal_casino`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `id` int(11) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`id`, `correo`, `password`) VALUES
(9, 'usss017222', '559977'),
(12, 'usss017922', '56568488'),
(13, 'usss030722', '79208499'),
(14, 'usss004122', '48462594'),
(15, 'usts002422', '59526295');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `DUI` int(11) NOT NULL,
  `telefono` int(11) NOT NULL,
  `p_pendiente` varchar(30) NOT NULL,
  `c_reservaciones` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `nombres`, `apellidos`, `DUI`, `telefono`, `p_pendiente`, `c_reservaciones`) VALUES
(80, 'Edwin', 'Lopez', 66197580, 75942434, 'Pagado', 3),
(81, 'Diego', 'Zepeda', 64253039, 70618355, 'Pendiente', 1),
(82, 'Fernando', 'Lopez', 66676661, 75714271, 'Pendiente', 1),
(83, 'Nilderson', 'chavez', 66172899, 64245174, 'Pagado', 1),
(84, 'henry', 'cortez', 55442336, 74258334, 'Pendiente', 1),
(85, 'Lorena', 'Rodriguez', 65488987, 74243031, 'pendiente', 1),
(86, 'Gustavo', 'Argueta', 64048434, 61171853, 'pendiente', 1),
(87, 'hendry', 'emilio', 63997583, 72537776, 'pagado', 1),
(88, 'Luis', 'hernandez', 155885413, 74286644, 'Inventario Devuelto', 1),
(89, 'Karla', 'Molina', 123810, 70706060, 'Pagado', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `cantidad` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id`, `nombre`, `cantidad`) VALUES
(1, 'sillas', -3880),
(2, 'mesas', -2916),
(3, 'manteles', -3029);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rmms`
--

CREATE TABLE `rmms` (
  `id` int(11) NOT NULL,
  `t_reservacion` varchar(30) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `DUI` int(11) NOT NULL,
  `telefono` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `c_mesas` int(11) NOT NULL,
  `c_sillas` int(11) NOT NULL,
  `c_manteles` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `pago` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `rmms`
--

INSERT INTO `rmms` (`id`, `t_reservacion`, `nombres`, `apellidos`, `DUI`, `telefono`, `fecha`, `c_mesas`, `c_sillas`, `c_manteles`, `total`, `pago`) VALUES
(22, '', 'Lorena', 'Rodriguez', 65488987, 74244461, '2024-02-22', 400, 150, 300, 1175, 'pendiente'),
(23, '', 'edwin', 'lopez', 66197580, 75942434, '2024-03-08', 100, 100, 300, 550, 'pendiente'),
(24, '', 'Fernando', 'Esquivel', 55874312, 74318889, '2024-01-03', 400, 800, 400, 1600, 'pagado'),
(25, '', 'Gustavo', 'Argueta', 64048434, 61171853, '2024-05-15', 100, 400, 100, 500, 'pendiente'),
(26, '', 'hendry', 'emilio', 63997583, 72537776, '2024-04-26', 200, 600, 200, 900, 'pagado'),
(28, '', 'luis', 'hernandez', 155885413, 26251515, '2024-01-06', 200, 400, 200, 800, 'pagado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `r_local`
--

CREATE TABLE `r_local` (
  `id` int(11) NOT NULL,
  `nombres` varchar(40) NOT NULL,
  `apellidos` varchar(40) NOT NULL,
  `DUI` int(11) NOT NULL,
  `telefono` int(11) NOT NULL,
  `t_reservacion` varchar(30) NOT NULL,
  `c_mesas` int(11) NOT NULL,
  `c_sillas` int(11) NOT NULL,
  `c_manteles` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `total` varchar(30) NOT NULL,
  `pago` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `r_local`
--

INSERT INTO `r_local` (`id`, `nombres`, `apellidos`, `DUI`, `telefono`, `t_reservacion`, `c_mesas`, `c_sillas`, `c_manteles`, `fecha`, `total`, `pago`) VALUES
(127, 'Edwin', 'Lopez', 66197580, 75942434, 'Planta Alta $125', 200, 500, 99, '2023-12-20', '874.00', 'Inventario Devuelto'),
(128, 'Diego', 'Zepeda', 64253039, 70618355, 'Planta Alta $125', 122, 100, 122, '2024-01-04', '541.00', 'Pendiente'),
(130, 'Nilderson', 'chavez', 66172899, 64245174, 'Planta Alta $125', 400, 100, 400, '2023-12-28', '1375.00', 'Pagado'),
(131, 'henry', 'cortez', 55442336, 74258334, 'Planta Alta $125', 50, 80, 50, '2024-02-09', '190.00', 'Inventario Devuelto'),
(134, 'Karla', 'Molina', 123810, 70706060, 'Local Completo $225', 20, 40, 25, '2023-12-10', '310.00', 'Pagado');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `rmms`
--
ALTER TABLE `rmms`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `r_local`
--
ALTER TABLE `r_local`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `rmms`
--
ALTER TABLE `rmms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `r_local`
--
ALTER TABLE `r_local`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=135;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
