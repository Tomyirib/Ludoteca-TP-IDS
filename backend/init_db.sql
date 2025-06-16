CREATE DATABASE IF NOT EXISTS ludoteca;
USE ludoteca;

CREATE TABLE IF NOT EXISTS juegos (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(50),
    is_free BOOLEAN,
    required_age INT,
    website TEXT,
    description TEXT,
    header_image TEXT,
    price TEXT
);


CREATE TABLE IF NOT EXISTS generos (
    id_genero INT PRIMARY KEY,
    descripcion VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS juego_genero (
    id_juego INT REFERENCES juegos(id),
    id_genero INT REFERENCES generos(id_genero),
    PRIMARY KEY (id_juego, id_genero)
);

CREATE TABLE IF NOT EXISTS screenshots (
    id_screenshot INT PRIMARY KEY AUTO_INCREMENT,
    juego_id INT,
    url TEXT,
    FOREIGN KEY (juego_id) REFERENCES juegos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS videos (
    id_video INT PRIMARY KEY AUTO_INCREMENT,
    juego_id INT,
    url TEXT,
    FOREIGN KEY (juego_id) REFERENCES juegos(id) ON DELETE CASCADE
);

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER UNIQUE PRIMARY KEY,
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS juego_categoria (
    juego_id INT,
    categoria_id INT,
    PRIMARY KEY (juego_id, categoria_id),
    FOREIGN KEY (juego_id) REFERENCES juegos(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS requisitos_minimos (
    id_requisito INT PRIMARY KEY,
    id_juego INT REFERENCES juegos(id),
    sistema_operativo VARCHAR(100),
    procesador VARCHAR(255),
    memoria_ram VARCHAR(100),
    almacenamiento VARCHAR(100),
    tarjeta_grafica VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS requisitos_recomendados (
    id_requisito INT PRIMARY KEY,
    id_juego INT REFERENCES juegos(id),
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
    email VARCHAR(255) UNIQUE NOT NULL,
    contrasenia VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL
);


-- Tabla Comentarios

CREATE TABLE IF NOT EXISTS comentarios (
    comentario_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    juego_id INT NOT NULL,
    comentario_texto VARCHAR(511) NOT NULL,
    comentario_timestamp DATETIME NOT NULL,
    FOREIGN KEY (comentario_id)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE,
    FOREIGN KEY (juego_id)
        REFERENCES juegos(id)
        ON DELETE CASCADE
);