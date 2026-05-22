# Programa Botones Audio

Aplicación de escritorio en Python para gestionar y reproducir archivos de audio desde un panel de botones.

## Descripción

Este proyecto ofrece una interfaz gráfica retro futurista para agregar, reproducir y detener módulos de audio. Está diseñado con PySide6 y usa `pygame` como backend de reproducción de audio.

## Características

- Interfaz gráfica con PySide6.
- Reproducción de audio con pygame.
- Añadir nuevos módulos de audio mediante un diálogo.
- Panel derecho de estado del sistema.
- Soporte multilenguaje mediante archivos JSON en `lang/`.
- Configuración persistente en `msat_audio_config.json`.

## Estructura del proyecto

- `msat.py` - Script principal de la aplicación.
- `audio_files/` - Carpeta donde se almacenan los archivos de audio usados por la aplicación.
- `lang/` - Archivos de traducción JSON para los idiomas disponibles.
- `msat_audio_config.json` - Configuración de los módulos de audio guardada por la aplicación.
- `msat_language_config.json` - Configuración de idioma guardada por la aplicación.

## Requisitos

- Python 3.11+ (o 3.14 como en el entorno actual).
- PySide6
- pygame

## Instalación

1. Crear y activar un entorno virtual (opcional pero recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install PySide6 pygame
```

## Uso

Ejecutar la aplicación desde la carpeta del proyecto:

```powershell
python msat.py
```

## Flujo de la aplicación

1. Al iniciar, el proyecto carga el idioma guardado y la configuración de los botones.
2. Se inicializa la interfaz gráfica y el motor de audio `pygame.mixer`.
3. El usuario puede agregar nuevos módulos de audio usando el diálogo correspondiente.
4. Cada módulo se muestra como un botón que reproduce el audio asociado.
5. Al cambiar el idioma, la reproducción activa se detiene automáticamente.

## Localización

El proyecto usa el directorio `lang/` para potenciar la localización. Cada archivo JSON contiene las claves de texto utilizadas en la interfaz.

## Notas importantes

- Asegúrate de que `audio_files/` exista y contenga los archivos `.mp3`, `.wav` u otros formatos soportados.
- Si la aplicación no encuentra un archivo de audio, mostrará un mensaje de error.
- El archivo `msat_audio_config.json` guarda la lista de módulos configurados.

## Contacto

Proyecto personal.
