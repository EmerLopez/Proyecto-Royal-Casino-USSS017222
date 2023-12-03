from flask import Flask, render_template, request, redirect, url_for, session, Response, make_response, render_template_string
import os
import database as db
from flask_mysqldb import MySQL,MySQLdb
import json
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

#Cargar Clientes Campos en Blanco
@app.route('/show_messageclientwhite/<mensaje_error>')
def show_messageclientwhite(mensaje_error):
  
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM clientes")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    text = 0
    return render_template('clientes.html', data=insertObject, mensaje_error=mensaje_error)

#Cargar Alerta Clientes
@app.route('/show_messageclient/<msg>')
def show_messageclient(msg):
  
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM clientes")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    text = 0
    return render_template('clientes.html', data=insertObject, msg=msg, tipo=1)
   
#Mensaje agregar cliente:
@app.route('/valclient',methods=['GET'])
def valclient():
    msg = "Cliente Ingresado con Exito!"
    return redirect(url_for('show_messageclient', msg=msg))

#Editar cliente:
@app.route('/msgclientedit',methods=['GET'])
def msgclientedit():
    msg = "Cliente Editado con Exito!"
    return redirect(url_for('show_messageclient',msg=msg))

#Eliminar cliente:
@app.route('/msgclientdelete',methods=['GET'])
def msgclientdelete():
    msg = "Cliente Eliminado con Exito!"
    return redirect(url_for('show_messageclient', msg=msg))

#Validacion campos en blanco:
@app.route('/valclientwhite',methods=['GET'])
def valclientwhite():
    mensaje_error = "Error: Campos en blanco, llena todos los campos"
    return redirect(url_for('show_messageclientwhite', mensaje_error=mensaje_error))
    
 #MENSAJES ADMINISTRADORES...                                          $$$$
 
  #Cargar Campos en blanco Administradores:
@app.route('/show_messageadminwhite/<mensaje_error>')
def show_messageadminwhite(mensaje_error):
  
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM administrador")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    text = 0
    return render_template('admin.html', data=insertObject, mensaje_error=mensaje_error)
 
 #Cargar Administradores:
@app.route('/show_messageadmin/<msg>')
def show_messageadmin(msg):
  
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM administrador")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    text = 0
    return render_template('admin.html', data=insertObject, msg=msg, tipo=1)

#Agregar Administrador:
@app.route('/msgadminadd',methods=['GET'])
def msgadminadd():
    msg = "Administrador Ingresado con Exito!"
    return redirect(url_for('show_messageadmin', msg=msg))

#Editar Administrador:
@app.route('/msgadminedit',methods=['GET'])
def msgadminedit():
    msg = "Administrador Editado con Exito!"
    return redirect(url_for('show_messageadmin', msg=msg))

#Eliminar Administrador:
@app.route('/msgadmindelete',methods=['GET'])
def msgadmindelete():
    msg = "Administrador Eliminado con Exito!"
    return redirect(url_for('show_messageadmin', msg=msg))

#Validar Campo en blanco:
@app.route('/whiteadmindelete',methods=['GET'])
def whiteadmindelete():
    mensaje_error = "Error: Campos en blanco, llena todos los campos"
    return redirect(url_for('show_messageadminwhite', mensaje_error=mensaje_error))

 #MENSAJES RESERVACIONES LOCAL... r_local                           $$$$
 
 #Carga error r_local:
@app.route('/show_messagelocale/<mensaje_error>')
def show_messagelocale(mensaje_error):
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM r_local")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('r_local.html', data=insertObject, mensaje_error=mensaje_error)
 
 #Carga r_local:
@app.route('/show_messagelocal/<msg>')
def show_messagelocal(msg):
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM r_local")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('r_local.html', data=insertObject, msg=msg, tipo=1)

#Agregar r_local:
@app.route('/msglocaladd',methods=['GET'])
def msglocaladd():
    msg = "Reservacion Ingresada con Exito!"
    return redirect(url_for('show_messagelocal', msg=msg))

#Editar r_local:
@app.route('/msglocaledit',methods=['GET'])
def msglocaledit():
    msg = "Reservacion Editada con Exito!"
    return redirect(url_for('show_messagelocal', msg=msg))

#Eliminar r_local:
@app.route('/msglocaldelete',methods=['GET'])
def msglocaldelete():
    msg = "Reservacion Eliminada con Exito!"
    return redirect(url_for('show_messagelocal', msg=msg))

#Validacion de fecha r_local:
@app.route('/vallocaladd',methods=['GET'])
def vallocaladd():
    mensaje_error = "Error al Guardar, fecha no disponible! "
    #return render_template('rmms.html', message_error=message_error)
    return redirect(url_for('show_messagelocale', mensaje_error=mensaje_error))

#Validacion de campos en blanco r_local:
@app.route('/whitelocaladd',methods=['GET'])
def whitelocaladd():
    mensaje_error = "Error: Campos en blanco, llena todos los campos"
    return redirect(url_for('show_messagelocale', mensaje_error=mensaje_error))

#MENSAJES RESERVACIONES DE Mesas, Manteles, ETC... rmms                 $$$

#Carga Error rmms:
@app.route('/show_messagermmsv/<mensaje_error>')
def show_messagermmsv(mensaje_error):
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM rmms")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('rmms.html', data=insertObject,mensaje_error=mensaje_error)
 
 #Carga rmms:
@app.route('/show_messagermms/<msg>')
def show_messagermms(msg):
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM rmms")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('rmms.html', data=insertObject, msg=msg, tipo=1)

#Agregar rmms:
@app.route('/msgrmmsadd',methods=['GET'])
def msgrmmsadd():
    msg = "Reservacion Ingresada con Exito!"
    return redirect(url_for('show_messagermms', msg=msg))

#Editar rmms:
@app.route('/msgrmmsedit',methods=['GET'])
def msgrmmsedit():
    msg = "Reservacion Editada con Exito!"
    return redirect(url_for('show_messagermms', msg=msg))

#Eliminar rmms:
@app.route('/msgrmmsdelete',methods=['GET'])
def msgrmmsdelete():
    msg = "Reservacion Eliminada con Exito!"
    return redirect(url_for('show_messagermms', msg=msg))

#Val fecha rmms:
@app.route('/valrmmsadd',methods=['GET'])
def valrmmsadd():
    mensaje_error = "Error al Guardar, fecha no disponible!"
    return redirect(url_for('show_messagermmsv', mensaje_error=mensaje_error))

#Val campos en blanco rmms:
@app.route('/valrmmswhite',methods=['GET'])
def valrmmswhite():
    mensaje_error = "Error: Campos en blanco, llena todos los campos"
    return redirect(url_for('show_messagermmsv', mensaje_error=mensaje_error))

#-----------------------------------------------------------------------------------
     


#---------------------------------------------------------------------------
#funciones rmms

@app.route('/rmms')
def rmms():
   
    search_term = request.args.get('search', '')  # Obtener el término de búsqueda de la URL
    cursor = db.database.cursor()

    if search_term:
        # Filtrar resultados si hay un término de búsqueda
        sql = "SELECT * FROM rmms WHERE nombres LIKE %s "
        data = ('%' + search_term + '%', '%' + search_term + '%')
        cursor.execute(sql, data)
    else:
        # Consulta sin filtrar si no hay término de búsqueda
        cursor.execute("SELECT * FROM rmms")

    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    return render_template('rmms.html', data=insertObject, search_term=search_term)

@app.route('/user', methods=['POST'])
def addUser():
    t_reservacion = request.form['t_reservacion'].strip()
    nombres = request.form['nombres'].strip()
    apellidos = request.form['apellidos'].strip()
    DUI = request.form['DUI'].strip()
    telefono = request.form['telefono'].strip()
    fecha = request.form['fecha'].strip()
    c_mesas = request.form['c_mesas'].strip()
    c_sillas = request.form['c_sillas'].strip()
    c_manteles = request.form['c_manteles'].strip()
    total = request.form['total'].strip()
    pago = request.form['pago'].strip()
    p_pendiente = request.form['pago'].strip()

    # Verifica si alguna de las variables después de aplicar strip() está vacía
    if not all([t_reservacion, nombres, apellidos, DUI, telefono, fecha, c_mesas, c_sillas, c_manteles, total, pago]):
        return redirect(url_for('valrmmswhite'))

    cursor = db.database.cursor()
    Cnombre = nombres
    select_query = "SELECT nombres, c_reservaciones FROM clientes WHERE nombres = %s"
    cursor.execute(select_query, (Cnombre,))
    result = cursor.fetchone()

    consulta = "SELECT * FROM rmms WHERE fecha = %s"
    valores = (fecha,)
    cursor.execute(consulta, valores)
    resultado = cursor.fetchone()

    if resultado:
        return redirect(url_for('valrmmsadd'))
    else:
        if result:
            NID, cantidad = result
            Ncantidad = cantidad + 1
            update_query = "UPDATE clientes SET c_reservaciones = %s WHERE nombres = %s"
            cursor.execute(update_query, (Ncantidad, NID,))
            db.database.commit()
            
        elif t_reservacion and nombres and apellidos and DUI and telefono and fecha and c_mesas and c_sillas and c_manteles and total and pago:
            cursor = db.database.cursor()
            sql = "INSERT INTO clientes (nombres, apellidos, DUI, telefono, p_pendiente, c_reservaciones) VALUES (%s, %s, %s, %s, %s, 1)"
            data = (nombres, apellidos, DUI, telefono, p_pendiente )
            cursor.execute(sql, data)
            db.database.commit()
            
        cursor = db.database.cursor()
        sql = "INSERT INTO rmms (t_reservacion, nombres, apellidos, DUI, telefono, fecha, c_mesas, c_sillas, c_manteles, total, pago) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (t_reservacion, nombres, apellidos, DUI, telefono, fecha, c_mesas, c_sillas, c_manteles, total, pago)
        cursor.execute(sql, data)
        db.database.commit() 
    return redirect(url_for('msgrmmsadd'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    select_query = "SELECT nombres FROM rmms WHERE id = %s"
    cursor.execute(select_query, (id,))
    result = cursor.fetchone()

    if result:
        cliente_nombre = result[0]

        # Resta 1 a la cantidad de reservaciones del cliente
        update_query = "UPDATE clientes SET c_reservaciones = c_reservaciones - 1 WHERE nombres = %s"
        cursor.execute(update_query, (cliente_nombre,))
        db.database.commit()

        # Elimina el registro de r_local
        delete_query = "DELETE FROM rmms WHERE id=%s"
        cursor.execute(delete_query, (id,))
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
    search_term = request.args.get('search', '')  # Obtener el término de búsqueda de la URL
    cursor = db.database.cursor()

    if search_term:
        # Filtrar resultados si hay un término de búsqueda
        sql = "SELECT * FROM r_local WHERE nombres LIKE %s "
        data = ('%' + search_term + '%', '%' + search_term + '%')
        cursor.execute(sql, data)
    else:
        # Consulta sin filtrar si no hay término de búsqueda
        cursor.execute("SELECT * FROM r_local")

    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    return render_template('r_local.html', data=insertObject, search_term=search_term)

@app.route('/userlocal', methods=['POST'])
def addUserlocal():
    nombres = request.form['nombres'].strip()
    apellidos = request.form['apellidos'].strip()
    DUI = request.form['DUI'].strip()
    telefono = request.form['telefono'].strip()
    t_reservacion = request.form['t_reservacion'].strip()
    fecha = request.form['fecha'].strip()
    total = request.form['total'].strip()
    pago = request.form['pago'].strip()
    p_pendiente = request.form['pago'].strip()
    
    if not all([nombres, apellidos, DUI, telefono, t_reservacion, fecha, total, pago , p_pendiente]):
        return redirect(url_for('valrmmswhite'))
    
    cursor = db.database.cursor()
    Cnombre = nombres
    select_query = "SELECT nombres, c_reservaciones FROM clientes WHERE nombres = %s"
    cursor.execute(select_query, (Cnombre,))
    result = cursor.fetchone()
    
    consulta = "SELECT * FROM r_local WHERE fecha = %s"
    valores = (fecha,)
    cursor.execute(consulta, valores,)
    resultado = cursor.fetchone()
    
    #R_local
    if resultado:
       return redirect(url_for('vallocaladd'))   
    else:        
        if result:
            NID, cantidad = result
            Ncantidad = cantidad + 1
            update_query = "UPDATE clientes SET c_reservaciones = %s WHERE nombres = %s"
            cursor.execute(update_query, (Ncantidad, NID,))
            db.database.commit()
            
        elif nombres and apellidos and DUI and telefono and t_reservacion and fecha and total and pago and p_pendiente: 
            cursor = db.database.cursor()
            sql = "INSERT INTO clientes (nombres, apellidos, DUI, telefono, p_pendiente, c_reservaciones) VALUES (%s, %s, %s, %s, %s, 1)"
            data = (nombres, apellidos, DUI, telefono, p_pendiente )
            cursor.execute(sql, data)
            db.database.commit()
            
        cursor = db.database.cursor()
        sql = "INSERT INTO r_local (nombres, apellidos, DUI, telefono, t_reservacion, fecha, total, pago) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (nombres, apellidos, DUI, telefono, t_reservacion, fecha, total, pago)
        cursor.execute(sql, data)
        db.database.commit() 
        del resultado
    return redirect(url_for('msglocaladd'))
    
    
        

@app.route('/deletelocal/<string:id>')
def deletelocal(id):
    cursor = db.database.cursor()
    select_query = "SELECT nombres FROM r_local WHERE id = %s"
    cursor.execute(select_query, (id,))
    result = cursor.fetchone()

    if result:
        cliente_nombre = result[0]

        # Resta 1 a la cantidad de reservaciones del cliente
        update_query = "UPDATE clientes SET c_reservaciones = c_reservaciones - 1 WHERE nombres = %s"
        cursor.execute(update_query, (cliente_nombre,))
        db.database.commit()

        # Elimina el registro de r_local
        delete_query = "DELETE FROM r_local WHERE id=%s"
        cursor.execute(delete_query, (id,))
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
     
    search_term = request.args.get('search', '')  # Obtener el término de búsqueda de la URL
    cursor = db.database.cursor()

    if search_term:
        # Filtrar resultados si hay un término de búsqueda
        sql = "SELECT * FROM administrador WHERE correo LIKE %s "
        data = ('%' + search_term + '%', '%' + search_term + '%')
        cursor.execute(sql, data)
    else:
        # Consulta sin filtrar si no hay término de búsqueda
        cursor.execute("SELECT * FROM administrador")

    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    return render_template('admin.html', data=insertObject, search_term=search_term) 


@app.route('/useradmin', methods=['POST'])
def useradmin():
    correo = request.form['correo'].strip()
    password = request.form['password'].strip()
    
     # Verifica si alguna de las variables después de aplicar strip() está vacía
    if not all([correo, password]):
        return redirect(url_for('whiteadmindelete'))
    
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
    search_term = request.args.get('search', '')  # Obtener el término de búsqueda de la URL
    cursor = db.database.cursor()

    if search_term:
        # Filtrar resultados si hay un término de búsqueda
        sql = "SELECT * FROM clientes WHERE nombres LIKE %s "
        data = ('%' + search_term + '%', '%' + search_term + '%')
        cursor.execute(sql, data)
    else:
        # Consulta sin filtrar si no hay término de búsqueda
        cursor.execute("SELECT * FROM clientes")

    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    return render_template('clientes.html', data=insertObject, search_term=search_term)


@app.route('/userclient', methods=['POST'])
def userclient():
    nombres = request.form['nombres'].strip()
    apellidos = request.form['apellidos'].strip()
    DUI = request.form['DUI'].strip()
    telefono = request.form['telefono'].strip()
    p_pendiente = request.form['p_pendiente'].strip()
    c_reservaciones = request.form['c_reservaciones'].strip()
    
    # Verifica si alguna de las variables después de aplicar strip() está vacía
    if not all([nombres, apellidos,DUI, telefono, p_pendiente, c_reservaciones]):
        return redirect(url_for('valclientwhite'))
    
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
    
#----------------------------------------------------------------------------------