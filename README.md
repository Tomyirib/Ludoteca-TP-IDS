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

