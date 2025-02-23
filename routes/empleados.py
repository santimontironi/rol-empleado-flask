from flask import redirect,url_for,render_template,session,Blueprint

empleados_bp = Blueprint('empleados',__name__)

#RUTA Y FUNCION PARA EL MENU DE EMPLEADOS.
@empleados_bp.route('/empleados')
def empleados():
    nombre = session.get('nombre')
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('empleados.html',nombre = nombre)