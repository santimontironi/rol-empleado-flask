from flask import request,session,redirect,url_for,render_template,Blueprint
from models.bd import mysql

noticiasRecientes_bp = Blueprint('noticiasRecientes',__name__)

#RUTA Y FUNCION PARA VER NOTICIAS RECIENTES
@noticiasRecientes_bp.route('/noticias-recientes')
def noticiasRecientes():
    noticias = []
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        conexion = mysql.connection.cursor()
        conexion.execute('SELECT * FROM noticias WHERE estado = "publicada"')
        noticias = conexion.fetchall()
        
        return render_template('noticiasRecientes.html',noticias = noticias)