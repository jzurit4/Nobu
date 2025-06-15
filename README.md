
# Nobu

**Nobu** es un bot de Discord desarrollado en Python que permite a los servidores recordar y felicitar automáticamente a los miembros en sus cumpleaños. Ideal para comunidades que buscan mantener un ambiente cálido y personalizado.

## 🎯 Descripción

Este bot facilita la gestión de cumpleaños dentro de un servidor de Discord. Los usuarios pueden registrar sus fechas de nacimiento, y el bot enviará un mensaje de felicitación en el canal designado en la fecha correspondiente.

## ⚙️ Requisitos

- Python 3.10 o superior
- Biblioteca `discord.py` (instalable mediante `pip install discord.py`)
- Base de datos SQLite (incluida en el proyecto)

## 🚀 Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/jzurit4/Nobu.git
   cd Nobu
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura tu token de Discord:

   - Crea una aplicación en el [Portal de Desarrolladores de Discord](https://discord.com/developers/applications).
   - Obtén el token de tu bot y reemplaza 'YOUR_BOT_TOKEN' en el archivo `main.py`.

5. Ejecuta el bot:

   ```bash
   python main.py
   ```

## 📂 Estructura del Proyecto

- `main.py`: Código principal del bot.
- `requirements.txt`: Dependencias necesarias.
- `birthdays.db`: Base de datos SQLite que almacena los cumpleaños.
- `sent_birthdays.json`: Registro de felicitaciones enviadas.

## ✅ Funcionalidades

- Registro de fechas de nacimiento de miembros.
- Envío automático de mensajes de cumpleaños en el canal configurado.
- Almacenamiento persistente mediante base de datos SQLite.

## 📌 Notas

- Asegúrate de que tu bot tenga los permisos necesarios para enviar mensajes en el canal deseado.
- La base de datos `birthdays.db` se actualiza automáticamente con cada nuevo registro.
- Asegúrate de que el bot este solo en tu servidor, ya que fue hecho con el fin de un servidor fijo.


