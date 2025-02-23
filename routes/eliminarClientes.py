from flask import request,session,redirect,url_for,render_template,Blueprint
from models.bd import mysql

eliminarCliente_bp = Blueprint('eliminarClientes',__name__)

#RUTA Y FUNCION PARA ELIMINAR CLIENTE.
@eliminarCliente_bp.route('/eliminar-cliente', methods = ['POST','GET'])   
def eliminarCliente():
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == "POST":
            clienteId = request.form['clienteId']
            
            conexion = mysql.connection.cursor()
            
            conexion.execute('UPDATE clientes SET activo = FALSE WHERE id = %s',(clienteId,))
            conexion.execute('UPDATE proyectosclientes SET activo = FALSE WHERE id_cliente = %s',(clienteId,))
            mysql.connection.commit()
            
            return redirect(url_for('clientes.listadoClientes'))
