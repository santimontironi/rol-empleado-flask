#RUTA Y FUNCION PARA EL LISTADO DE CLIENTES
from flask import session,request,redirect,url_for,render_template,Blueprint
from models.bd import mysql

clientes_bp = Blueprint('clientes',__name__)

@clientes_bp.route('/listado-clientes', methods = ['GET','POST'])
def listadoClientes():
    if 'nombre' not in session:
        return redirect(url_for('login.login'))
    else:   
        conexion = mysql.connection.cursor()
        if request.method == "GET":
            #Se hace un left join para mostrar por pantalla los registros de clientes (tabla left) y los de proyectosclientes (a la que se le hace el join) con sus registros que coincidan con el id de clientes.
            conexion.execute('''
                SELECT clientes.id, clientes.nombre, clientes.apellido, clientes.correo, clientes.telefono, proyectosclientes.titulo_proyecto, proyectosclientes.descripcion_proyecto,proyectosclientes.estado_proyecto
                FROM clientes
                JOIN proyectosclientes ON clientes.id = proyectosclientes.id_cliente
                WHERE clientes.activo = TRUE
            ''')
        else:
            inputBusqueda = request.form['busqueda']
            busqueda = '''
                SELECT clientes.id, clientes.nombre, clientes.apellido, clientes.correo, clientes.telefono, proyectosclientes.titulo_proyecto,proyectosclientes.descripcion_proyecto,proyectosclientes.estado_proyecto
                FROM clientes
                JOIN proyectosclientes ON clientes.id = proyectosclientes.id_cliente
                WHERE clientes.activo = true AND (clientes.nombre LIKE %s OR clientes.apellido LIKE %s OR clientes.correo LIKE %s OR clientes.telefono LIKE %s)
            '''
            resultado = f"%{inputBusqueda}%" #Ejemplo %sant%
            conexion.execute(busqueda,(resultado,resultado,resultado,resultado))
            
        clientes = conexion.fetchall()
    return render_template('listadoClientes.html',clientes = clientes)