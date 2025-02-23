#SE IMPORTAN LAS LIBRERIAS A UTILIZAR EN EL PROYECTO.
from flask import Flask, render_template, request, session, redirect, url_for
from models.bd import inicializar_bd
from models.mail import configurar_mail


#SE GENERA UNA CLAVE DE FLASK Y EL ENTORNO DE TRABAJO DE LA APP.
app = Flask(__name__)
app.secret_key = "claveSecreta"

#INICIALIZACION DE LA BD
mysql = inicializar_bd(app)

#INICIALIZACION DEL SERVIDOR DE MAILS
Mail = configurar_mail(app)

#RUTA Y FUNCION DEL INICIO
@app.route('/')
def ingresoEmpleados():
    return redirect(url_for('login'))


#RUTA Y FUNCION PARA EL MENU DE EMPLEADOS.
@app.route('/empleados')
def empleados():
    nombre = session.get('nombre')
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('empleados.html',nombre = nombre)
    
    
#RUTA Y FUNCION PARA EL MANEJO DEL AGREGO DE CLIENTES.
@app.route('/agregar-clientes',methods = ['POST','GET'])
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


#RUTA Y FUNCION PARA EL LISTADO DE CLIENTES
@app.route('/listado-clientes', methods = ['GET','POST'])
def listadoClientes():
    if 'nombre' not in session:
        return redirect(url_for('login'))
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


#RUTA Y FUNCION PARA ELIMINAR CLIENTE.
@app.route('/eliminar-cliente', methods = ['POST','GET'])   
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
            
            return redirect(url_for('listadoClientes'))


#RUTA Y FUNCION PARA EDITAR UN CLIENTE.
@app.route('/editar-cliente',methods = ['POST','GET'])
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

#RUTA Y FUNCION PARA VER NOTICIAS RECIENTES
@app.route('/noticias-recientes')
def noticiasRecientes():
    noticias = []
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        conexion = mysql.connection.cursor()
        conexion.execute('SELECT * FROM noticias WHERE estado = "publicada"')
        noticias = conexion.fetchall()
        
        return render_template('noticiasRecientes.html',noticias = noticias)
    
#RUTA Y FUNCION PARA EL PANEL DE SUGERENCIAS
@app.route('/sugerencias')
def sugerencias():
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('sugerencias.html')
    
#RUTA Y FUNCION PARA INGRESAR SUGERENCIAS   
@app.route('/ingresar-sugerencias', methods = ['POST','GET'])
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

#RUTA Y FUNCION PARA VER LAS SUGERENCIAS Y SUS RESPUESTAS
@app.route('/mis-sugerencias', methods = ['POST','GET'])
def misSugerencias():
    sugerencias = []
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == "GET":
            conexion = mysql.connection.cursor()
            
            idEmpleado = session.get('id')
            
            conexion.execute("SELECT * FROM sugerencias WHERE id_empleado = %s",(idEmpleado,))
            sugerencias = conexion.fetchall()
            mysql.connection.commit()
    
    return render_template('misSugerencias.html',sugerencias = sugerencias)
   
#RUTA Y FUNCION PARA CERRAR SESION.
@app.route('/cerrar-sesion')
def cerrarSesion():
    session.pop('nombre')
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug = True,port = 5000, host = "0.0.0.0")