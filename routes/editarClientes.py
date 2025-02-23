from flask import request,session,redirect,url_for,render_template,Blueprint
from models.bd import mysql

editarCliente_bp = Blueprint('editarCliente',__name__)

#RUTA Y FUNCION PARA EDITAR UN CLIENTE.
@editarCliente_bp.route('/editar-cliente',methods = ['POST','GET'])
def editarCliente():
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            idCliente = request.args.get('clienteId')
            conexion = mysql.connection.cursor()
            conexion.execute('SELECT * FROM proyectosclientes WHERE id_proyecto = %s',(idCliente,))
            cliente = conexion.fetchone()
            return render_template('editarClientes.html', cliente = cliente)
        else:
            idCliente = request.form['clienteId']
            tituloNuevo = request.form['tituloNuevo']
            infoNueva = request.form['infoNueva']
            estadoNuevo = request.form['estadoNuevo']
            
            conexion = mysql.connection.cursor()
            conexion.execute('UPDATE proyectosclientes SET titulo_proyecto = %s, descripcion_proyecto = %s,estado_proyecto = %s WHERE id_cliente = %s',(tituloNuevo,infoNueva,estadoNuevo,idCliente))
            mysql.connection.commit()

            return redirect(url_for('listadoClientes'))