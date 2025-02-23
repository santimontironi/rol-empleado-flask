from flask import redirect,url_for,render_template

#RUTA Y FUNCION PARA EL MENU DE EMPLEADOS.
@app.route('/empleados')
def empleados():
    nombre = session.get('nombre')
    if 'nombre' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('empleados.html',nombre = nombre)