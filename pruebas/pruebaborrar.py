from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/borrar', methods=['GET', 'POST'])
def borrar():
    if request.method == 'POST':
        name = request.form['name']
        # Aquí realizarías la lógica para eliminar la persona de la base de datos
        return f"Deleted person with name: {name}"
    
    # Servir el archivo HTML desde el directorio actual
    return send_from_directory(directory='.', path='borrar.html')

if __name__ == '__main__':
    app.run(debug=True)
