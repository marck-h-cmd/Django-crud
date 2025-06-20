# 🐍 Django Project Setup Guide

Este proyecto está desarrollado con Django y requiere instalar sus dependencias, aplicar migraciones y luego ejecutar el servidor de desarrollo. Sigue estos pasos para correrlo correctamente.

## ✅ Requisitos previos

Asegúrate de tener instalado:

- Python 3.8+
- pip
- virtualenv (opcional pero recomendado)
- PostgreSQL o SQLite (según la configuración del proyecto)

## 🚀 Instalación y ejecución

### 1. Instala las dependencias

```bash
pip install -r requirements.txt
Claro, aquí tienes el `README.md` actualizado sin los puntos 1, 2, 4 ni la sección de tests:

````markdown
# 🐍 Django Project Setup Guide

Este proyecto está desarrollado con Django y requiere instalar sus dependencias, aplicar migraciones y luego ejecutar el servidor de desarrollo. Sigue estos pasos para correrlo correctamente.

## ✅ Requisitos previos

Asegúrate de tener instalado:

- Python 3.8+
- pip
- virtualenv (opcional pero recomendado)
- PostgreSQL o SQLite (según la configuración del proyecto)

## 🚀 Instalación y ejecución

### 1. Instala las dependencias

```bash
pip install -r requirements.txt
````

### 2. Aplica las migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. (Opcional) Crea un superusuario

```bash
python manage.py createsuperuser
```

### 4. Ejecuta el servidor de desarrollo

```bash
python manage.py runserver
```

Luego ve a `http://127.0.0.1:8000/` en tu navegador.

---



