# Proyecto para la evaluación del módulo de PA: Diario Personal
# Concepto general

El Diario Personal de Notas de Texto es una API REST desarrollada en FastAPI que permite a los usuarios registrarse y guardar notas personales en una base de datos.
Cada nota procede de un archivo .txt o .md existente en el sistema, cuyo path se envía en el cuerpo de la petición.

La API lee el contenido del archivo, lo guarda en la base de datos asociado al usuario, y ofrece endpoints para consultar, buscar o eliminar notas.

Todo el flujo (usuarios + notas) se ejecuta 100 % en local con Python.

# Objetivos del proyecto

- Aplicar principios de **POO**.
- Implementar múltiples endpoints REST (GET, POST, DELETE, PUT...).
- Emplear SQLite mediante SQLAlchemy para persistir los datos.
- Interactuar con la API usando un script Python con la librería _requests_.
- Desplegar y probar todo en entorno local (localhost).

# Entidades del sistema

## `User`

Representa a un usuario del diario. Sus campos son:

- `id` (int, primary key)
- `name` (str)
- `email` (str) 
- `password` (str)
- `created_at` (datetime)

## `Note`

Representa una nota del diario asociada a un archivo de texto. Sus campos son:

- `id` (int, primary key)
- `user_id` (foreign key (`User`))
- `file_path` (str)
- `content` (str)
- `created_at` (datetime)

## Endpoints REST

| Método           | Ruta                           | Descripción                            |
| ---------------- | -------------------------------| -------------------------------------- |
| `POST`           | `/users`                       | Crear nuevo usuario                    |
| `GET`            | `/users`                       | Listar todos los usuarios              |
| `POST`           | `/notes`                       | Crear nota desde un archivo local      |
| `GET`            | `/notes`                       | Listar todas las notas                 |
| `GET`            | `/notes/{id}`                  | Ver contenido completo de una nota     |
| `GET`            | `/notes/search?query=palabra`  | Buscar notas que contengan una palabra |
| `DELETE`         | `/notes/{id}`                  | Eliminar una nota                      |

