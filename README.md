🚀 Gestor de Tareas con FastAPI
¡Hola! 👋 Este es un proyecto simple pero funcional para gestionar tareas usando FastAPI, SQLite y JWT Auth. Lo armé como ejercicio para practicar backends con Python de forma rápida, moderna y divertida 🧠⚡

🧩 ¿Qué hace esta app?
Con esta API puedes:

✅ Crear usuarios y autenticarte con tokens (JWT)
✅ Crear tareas (todo items)
✅ Listar todas tus tareas
✅ Marcar tareas como completadas o eliminarlas
✅ Cada usuario solo ve sus propias tareas (autenticación protegida)

🛠 Tecnologías utilizadas
FastAPI ⚡
SQLite para la base de datos
SQLAlchemy como ORM
Pydantic para validación de datos
JWT para autenticación
🔧 Cómo levantar el proyecto
Clona este repo:
git clone https://github.com/tuusuario/gestor-de-tareas.git
cd gestor-de-tareas

2. Instala las dependencias:
pip install -r requirements.txt

3. Correr el servidor:
uvicorn main:app --reload

4. Abre el navegador y ve a:
http://127.0.0.1:8000/docs


🧙‍♂️ "No trates de hacer la app perfecta. Haz una app que funcione, que entiendas y que puedas mejorar luego."
