# Ludoteca-TP-IDS
Trabajo Practico Final para la material de introduccion al desarrollo de software.

## Integrantes
- Nahuel Matias Villa - Padron: 106795
- Brian Abel Quiroz - Padron: 107166
- Franco Guastavino - Padron: 113265
- Alejandro Nicolas Sotelo van Oordt - Padron: 95985
- Tomás Agustín Irigoyen Barrone - Padron: 114019
- Gianluca Miguel Pate - Padron: 105695
- Dionel Ulises Paco Anagua - Padron: 113561

## 🚀 Levantar el Proyecto con Docker

Este proyecto utiliza **Docker** y **Docker Compose** para levantar automáticamente todos los servicios necesarios: base de datos, backend y frontend.

### 📦 Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

---

### ▶️ Iniciar el proyecto

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```


2.  **Verificar puertos en uso (opcional pero recomendado)**

Antes de iniciar los servicios, asegurate de que los puertos necesarios estén libres:

```bash
lsof -i :3306   # Puerto MySQL
lsof -i :8080   # Puerto Backend
lsof -i :3000   # Puerto Frontend
kill -9 <PID>   # En caso de que un puerto esté en uso
```

3. **Iniciar proyecto**
```bash
docker-compose up --build
```

Nota: Ante cada cambio es necesario agregar el flag de build, de lo contrario no sumarlo si solo quiere correr una imagen estable

## Endpoints
- '/' o index -----> Es el home de la pagina. Aca vemos juegos que son "novedad" o "populares" tanto con un formato de carrusel como 
con cuadros que muestran la descripcion y el precio del mismo.

- '/juego/<int:game_id>' -----> Este endpoint va a mostrar la pagina de cada juego individualmente, segun su id obtenido desde la api de Steam. 
En la siguiente, se muestra precio, descripcion, generos y categorias, reseñas de usuarios y un boton para añadir al carrito.

- '/login' -----> Permite al usuario loguearse o registrarse, en caso de no tener cuenta.

- '/carrito' -----> Como lo indica el nombre, acá deberán aparecer los juegos que el usuario logueado añadió a su carrito para poder finalizar 
la compra.

- '/catalogo' -----> Un endpoint que muestre, en varias paginas, el catalogo de juegos completo pedido a la api de Steam y 
guardado en nuestra base de datos.

