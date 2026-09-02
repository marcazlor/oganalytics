# OGAnalytics

Plataforma de análisis del mercado del petróleo. Integra datos públicos de precios de crudo, producción por país e inventarios; los expone mediante una API REST y aplica modelos de machine learning para detección de anomalías y análisis predictivo del diferencial Brent-WTI.

## Requisitos

- [Docker](https://www.docker.com/products/docker-desktop/) y Docker Compose.

No hace falta instalar Python ni PostgreSQL: todo corre en contenedores.

## Puesta en marcha

**1. Clonar el repositorio**

```bash
git clone <url-del-repositorio>
cd oganalytics
```

**2. Configurar las variables de entorno**

Copia el fichero de ejemplo y edita los valores (sobre todo la contraseña):

```bash
cp .env.example .env
```

**3. Levantar los servicios**

```bash
docker compose up --build -d
```

Esto construye la imagen de la API y arranca dos contenedores: la aplicación y una base de datos PostgreSQL. Las tablas se crean automáticamente al arrancar.

**4. Cargar los datos**

La base de datos arranca vacía. Para poblarla con los CSV de `data/raw/`:

```bash
docker compose exec api python scripts/load_data.py
```

El script es idempotente: puede ejecutarse las veces que haga falta sin duplicar registros.

**5. Entrenar el modelo**

El endpoint de predicción necesita el modelo serializado:

```bash
docker compose exec api python scripts/train_model.py
```

**6. Comprobar que funciona**

La documentación interactiva de la API está en [http://localhost:8000/docs](http://localhost:8000/docs).

## Conflicto de puertos con PostgreSQL

Por defecto, el servicio de base de datos se publica en el puerto **5432** del host. Si ya tienes PostgreSQL instalado y ejecutándose en tu máquina, ese puerto estará ocupado y la conexión desde clientes externos (pgAdmin, DBeaver, la extensión de VS Code) llegará a tu instalación local en lugar de al contenedor. El síntoma es un error de autenticación con un usuario que sí existe en el contenedor.

Para evitarlo, cambia el puerto del host en `docker-compose.yml`:

```yaml
  postgres:
    ports:
      - "5433:5432"
```

El primer número es el puerto del host y el segundo el del contenedor. La API no se ve afectada: se comunica con la base de datos por la red interna de Compose, donde el puerto sigue siendo el 5432.

Para conectar desde un cliente externo con esa configuración:

| Parámetro | Valor |
|---|---|
| Host | `localhost` |
| Puerto | `5433` |
| Base de datos | el valor de `POSTGRES_DB` |
| Usuario | el valor de `POSTGRES_USER` |
| Contraseña | el valor de `POSTGRES_PASSWORD` |

Desde dentro de la red de Compose el host es `postgres`, no `localhost`.

## Reiniciar la base de datos desde cero

PostgreSQL solo aplica las credenciales de las variables de entorno en la **primera** inicialización del volumen. Si cambias usuario o contraseña en el `.env` después de haber levantado el proyecto, hay que recrear el volumen:

```bash
docker compose down -v
docker compose up -d
```

Después habrá que volver a ejecutar los pasos 4 y 5.

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/price/` | Precios mensuales de Brent y WTI |
| GET | `/price/spread` | Diferencial Brent-WTI, con filtro opcional de fechas |
| GET | `/price/latest` | Último registro de precios disponible |
| GET | `/production/` | Producción de crudo por país |
| GET | `/production/{country}` | Producción de un país concreto |
| GET | `/production/filter` | Producción con filtros de país y fechas |
| GET | `/inventory/` | Inventarios de crudo en Cushing |
| GET | `/inventory/filter` | Inventarios con filtro de fechas |
| GET | `/predictions/spread` | Predicción del spread del mes siguiente |

## Desarrollo en local sin Docker

El proyecto también puede ejecutarse directamente con Python usando SQLite, que es la configuración por defecto del `.env`:

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements-dev.txt
uvicorn src.main:app --reload
```

La aplicación lee la URL de la base de datos de la variable `DATABASE_URL`, de modo que el mismo código funciona con SQLite en local y con PostgreSQL en contenedor sin cambios.