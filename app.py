from flask import Flask, session, redirect, url_for
from models.bd import inicializar_bd
from models.mail import configurar_mail
from routes.login import loginEmpleado_bp
from routes.empleados import empleados_bp
from routes.clientes import clientes_bp
from routes.agregarClientes import agregarClientes_bp
from routes.editarClientes import editarCliente_bp
from routes.eliminarClientes import eliminarCliente_bp
from routes.noticiasRecientes import noticiasRecientes_bp
from routes.sugerencias import sugerencias_bp
from routes.misSugerencias import misSugerencias_bp

#SE GENERA UNA CLAVE DE FLASK Y EL ENTORNO DE TRABAJO DE LA APP.
app = Flask(__name__)
app.secret_key = "claveSecreta"

#INICIALIZACION DE LA BD
mysql = inicializar_bd(app)

#INICIALIZACION DEL SERVIDOR DE MAILS
Mail = configurar_mail(app)

#SE REGISTRAN LOS BLUEPRINTS
app.register_blueprint(loginEmpleado_bp)
app.register_blueprint(empleados_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(agregarClientes_bp)
app.register_blueprint(editarCliente_bp)
app.register_blueprint(eliminarCliente_bp)
app.register_blueprint(noticiasRecientes_bp)
app.register_blueprint(sugerencias_bp)
app.register_blueprint(misSugerencias_bp)

#RUTA Y FUNCION DEL INICIO
@app.route('/')
def ingresoEmpleados():
    return redirect(url_for('login'))
    
#RUTA Y FUNCION PARA CERRAR SESION.
@app.route('/cerrar-sesion')
def cerrarSesion():
    session.pop('nombre')
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug = True,port = 5000, host = "0.0.0.0")