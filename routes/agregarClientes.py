from flask import request,session,redirect,url_for,render_template,Blueprint
from models.bd import mysql

agregarClientes_bp = Blueprint('agregarClientes',__name__)

#RUTA Y FUNCION PARA EL MANEJO DEL AGREGO DE CLIENTES.
@agregarClientes_bp.route('/agregar-clientes',methods = ['POST','GET'])
def agregarClientes():
    mensaje = None
    mensajeError = None
    mensajeEnlace = None

    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == "POST":
            nombreCliente = request.form['nombre_cliente']
            apellidoCliente = request.form['apellido_cliente']
            correoCliente = request.form['correo_cliente']
            telefonoCliente = request.form['telefono_cliente']
            tituloProyecto = request.form['titulo_proyecto']
            proyectoCliente = request.form['nombre_proyecto']
            
            conexion = mysql.connection.cursor()
            
            # Se verifica que el cliente que se ingresa no se repita.
            conexion.execute('SELECT * FROM clientes WHERE activo = 1 AND (correo = %s or telefono = %s)',(correoCliente,telefonoCliente))
            clienteRepetido = conexion.fetchone()
        
            if clienteRepetido:
                mensajeError = "El cliente ya existe."
            else:
                conexion.execute('INSERT INTO clientes (nombre,apellido,correo,telefono) VALUES (%s,%s,%s,%s)',(nombreCliente,apellidoCliente,correoCliente,telefonoCliente))
                mysql.connection.commit()
                    
                # OBTENER EL ID DEL CLIENTE RECIEN INGRESADO.
                idCliente = conexion.lastrowid
                
                estadoProyecto = "En proceso"
            
                # Se ingresa en la tabla de proyectos el id del cliente el nombre del proyecto y el estado que por defecto es 'en proceso'.
                conexion.execute('INSERT INTO proyectosclientes (id_cliente,titulo_proyecto,descripcion_proyecto,estado_proyecto) VALUES (%s,%s,%s,%s)',(idCliente,tituloProyecto, proyectoCliente,estadoProyecto));
                mysql.connection.commit()
                
                mensaje = "Se ha ingresado el cliente correctamente."
                mensajeEnlace = "Ver listado de clientes"
        
    return render_template('agregarClientes.html', mensaje = mensaje, mensajeError = mensajeError, mensajeEnlace = mensajeEnlace)