# ⚽ API JSON SoccerVision  

API RESTful desarrollada en Python que permite la gestión de usuarios, equipos, jugadores y partidos de fútbol. Proporciona endpoints para la creación, consulta, actualización y eliminación de estos datos.  

## 📌 Características  
- Gestión de **usuarios** con autenticación.  
- CRUD para **equipos, jugadores y partidos**.  
- Respuestas en formato JSON.  
- Uso de **Flask** para el backend.  

## 🚀 Instalación  
1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/CrisJurado10/API_JSON_SoocerVison.git
   cd API_JSON_SoocerVison
2. **Crear y activar un entorno virtual**  
bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate\

▶️ Uso
Ejecutar el servidor:
python app.py

Acceder a la API en http://localhost:5000/
📡 Endpoints
🔹 Usuarios
POST /usuarios → Crear usuario
GET /usuarios → Obtener todos los usuarios
GET /usuarios/<id> → Obtener un usuario específico
PUT /usuarios/<id> → Actualizar usuario
DELETE /usuarios/<id> → Eliminar usuario
🔹 Equipos
POST /equipos → Crear equipo
GET /equipos → Obtener todos los equipos
GET /equipos/<id> → Obtener un equipo específico
PUT /equipos/<id> → Actualizar equipo
DELETE /equipos/<id> → Eliminar equipo
🔹 Jugadores
POST /jugadores → Crear jugador
GET /jugadores → Obtener todos los jugadores
GET /jugadores/<id> → Obtener un jugador específico
PUT /jugadores/<id> → Actualizar jugador
DELETE /jugadores/<id> → Eliminar jugador
🔹 Partidos
POST /partidos → Crear partido
GET /partidos → Obtener todos los partidos
GET /partidos/<id> → Obtener un partido específico
PUT /partidos/<id> → Actualizar partido
DELETE /partidos/<id> → Eliminar partido
📜 Licencia
Este proyecto está bajo la Licencia MIT.

👤 Autor
Cristian Jurado
GitHub: CrisJurado10
