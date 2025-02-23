from flask import Flask, session, redirect, url_for
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
    
#RUTA Y FUNCION PARA CERRAR SESION.
@app.route('/cerrar-sesion')
def cerrarSesion():
    session.pop('nombre')
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug = True,port = 5000, host = "0.0.0.0")