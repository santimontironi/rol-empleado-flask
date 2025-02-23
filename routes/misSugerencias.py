from flask import request,session,redirect,url_for,render_template,Blueprint
from models.bd import mysql

misSugerencias_bp = Blueprint('misSugerencias',__name__)

#RUTA Y FUNCION PARA VER LAS SUGERENCIAS Y SUS RESPUESTAS
@misSugerencias_bp.route('/mis-sugerencias', methods = ['POST','GET'])
def misSugerencias():
    sugerencias = []
    if 'nombre' not in session:
        return redirect(url_for('login.login'))
    else:
        if request.method == "GET":
            conexion = mysql.connection.cursor()
            
            idEmpleado = session.get('id')
            
            conexion.execute("SELECT * FROM sugerencias WHERE id_empleado = %s",(idEmpleado,))
            sugerencias = conexion.fetchall()
            mysql.connection.commit()
    
    return render_template('misSugerencias.html',sugerencias = sugerencias)