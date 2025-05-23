import gradio as gr

def saludar(nombre):
    return f"Hola {nombre}! (App en plan F1)"

app = gr.Interface(
    fn=saludar,
    inputs="text",
    outputs="text",
    title="App Gradio en F1",
    description="Versión simplificada para plan gratuito"
)

# Configuración específica para Azure F1
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=8000, share=False)
else:
    # Para el despliegue en Azure
    application = app
