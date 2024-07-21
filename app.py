from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='postgres-service', 
            database='mydb', 
            user='myuser', 
            password='mypassword'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute('INSERT INTO people (name, email) VALUES (%s, %s)', (name, email))
                conn.commit()
                cur.close()
                conn.close()
                return render_template('success.html', action='added')
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                return render_template('success.html', action='error', message='Error al agregar la persona')
        else:
            return render_template('success.html', action='error', message='Error en la conexión a la base de datos')
    
    return render_template('add_person.html')

@app.route('/delete_person', methods=['GET', 'POST'])
def delete_person():
    if request.method == 'POST':
        name = request.form['name']
        
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute('SELECT email FROM people WHERE name = %s', (name,))
                result = cur.fetchone()
                
                if result:
                    # Persona encontrada
                    email = result[0]
                    cur.execute('DELETE FROM people WHERE name = %s', (name,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    return render_template('delete_person.html', message=f"Persona eliminada correctamente: Nombre: {name}, Correo: {email}")
                else:
                    # Persona no encontrada
                    cur.close()
                    conn.close()
                    return render_template('delete_person.html', message="No se ha borrado a nadie. La persona no existe.")
                    
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                return render_template('delete_person.html', message='Error al eliminar la persona')
        else:
            return render_template('delete_person.html', message='Error en la conexión a la base de datos')
    
    # Servir el archivo HTML desde el directorio actual si se accede por GET
    return render_template('delete_person.html')

@app.route('/get_people')
def get_people():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM people')
            people = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('get_people.html', people=people)
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return "Error al obtener la lista de personas"
    else:
        return "Error en la conexión a la base de datos"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
