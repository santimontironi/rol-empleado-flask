from flask import Blueprint, request, session, render_template
from flask_mail import Message,Mail
from datetime import datetime
import random
from models.bd import mysql
from models.mail import mail
from werkzeug.security import generate_password_hash, check_password_hash #libreria para el hash de claves
import re # proporciona herramientas para trabajar con expresiones regulares. Las expresiones regulares son una poderosa herramienta para buscar, comparar y manipular cadenas de texto según patrones específicos.

loginEmpleado_bp = Blueprint('login',__name__)

#RUTA Y FUNCION LOGIN.
@loginEmpleado_bp.route('/ingreso-empleado', methods = ["GET","POST"])
def login():
    error = None
    errorClaveIncorrecta = None
    errorCodigoIncorrecto = None
    mostrarCodigo = False
    if request.method == "POST":
        correo = request.form['correo_ingreso']
        clave = request.form['clave_ingreso']
        codigo = request.form['codigo'] if 'codigo' in request.form else None
        
        conexion = mysql.connection.cursor()
        
        conexion.execute('SELECT * FROM registroempleados WHERE correo_registro = %s AND estado = "Activo"', (correo,))
        registro = conexion.fetchone()
        
        if registro and check_password_hash(registro['clave_registro'],clave):
            idEmpleado = registro['id']
            nombreEmpleado = registro['nombre']
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            #SE RECUPERA EL NOMBRE PARA PODER MOSTRARLO EN PANTALLA Y MANEJAR LA AUTENTICACION.
            session['nombre'] = nombreEmpleado
                
            #SE RECUPERA EL ID PARA POSTERIORES OPERACIONES
            session['id'] = idEmpleado
                
            conexion.execute('SELECT * FROM ingresoempleados WHERE id_empleado = %s',(idEmpleado,))
            registro_repetido = conexion.fetchone()

            if str(codigo).strip() == str(session.get('codigoVerificacion')).strip():
                #SI EL EMPLEADO QUE INGRESA YA INGRESÓ PREVIAMENTE SE ACTUALIZA LA FECHA Y HORA
                if registro_repetido:
                    conexion.execute('UPDATE ingresoempleados SET fechasesion = %s WHERE id_empleado = %s',(fecha,idEmpleado))
                else:
                    conexion.execute('INSERT INTO ingresoempleados(id_empleado,fechasesion) VALUES (%s,%s)',(idEmpleado,fecha))
                    
                mysql.connection.commit()
                    
                session.pop('codigoVerificacion',None) #elimina la clave 'codigoVerificacion' de la sesión si existe, y elargumento None asegura que no se genere un error en caso de que la clave no esté presente.
                    
                return render_template ('empleados.html',nombre = nombreEmpleado)
            else:
                errorCodigoIncorrecto = "Codigo incorrecto"
                mostrarCodigo = True 
        else:
            error = "Credenciales incorrectas."
            mostrarCodigo = True if session.get('codigoVerificacion') else None
            
    return render_template('formulario-empleado.html', error=error, errorClaveIncorrecta = errorClaveIncorrecta, errorCodigoIncorrecto = errorCodigoIncorrecto, mostrarCodigo = mostrarCodigo)

#RUTA Y FUNCION PARA CAMBIAR CLAVE.
@loginEmpleado_bp.route('/cambiar_clave', methods = ["GET","POST"])
def cambiarClave():
    errorCorreoInvalidoAlCambiarClave = None
    mensajeClaveNueva = None
    errorClaveInvalida = None
    inputCodigo = False
    if request.method == "POST":
        email = request.form['email']
        claveNueva = request.form['claveNueva']
        
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', claveNueva):
            errorClaveInvalida = "La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula y un número."
            return render_template('formulario-empleado.html', errorClaveInvalida = errorClaveInvalida)
        
        claveNuevaHash = generate_password_hash(claveNueva)
        
        conexion = mysql.connection.cursor()
        conexion.execute('SELECT * FROM registroempleados WHERE correo_registro = %s',(email,))
        
        empleado = conexion.fetchone()
        if empleado:
            conexion.execute('UPDATE registroempleados SET clave_registro = %s WHERE correo_registro = %s',(claveNuevaHash,email))
            mysql.connection.commit()
            
            codigo = random.randint(1000,9999)
            
            session['codigoVerificacion'] = codigo
            
            msg = Message("Codigo de verificación para cambio de clave.",
                          recipients=[email],
                          body=f"Hola {empleado['nombre']}. Su código de verificación es: {codigo}",
                          sender="fullweb10@gmail.com")
            
            mail.send(msg)
            mensajeClaveNueva = "Clave cambiada con éxito. Por favor inicie sesión ingresando correctamente el codigo enviado a su e-mail."
        
            inputCodigo = True
        else:
            errorCorreoInvalidoAlCambiarClave = "No existe un empleado con el correo proporcionado."
           
    return render_template('formulario-empleado.html', mensajeClaveNueva = mensajeClaveNueva, errorCorreoInvalidoAlCambiarClave = errorCorreoInvalidoAlCambiarClave, inputCodigo = inputCodigo)