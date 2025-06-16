# WeatherBuddy - GuardiánClima ITBA

WeatherBuddy es una aplicación de consola desarrollada por el grupo "{NOMBRE_DE_GRUPO}" del ITBA. Permite consultar el clima actual de cualquier ciudad, guardar un historial global de consultas, generar estadísticas y gráficos, y recibir consejos de vestimenta personalizados mediante IA.

## ¿Cómo funciona?

- **Registro e inicio de sesión:**
  - Los usuarios pueden registrarse con un nombre de usuario y una contraseña segura (mínimo 8 caracteres, mayúsculas, minúsculas, dígitos y caracteres especiales).
  - El almacenamiento de credenciales es simulado y no seguro (CSV). Se utiliza hashing SHA-256 como ejemplo, pero se recomienda usar técnicas más robustas en producción.

- **Consultar clima:**
  - Ingresa el nombre de una ciudad y la app obtiene el clima actual desde APIs externas (OpenWeatherMap y OpenMeteo).
  - Los resultados se guardan en un historial global por usuario.

- **Historial personal:**
  - Consulta tu historial de búsquedas por ciudad.

- **Estadísticas y exportación:**
  - Genera estadísticas globales de uso, genera gráicos y exporta el historial completo en formato CSV.

- **Consejo IA:**
  - Recibe sugerencias de vestimenta personalizadas según el clima, usando IA (Gemini API).

## Menú principal

1. Consultar Clima Actual y Guardar en Historial Global
2. Ver Mi Historial Personal de Consultas por Ciudad
3. Estadísticas Globales de Uso y Exportar Historial Completo
4. Consejo IA: ¿Cómo Me Visto Hoy?
5. Acerca De...
6. Salir

## Instalación y uso

1. Clona este repositorio.
2. Instala Python 3.10+.
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crea un archivo `.env` con tus claves de API:
   ```
   WEATHER_KEY=tu_clave_openweathermap
   GEMINI_KEY=tu_clave_gemini
   ```
5. Ejecuta el programa principal:
   ```bash
   python main.py
   ```

## Dependencias
- Matplotlib
- Librería estándar de Python (hashlib, csv, os, datetime, etc.)
- Acceso a internet para las APIs

## Equipo de desarrollo
- Patricio Aldasoro
- Alejandro de Ugarriza Mohnblatt
- Zoe María Perez Colman
- Tomás Spurio
- Bautista Andrés Peral

**Grupo:** WeatherGuardians

---

Este proyecto es educativo y no debe usarse en producción sin mejoras de seguridad.
