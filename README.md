# M.S.A.T. - Mentor Studios Audio Terminal

Aplicación de escritorio para gestionar y reproducir archivos de audio desde un panel de botones.

## Resumen

Esta aplicación ofrece una interfaz gráfica moderna para agregar, reproducir y detener módulos de audio usando `PySide6` y `pygame`.

## Características principales

- Interfaz gráfica con PySide6.
- Reproducción de audio con `pygame`.
- Soporte multilenguaje a partir de archivos JSON en `lang/`.
- Configuración persistente de los módulos en `msat_audio_config.json`.
- Gestión de audio mediante botones configurables.

## Requisitos

- Python 3.11+ (también compatible con Python 3.14).
- `PySide6`
- `pygame`

## Instalación

1. Crear y activar un entorno virtual (recomendado):

Para PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Para Windows CMD:

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

Para Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install PySide6 pygame
```

## Uso

Ejecuta la aplicación desde la carpeta del proyecto:

```bash
python msat.py
```

## Estructura del proyecto

- `msat.py` - Script principal de la aplicación.
- `audio_files/` - Carpeta que contiene los archivos de audio del proyecto.
- `lang/` - Traducciones en JSON para los idiomas disponibles.
- `msat_audio_config.json` - Configuración de módulos de audio.
- `msat_language_config.json` - Configuración de idioma.

## Configuración y datos

- `audio_files/` debe contener los archivos de audio que usa la aplicación.
- `lang/` maneja la localización y permite agregar nuevos idiomas fácilmente.
- Los archivos JSON de configuración guardan los módulos y la selección de idioma entre sesiones.

## Seguridad y buenas prácticas

- El repositorio incluye un `.gitignore` actualizado para evitar subir archivos de entorno, caches y configuraciones locales.
- No agregues archivos sensibles como `.env`, claves privadas, certificados o bases de datos locales al repositorio.
- `audio_files/` puede contener datos pesados; controla bien qué activos subes al repositorio si deseas mantenerlo liviano.

## Contribuciones

Si deseas mejorar el proyecto, puedes:

- Extender la localización en `lang/`.
- Mejorar la interfaz y la experiencia de usuario.

## Licencia

Proyecto personal.
