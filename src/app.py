from flask import Flask, render_template, request, redirect, url_for, session, Response, make_response, render_template_string
import os
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import database as db
from flask_mysqldb import MySQL,MySQLdb
from jinja2 import Environment, FileSystemLoader


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder=template_dir)

IMG_FOLDER = os.path.join("src", "static", "img")
app.config["UPLOAD_FOLDER"] = IMG_FOLDER 

@app.route("/")
def Display_IMG():
    Logo = os.path.join(app.config["UPLOAD_FOLDER"], "logo.png")
    return render_template("login.html",user_image = Logo)


@app.route('/cabecera')
def cabecera():
    return render_template('cabecera.html') 

@app.route('/index')
def index():
    #message = "Este es un mensaje flotante"
    #return render_template('index.html', message=message)
 return render_template('index.html') 

#--------------------------------------------------------------------------
#MENSAJES FLOTANTES

#MENSAJES CLIENTES...                                           $$$$

#Cargar Clientes
@app.route('/show_messageclient/<message>')
def show_messageclient(message):
  
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM clientes")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    text = 0
    return render_template('clientes.html', data=insertObject, message=message)
   
#Mensaje agregar cliente:
@app.route('/valclient',methods=['GET'])
def valclient():
    message = "Cliente Ingresado con Exito!"
    return redirect(url_for('show_messageclient', message=message))

#Editar cliente:
@app.route('/msgclientedit',methods=['GET'])
def msgclientedit():
    message = "Cliente Editado con Exito!"
    return redirect(url_for('show_messageclient', message=message))

#Eliminar cliente:
@app.route('/msgclientdelete',methods=['GET'])
def msgclientdelete():
    message = "Cliente Eliminado con Exito!"
    return redirect(url_for('show_messageclient', message=message))
    
 #MENSAJES ADMINISTRADORES...                                          $$$$
 
 #Cargar Administradores:
@app.route('/show_messageadmin/<message>')
def show_messageadmin(message):
  
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM administrador")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    text = 0
    return render_template('admin.html', data=insertObject, message=message)

#Agregar Administrador:
@app.route('/msgadminadd',methods=['GET'])
def msgadminadd():
    message = "Administrador Ingresado con Exito!"
    return redirect(url_for('show_messageadmin', message=message))

#Editar Administrador:
@app.route('/msgadminedit',methods=['GET'])
def msgadminedit():
    message = "Administrador Editado con Exito!"
    return redirect(url_for('show_messageadmin', message=message))

#Eliminar Administrador:
@app.route('/msgadmindelete',methods=['GET'])
def msgadmindelete():
    message = "Administrador Eliminado con Exito!"
    return redirect(url_for('show_messageadmin', message=message))

 #MENSAJES RESERVACIONES LOCAL... r_local                           $$$$
 
 #Carga r_local:
@app.route('/show_messagelocal/<message>')
def show_messagelocal(message):
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM r_local")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('r_local.html', data=insertObject, message=message)

#Agregar r_local:
@app.route('/msglocaladd',methods=['GET'])
def msglocaladd():
    message = "Reservacion Ingresada con Exito!"
    return redirect(url_for('show_messagelocal', message=message))

#Editar r_local:
@app.route('/msglocaledit',methods=['GET'])
def msglocaledit():
    message = "Reservacion Editada con Exito!"
    return redirect(url_for('show_messagelocal', message=message))

#Eliminar r_local:
@app.route('/msglocaldelete',methods=['GET'])
def msglocaldelete():
    message = "Reservacion Eliminada con Exito!"
    return redirect(url_for('show_messagelocal', message=message))

#MENSAJES RESERVACIONES DE Mesas, Manteles, ETC... rmms                 $$$
 
 #Carga rmms:
@app.route('/show_messagermms/<message>')
def show_messagermms(message):
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM rmms")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('rmms.html', data=insertObject, message=message)

#Agregar rmms:
@app.route('/msgrmmsadd',methods=['GET'])
def msgrmmsadd():
    message = "Reservacion Ingresada con Exito!"
    return redirect(url_for('show_messagermms', message=message))

#Editar rmms:
@app.route('/msgrmmsedit',methods=['GET'])
def msgrmmsedit():
    message = "Reservacion Editada con Exito!"
    return redirect(url_for('show_messagermms', message=message))

#Eliminar rmms:
@app.route('/msgrmmsdelete',methods=['GET'])
def msgrmmsdelete():
    message = "Reservacion Eliminada con Exito!"
    return redirect(url_for('show_messagermms', message=message))

#-----------------------------------------------------------------------------------
     


#---------------------------------------------------------------------------
#funciones rmms

@app.route('/rmms')
def rmms():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM rmms")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('rmms.html', data=insertObject)

@app.route('/user', methods=['POST'])
def addUser():
    t_reservacion = request.form['t_reservacion']
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    DUI = request.form['DUI']
    telefono = request.form['telefono']
    fecha = request.form['fecha']
    c_mesas = request.form['c_mesas']
    c_sillas = request.form['c_sillas']
    c_manteles = request.form['c_manteles']
    total = request.form['total']
    pago = request.form['pago']
    
    if t_reservacion and nombres and apellidos and DUI and telefono and fecha and c_mesas and c_sillas and c_manteles and total and pago:
        cursor = db.database.cursor()
        sql = "INSERT INTO rmms (t_reservacion, nombres, apellidos, DUI, telefono, fecha, c_mesas, c_sillas, c_manteles, total, pago) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        data = (t_reservacion, nombres, apellidos, DUI, telefono, fecha, c_mesas, c_sillas, c_manteles, total, pago)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('msgrmmsadd'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM rmms WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('msgrmmsdelete'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    t_reservacion = request.form['t_reservacion']
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    DUI = request.form['DUI']
    telefono = request.form['telefono']
    fecha = request.form['fecha']
    c_mesas = request.form['c_mesas']
    c_sillas = request.form['c_sillas']
    c_manteles = request.form['c_manteles']
    total = request.form['total']
    pago = request.form['pago']
    

    if t_reservacion and nombres and apellidos and DUI and telefono and fecha and c_mesas and c_sillas and c_manteles and total and pago:
        cursor = db.database.cursor()
        sql = "UPDATE rmms SET t_reservacion=%s, nombres=%s, apellidos=%s, Dui=%s, telefono=%s, fecha=%s, c_mesas=%s, c_sillas=%s, c_manteles=%s, total=%s, pago=%s WHERE id=%s"

        data = (t_reservacion, nombres, apellidos, DUI, telefono, fecha, c_mesas, c_sillas, c_manteles, total, pago,id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msgrmmsedit'))
    
#--------------------------------------------------------------------
#r_local

@app.route('/r_local')
def local():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM r_local")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('r_local.html', data=insertObject)

@app.route('/userlocal', methods=['POST'])
def addUserlocal():
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    DUI = request.form['DUI']
    telefono = request.form['telefono']
    t_reservacion = request.form['t_reservacion']
    fecha = request.form['fecha']
    total = request.form['total']
    pago = request.form['pago']
    
    
    if nombres and apellidos and DUI and telefono and t_reservacion and fecha and total and pago :
        cursor = db.database.cursor()
        sql = "INSERT INTO r_local (nombres, apellidos, DUI, telefono, t_reservacion, fecha, total, pago) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (nombres, apellidos, DUI, telefono, t_reservacion, fecha, total, pago)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('msglocaladd'))

@app.route('/deletelocal/<string:id>')
def deletelocal(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM r_local WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('msglocaldelete'))

@app.route('/editlocal/<string:id>', methods=['POST'])
def editlocal(id):
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    DUI = request.form['DUI']
    telefono = request.form['telefono']
    t_reservacion = request.form['t_reservacion']
    fecha = request.form['fecha']
    total = request.form['total']
    pago = request.form['pago']
    

    if nombres and apellidos and DUI and telefono and t_reservacion and fecha and total and pago :
        cursor = db.database.cursor()
        sql = "UPDATE r_local SET nombres=%s, apellidos=%s, DUI=%s, telefono=%s, t_reservacion=%s, fecha=%s, total=%s, pago=%s WHERE id=%s"
        data = (nombres, apellidos, DUI, telefono, t_reservacion, fecha, total, pago, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msglocaledit'))

#-------------------------------------------------------------------------
#login

cursor = db.database.cursor()

@app.route('/acceso-login', methods=['POST'])
def login_post():
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']

    # Consulta para verificar las credenciales
    cursor.execute("SELECT * FROM administrador WHERE correo=%s AND password=%s", (correo, password))
    result = cursor.fetchone()

    if result:
        session['correo'] = correo
        message = "Inicio de Sesion con Exito!"
        return render_template('index.html', message=message)
    elif(correo == ''or password == ''):
        return render_template('login.html',mensaje="Campos vacios, ingrese sus credenciales")
    else:
        return render_template('login.html',mensaje="Usuario o Contraseña Incorrecta, Intentelo de nuevo")
     
     
      
#--------------------------------------



#--------------------------------------------------------------------------------
#Administradores


@app.route('/admin')
def admin():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM administrador")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('admin.html', data=insertObject)   


@app.route('/useradmin', methods=['POST'])
def useradmin():
    correo = request.form['correo']
    password = request.form['password']
    
    if correo and password:
        cursor=db.database.cursor()
        sql= "INSERT INTO administrador ( correo, password) VALUES (%s, %s)"
        data = ( correo, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('msgadminadd'))

@app.route('/deleteadmin/<string:id>')
def deleteadmin(id):
    cursor=db.database.cursor()
    sql= "DELETE FROM administrador WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('msgadmindelete'))
    
@app.route('/editadmin/<string:id>', methods=['POST'])
def editadmin(id):

     correo = request.form['correo']
     password = request.form['password']
    
     if  correo and password:
       cursor = db.database.cursor()
       sql = "UPDATE administrador SET  correo=%s, password=%s WHERE id=%s"
       data = (correo, password, id)
       cursor.execute(sql, data)
       db.database.commit()
     return redirect(url_for('msgadminedit'))
#--------------------------------------------------------------------------------------
#Clientes

@app.route('/clientes')
def clientes():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM clientes")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('clientes.html', data=insertObject)


@app.route('/userclient', methods=['POST'])
def userclient():
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    DUI = request.form['DUI']
    telefono = request.form['telefono']
    p_pendiente = request.form['p_pendiente']
    c_reservaciones = request.form['c_reservaciones']
    
    if nombres and apellidos and DUI and telefono and p_pendiente and c_reservaciones :
        cursor = db.database.cursor()
        sql = "INSERT INTO clientes (nombres, apellidos, DUI, telefono, p_pendiente, c_reservaciones) VALUES (%s, %s, %s, %s, %s, %s)"

        data = (nombres, apellidos, DUI, telefono, p_pendiente, c_reservaciones)
        cursor.execute(sql, data)
        db.database.commit()
       
    return redirect(url_for('valclient'))
    
@app.route('/deleteclient/<string:id>')
def deleteclient(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM clientes WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('msgclientdelete'))

@app.route('/editclient/<string:id>', methods=['POST'])
def editclient(id):
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    DUI = request.form['DUI']
    telefono = request.form['telefono']
    p_pendiente = request.form['p_pendiente']
    c_reservaciones = request.form['c_reservaciones']
    

    if nombres and apellidos and DUI and telefono and p_pendiente and  c_reservaciones:
        cursor = db.database.cursor()
        sql = "UPDATE clientes SET nombres=%s, apellidos=%s, DUI=%s, telefono=%s, p_pendiente=%s, c_reservaciones=%s WHERE id=%s"

        data = (nombres, apellidos, DUI, telefono, p_pendiente, c_reservaciones, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msgclientedit'))
#----------------------------------------------------------------------------------

if __name__ == '__main__':
    app.secret_key = "12345"
    app.run(debug=True, port=7000)
    
