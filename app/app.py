from flask import Flask, render_template, url_for, request, flash, redirect, session

import mysql.connector


app = Flask (__name__)
app.secret_key = '73901147'

config = {

   'host' : 'localhost',

   'user' : 'root',

   'password' : '',

   'database' : 'login_db',
   

}

cnx = mysql.connector.connect(**config)




@app.route('/Bienvenido')
def Bienvenido():
    return render_template('ingreso.html')

@app.route('/verificacion')
def verificacion():
    return render_template('verificacion.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
       Correo = request.form['Correo']
       Password = request.form['Password']
       
       cursor = cnx.cursor(dictionary=True)
       query = "SELECT id, Correo, Nombres, Passwordd FROM Usuario where Correo = %s"
       cursor.execute(query, (Correo,))
       user = cursor.fetchone()
       cursor.close()
       
       if user and user['Passwordd'] == Password:
           session['id_user'] = user['id']
           return redirect(url_for('Bienvenido'))
       else:
            flash('Ingreso Incorrecto, intente otra vez', 'danger')
            
    return render_template('login.html')
  


@app.route('/registrarse', methods = ['GET', 'POST'])
def registro():
    if request.method == 'POST':
        Correo = request.form['Correo']
        Nombres = request.form['Nombres']
        Password = request.form['Password']
        
        cursor = cnx.cursor(dictionary=True)
        query = "select * from Usuario where Correo = %s"
        cursor.execute(query, (Correo, ))
        existe_user = cursor.fetchone()
        cursor.close()
        
        if existe_user:
            flash('El correo ya esta registrado', 'danger')
        else :
            cursor = cnx.cursor()
            query = "INSERT INTO Usuario (Correo, Passwordd, Nombres) VALUES (%s, %s, %s)"
            cursor.execute(query, (Correo, Password, Nombres))
            cnx.commit()
            cursor.close()
        
            flash('Registro exitoso')
            return redirect(url_for('login'))
        
    return render_template('Registrarse.html')



        
@app.route('/recuperar', methods = ['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        Correo = request.form['Correo']
        
        cursor = cnx.cursor(dictionary=True)
        query = "select id, Correo from Usuario where Correo = %s"
        cursor.execute(query, (Correo,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
           session['id_user'] = user['id']
           return redirect(url_for('verificacion'))
        else:
            flash('Correo no encontrado', 'danger')
    
    return render_template('Recuperar.html')

@app.route('/cambiar', methods = ['GET', 'POST'])
def cambiar():
    if 'id_user' not in session:
        flash('Debes iniciar primero', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        antes_password = request.form['antes_password']
        nueva_password = request.form['nueva_password']
        id_user = session['id_user']
        
        cursor = cnx.cursor(dictionary=True)
        query = "select * from Usuario where id = %s"
        cursor.execute(query, (id_user,))
        data = cursor.fetchone()
        cursor.close()
        
        if antes_password == data['Passwordd']:
            cursor = cnx.cursor()
            update_query = "update Usuario set Passwordd = %s where id = %s"
            cursor.execute(update_query, (nueva_password, id_user))
            cnx.commit()
            cursor.close()
            
            flash('Contraseña actualizada', 'success')
        else :
            flash('Contraseña actual incorrecta', 'danger')
    return render_template('Cambiar.html')




if __name__ == '__main__':
    app.run(debug=True, port = 5000)
    