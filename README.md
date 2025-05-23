# 🎓 Orientador de Carreras con FastAPI + Gradio

Este proyecto ofrece una interfaz interactiva donde los usuarios pueden describir sus intereses y recibir recomendaciones de carreras basadas en un modelo personalizado. 
Usa **Gradio** para la interfaz y **FastAPI** como backend, pensado para desplegar en **Azure App Service** (incluido el plan gratuito F1).

---

## 🚀 ¿Qué hace esta app?

- Recibe un texto sobre tus intereses o habilidades.
- Usa un modelo (`BuscadorCarreras`) que analiza tu entrada.
- Devuelve 2 posibles opciones con una puntuacion de 0 a 1.
- Se puede usar tanto localmente como en la nube (Azure Web App).

---

## 🧠 Tecnologías utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) – para el backend (ASGI compatible).
- [Gradio](https://www.gradio.app/) – para crear una interfaz web sencilla.
- [Uvicorn](https://www.uvicorn.org/) – servidor ASGI para producción.
- [Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/) – para desplegar la app.

---
=

