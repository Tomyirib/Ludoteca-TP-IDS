# Ludoteca-TP-IDS
Trabajo Practico Final para la material de introduccion al desarrollo de software.

## Integrantes
- Nahuel Matias Villa - Padron: 106795
- Brian Abel Quiroz - Padron: 107166
- Franco Guastavino - Padron: 113265
- Alejandro Nicolas Sotelo van Oordt - Padron: 95985
- Tomás Agustín Irigoyen Barrone - Padron: 114019

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
’/’ → (Página principal con juegos destacados)

’/catalogo’ → (Muestra todos los juegos disponibles, paginados)

’/juego/<int:game_id>’ → (Muestra los detalles del juego y sus comentarios)

’/login’ → (Formulario y lógica de inicio de sesión)

’/register’ → (Formulario y lógica de registro de usuario)

’/logout’ → (Cierra sesión del usuario)

’/carrito’ → (Muestra el carrito con los juegos agregados)

’/biblioteca’ → (Muestra los juegos comprados por el usuario logueado)

’/comunidad’ → (Muestra los últimos comentarios realizados por los usuarios)

’/admin’ → (Lleva al dashboard de admin)
