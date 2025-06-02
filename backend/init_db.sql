CREATE DATABASE IF NOT EXISTS ludoteca;
USE ludoteca;

CREATE TABLE IF NOT EXISTS juegos (
    id_juego INT PRIMARY KEY,
    nombre VARCHAR(255),
    tipo VARCHAR(50),
    es_gratis BOOLEAN,
    edad_requerida INT,
    sitio_web TEXT,
    descripcion_detallada TEXT,
    acerca_del_juego TEXT,
    descripcion_corta TEXT,
    imagen_cabecera TEXT,
    imagen_capsula_231x87 TEXT,
    imagen_capsula_184x69 TEXT
);


CREATE TABLE IF NOT EXISTS generos (
    id_genero INT PRIMARY KEY,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS juego_genero (
    id_juego INT REFERENCES juegos(id_juego),
    id_genero INT REFERENCES generos(id_genero),
    PRIMARY KEY (id_juego, id_genero)
);

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INT UNIQUE PRIMARY KEY,
    descripcion VARCHAR(255) 
);

CREATE TABLE IF NOT EXISTS juego_categoria (
    juego_id INT,
    categoria_id INT,
    PRIMARY KEY (juego_id, categoria_id),
    FOREIGN KEY (juego_id) REFERENCES juegos(id_juego) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS requisitos_minimos (
    id_requisito INT PRIMARY KEY,
    id_juego INT REFERENCES juegos(id_juego),
    sistema_operativo VARCHAR(100),
    procesador VARCHAR(255),
    memoria_ram VARCHAR(100),
    almacenamiento VARCHAR(100),
    tarjeta_grafica VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS requisitos_recomendados (
    id_requisito INT PRIMARY KEY,
    id_juego INT REFERENCES juegos(id_juego),
    sistema_operativo VARCHAR(100),
    procesador VARCHAR(255),
    memoria_ram VARCHAR(100),
    almacenamiento VARCHAR(100),
    tarjeta_grafica VARCHAR(255)
);


-- Tabla para login 

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    es_admin BOOLEAN,
    email VARCHAR(255) NOT NULL,
    contrasenia VARCHAR(255) NOT NULL,
    primer_nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL
);