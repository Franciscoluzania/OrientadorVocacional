import threading
from flask import Flask
import gradio as gr

# Definir interfaz Gradio
def saludar(nombre):
    return f"Hola {nombre}! (App en plan F1)"

interfaz = gr.Interface(
    fn=saludar,
    inputs="text",
    outputs="text",
    title="App Gradio en F1",
    description="Versión simplificada para plan gratuito"
)

# Crear aplicación Flask para manejar la raíz
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "<h2>Bienvenido a la app Flask. Visita /gradio para abrir la interfaz Gradio.</h2>"

# Lanzar Gradio en un hilo aparte
def lanzar_gradio():
    interfaz.launch(server_name="0.0.0.0", server_port=7860, share=False, inbrowser=False)

# Ejecutar Flask como aplicación principal
if __name__ == "__main__":
    threading.Thread(target=lanzar_gradio).start()
    flask_app.run(host="0.0.0.0", port=8000)
else:
    # Para Azure: gunicorn usará esta app
    application = flask_app
    threading.Thread(target=lanzar_gradio).start()
