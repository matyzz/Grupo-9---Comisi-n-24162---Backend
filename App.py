from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
from flask_mysqldb import MySQL, MySQLdb
import os

app = Flask(__name__)

# Conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'backend_proyecto'
mysql = MySQL(app)

# Configs
app.secret_key = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Galeria
@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

# Info
@app.route('/informacion')
def informacion():
    return render_template('informacion.html')

# Servicios
@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

# Contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            telefono = request.form['telefono']
            domicilio = request.form['domicilio']
            suscripcion = 'suscrito' if 'suscripcion' in request.form else 'no suscrito'

            if not nombre or not correo or not telefono or not domicilio:
                flash('Por favor, completa todos los campos', 'error')
                return redirect(url_for('contacto'))

            archivo = request.files['archivo']
            if archivo and archivo.filename != '':
                archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename))

            cur = mysql.connection.cursor()
            cur.execute('''
                INSERT INTO contacto (nombre, correo, telefono, domicilio, suscripcion) 
                VALUES (%s, %s, %s, %s, %s)
            ''', (nombre, correo, telefono, domicilio, suscripcion))
            mysql.connection.commit()
            flash('Contacto enviado satisfactoriamente', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al enviar el contacto: {e}', 'error')
        finally:
            cur.close()
        return redirect(url_for('contacto'))
    return render_template('contacto.html')

# Login
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['pass']

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        usuario_data = cur.fetchone()

        if usuario_data:
            if contraseña == usuario_data[2]:
                session['logged_in'] = True
                flash('Inicio de sesión exitoso!', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Contraseña incorrecta. Por favor, inténtalo nuevamente.', 'error')
                return redirect(url_for('index'))
        else:
            flash('Usuario no encontrado. Por favor, regístrate o verifica tus datos.', 'error')
            return redirect(url_for('index'))

        cur.close()

# Bloqueo de login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Acceso no autorizado. Por favor, inicia sesión primero.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Panel Admin
@app.route('/admin')
@login_required
def admin():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacto')
    data = cur.fetchall()
    cur.close()
    return render_template('admin.html', contactos=data)

# Boton editar con requerimiento de login
@app.route('/edit/<id>')
@login_required
def get_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacto WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    return render_template('editar_contacto.html', contacto=data[0])

# Boton Actualizar datos con requerimiento de login
@app.route('/update/<id>', methods=['POST'])
@login_required
def actualizar_contacto(id):
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            telefono = request.form['telefono']
            domicilio = request.form['domicilio']

            if not nombre or not correo or not telefono or not domicilio:
                flash('Por favor, completa todos los campos', 'error')
                return redirect(url_for('contacto'))
    
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE contacto
                SET nombre = %s,
                    correo = %s,
                    telefono = %s,
                    domicilio = %s
                WHERE id = %s
            """, (nombre, correo, telefono, domicilio, id))
            mysql.connection.commit()
            flash('Contacto editado satisfactoriamente', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al enviar el contacto: {e}', 'error')
        finally:
            cur.close()
        return redirect(url_for('admin'))
    return render_template('admin.html')

# Boton Borrar con requerimiento de login
@app.route('/delete/<string:id>')
@login_required
def eliminar_contacto(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM contacto WHERE id = %s', (id,))
        mysql.connection.commit()
        flash('Contacto eliminado satisfactoriamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar el contacto: {e}', 'error')
    finally:
        cur.close()
    return redirect(url_for('admin'))

# Cerrar sesion
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('index'))

# Config y carpeta update del formulario
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(port=3000, debug=True)
