# Viajerapp

Para correr el proyecto, se necesita agregar las siguientes variables en un archivo .env

```
# server variables
JWT_KEY=
SECRET_KEY=

#DB CONFIG
POSTGRES_HOST=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

# Amazon S3
AWS_BUCKET_NAME=
AWS_ACCESS_KEY=
AWS_SECRET_ACCESS_KEY=
REGION_NAME=
SERVICE_NAME=

# APIs
AMADEUS_API_KEY=LKSCwaojPNrqZagzQ53BUDXIsbt4
```

La carpeta resources debe quedar con la siguiente estructura

```
src
|- resources
    |- files
        |-intents_viajerapp.json
        |-offers.json
    |-models
        |-viajerapp_chatbot_model.keras
```