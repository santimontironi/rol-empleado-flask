from flask import request,session,redirect,url_for,render_template,Blueprint
from models.bd import mysql

sugerencias_bp = Blueprint('sugerencias',__name__)


#RUTA Y FUNCION PARA EL PANEL DE SUGERENCIAS
@sugerencias_bp.route('/sugerencias')
def sugerencias():
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('sugerencias.html')
    
#RUTA Y FUNCION PARA INGRESAR SUGERENCIAS   
@sugerencias_bp.route('/ingresar-sugerencias', methods = ['POST','GET'])
def ingresarSugerencias():
    mensaje = None
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            titulo = request.form['titulo']
            sugerencia = request.form['sugerencia']
            
            idEmpleado = session.get('id')
            
            conexion = mysql.connection.cursor()
            
            conexion.execute('INSERT INTO sugerencias(id_empleado,titulo,sugerencia) VALUES (%s,%s,%s)',(idEmpleado,titulo,sugerencia))
            
            mensaje = "Se agregó la sugerencia correctamente."
            
            mysql.connection.commit()
            
    return render_template('ingresarSugerencias.html', mensaje = mensaje)