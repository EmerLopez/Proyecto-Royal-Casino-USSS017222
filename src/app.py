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
    
    cursor = db.database.cursor()
    Cnombre = nombres
    select_query = "SELECT nombres, c_reservaciones FROM clientes WHERE nombres = %s"
    cursor.execute(select_query, (Cnombre,))
    result = cursor.fetchone()

    consulta = "SELECT * FROM rmms WHERE fecha = %s"
    valores = (fecha,)
    cursor.execute(consulta, valores)
    resultado = cursor.fetchone()
    
    #Variable booleana en caso de que todas las condiciones sean falsas:
    if_true = False

    # Verifica si alguna de las variables después de aplicar strip() está vacía
    if not all([t_reservacion, nombres, apellidos, DUI, telefono, fecha, c_mesas, c_sillas, c_manteles, total, pago]):
        if_true = True
        mensaje_error = "Error: Campo en blanco, llena todos los campos"
        search_term = request.args.get('search', '')
        data = datos_rmms(search_term)
        return render_template('rmms.html', mensaje_error=mensaje_error, 
                               t_reservacion=t_reservacion,
                               nombres=nombres,
                               apellidos=apellidos,
                               DUI=DUI,
                               telefono=telefono,
                               fecha=fecha, 
                               c_mesas=c_mesas,
                               c_sillas=c_sillas,
                               c_manteles=c_manteles,
                               total=total,
                               pago=pago,
                               data=data, search_term=search_term)
        
    elif not (DUI.replace('.', '', 1).isdigit() and total.replace('.', '', 1).isdigit() and telefono.replace('.', '', 1).isdigit() and c_mesas.replace('.', '', 1).isdigit() and c_sillas.replace('.', '', 1).isdigit() and c_manteles.replace('.', '', 1).isdigit()):
        mensaje_error = "Error: Datos Invalidos!"
        search_term = request.args.get('search', '')
        data = datos_rmms(search_term)
        return render_template('rmms.html', mensaje_error=mensaje_error, 
                               t_reservacion=t_reservacion,
                               nombres=nombres,
                               apellidos=apellidos,
                               DUI=DUI,
                               telefono=telefono,
                               fecha=fecha, 
                               c_mesas=c_mesas,
                               c_sillas=c_sillas,
                               c_manteles=c_manteles,
                               total=total,
                               pago=pago,
                               data=data, search_term=search_term) 

    else:
        if result:
            if_true = True
            NID, cantidad = result
            Ncantidad = cantidad + 1
            update_query = "UPDATE clientes SET c_reservaciones = %s WHERE nombres = %s"
            cursor.execute(update_query, (Ncantidad, NID,))
            db.database.commit()
            
        elif t_reservacion and nombres and apellidos and DUI and telefono and fecha and c_mesas and c_sillas and c_manteles and total and pago:
            if_true = True
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
    
        if  if_true == True:
            return redirect(url_for('msgrmmsadd'))
        else:
            mensaje_error = "Error al Guardar, Intentelo de nuevo"
            search_term = request.args.get('search', '')
            data = datos_rmms(search_term)
            return render_template('rmms.html', mensaje_error=mensaje_error, 
                               t_reservacion=t_reservacion,
                               nombres=nombres,
                               apellidos=apellidos,
                               DUI=DUI,
                               telefono=telefono,
                               fecha=fecha, 
                               c_mesas=c_mesas,
                               c_sillas=c_sillas,
                               c_manteles=c_manteles,
                               total=total,
                               pago=pago,
                               data=data, search_term=search_term)


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
    else:
        mensaje_error = "Error al Eliminar, Intentelo de nuevo"
        search_term = request.args.get('search', '')
        data = datos_rmms(search_term)
        return render_template('rmms.html', mensaje_error=mensaje_error,
                               data=data, search_term=search_term)

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
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
    
    if not all([t_reservacion, nombres, apellidos, DUI, telefono, fecha, c_mesas, c_sillas, c_manteles, total, pago]):
        mensaje_error = "Error: Campo en blanco, llena todos los campos"
        search_term = request.args.get('search', '')
        data = datos_rmms(search_term)
        return render_template('rmms.html', mensaje_error=mensaje_error, 
                               data=data, search_term=search_term)
        
    if t_reservacion and nombres and apellidos and DUI and telefono and fecha and c_mesas and c_sillas and c_manteles and total and pago:
        cursor = db.database.cursor()
        sql = "UPDATE rmms SET t_reservacion=%s, nombres=%s, apellidos=%s, Dui=%s, telefono=%s, fecha=%s, c_mesas=%s, c_sillas=%s, c_manteles=%s, total=%s, pago=%s WHERE id=%s"

        data = (t_reservacion, nombres, apellidos, DUI, telefono, fecha, c_mesas, c_sillas, c_manteles, total, pago,id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msgrmmsedit'))
    else:
        mensaje_error = "Error al Editar, Intentelo de nuevo"
        search_term = request.args.get('search', '')
        data = datos_rmms(search_term)
        return render_template('rmms.html', mensaje_error=mensaje_error, 
                               data=data, search_term=search_term)
    
def datos_rmms(search_term=''):
    cursor = db.database.cursor()

    if search_term:
        sql = "SELECT * FROM rmms WHERE nombres LIKE %s "
        data = ('%' + search_term + '%', '%' + search_term + '%')
        cursor.execute(sql, data)
    else:
        cursor.execute("SELECT * FROM rmms")

    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    return insertObject

 #Alertas rmms
 
#Agregar rmms:
@app.route('/msgrmmsadd',methods=['GET'])
def msgrmmsadd():
    data = datos_rmms()
    return render_template('rmms.html', data=data, msg = "Reservacion Ingresada con Exito!", tipo=1)

#Editar rmms:
@app.route('/msgrmmsedit',methods=['GET'])
def msgrmmsedit():
    data = datos_rmms()
    return render_template('rmms.html', data=data,msg = "Reservacion Editada con Exito!", tipo=1)

#Eliminar rmms:
@app.route('/msgrmmsdelete',methods=['GET'])
def msgrmmsdelete():
    data = datos_rmms()
    msg = "Reservacion Eliminada con Exito!"
    return render_template('rmms.html', data=data,msg = "Reservacion Eliminada con Exito!", tipo=1)

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
    
    #Variable booleana en caso de que todas las condiciones sean falsas:
    if_true = False
    
    if not all([nombres, apellidos, DUI, telefono, t_reservacion, fecha, total, pago , p_pendiente]):
        if_true = True
        mensaje_error = "Error: Campo en blanco, llena todos los campos"
        search_term = request.args.get('search', '')
        data = datos_rlocal(search_term)
        return render_template('r_local.html', mensaje_error=mensaje_error, 
                                nombres=nombres,
                                apellidos=apellidos,
                                DUI=DUI,
                                telefono=telefono,
                                t_reservacion=t_reservacion,
                                fecha=fecha,
                                total=total,
                                pago=pago,
                                p_pendiente=p_pendiente,
                                data=data, search_term=search_term)  
    
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
        if_true = True
        mensaje_error = "Error al Guardar, fecha no disponible!"
        search_term = request.args.get('search', '')
        data = datos_rlocal(search_term)
        return render_template('r_local.html', mensaje_error=mensaje_error, 
                                nombres=nombres,
                                apellidos=apellidos,
                                DUI=DUI,
                                telefono=telefono,
                                t_reservacion=t_reservacion,
                                fecha=fecha,
                                total=total,
                                pago=pago,
                                p_pendiente=p_pendiente,
                                data=data, search_term=search_term) 
    
    else:        
        if result:
            if_true = True
            NID, cantidad = result
            Ncantidad = cantidad + 1
            update_query = "UPDATE clientes SET c_reservaciones = %s WHERE nombres = %s"
            cursor.execute(update_query, (Ncantidad, NID,))
            db.database.commit()
            
        elif nombres and apellidos and DUI and telefono and t_reservacion and fecha and total and pago and p_pendiente:
            if_true = True 
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
    
    if  if_true == True:    
        return redirect(url_for('msglocaladd'))
    else:
        mensaje_error = "Error al Guardar, Intentelo de nuevo!"
        search_term = request.args.get('search', '')
        data = datos_rlocal(search_term)
        return render_template('r_local.html', mensaje_error=mensaje_error, 
                                nombres=nombres,
                                apellidos=apellidos,
                                DUI=DUI,
                                telefono=telefono,
                                t_reservacion=t_reservacion,
                                fecha=fecha,
                                total=total,
                                pago=pago,
                                p_pendiente=p_pendiente,
                                data=data, search_term=search_term)  
    

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
    else:
        mensaje_error = "Error al Eliminar, Intentelo de nuevo"
        search_term = request.args.get('search', '')
        data = datos_rlocal(search_term)
        return render_template('r_local.html', mensaje_error=mensaje_error,
                               data=data, search_term=search_term)
        

@app.route('/editlocal/<string:id>', methods=['POST'])
def editlocal(id):
    nombres = request.form['nombres'].strip()
    apellidos = request.form['apellidos'].strip()
    DUI = request.form['DUI'].strip()
    telefono = request.form['telefono'].strip()
    t_reservacion = request.form['t_reservacion'].strip()
    fecha = request.form['fecha'].strip()
    total = request.form['total'].strip()
    pago = request.form['pago'].strip()
    
    cursor = db.database.cursor()
    consulta = "SELECT * FROM r_local WHERE fecha = %s"
    valores = (fecha,)
    cursor.execute(consulta, valores,)
    resultado = cursor.fetchone()
    
    if resultado:
       
        mensaje_error = "Error al Guardar, fecha no disponible!"
        search_term = request.args.get('search', '')
        data = datos_rlocal(search_term)
        return render_template('r_local.html', mensaje_error=mensaje_error, 
                                nombres=nombres,
                                apellidos=apellidos,
                                DUI=DUI,
                                telefono=telefono,
                                t_reservacion=t_reservacion,
                                fecha=fecha,
                                total=total,
                                pago=pago,
                                data=data, search_term=search_term)
	
    
    if not all([nombres, apellidos, DUI, telefono, t_reservacion, fecha, total, pago]):
        mensaje_error = "Error: Campo en blanco, llena todos los campos"
        search_term = request.args.get('search', '')
        data = datos_rlocal(search_term)
        return render_template('r_local.html', mensaje_error=mensaje_error, 
                                data=data, search_term=search_term)
    

    if nombres and apellidos and DUI and telefono and t_reservacion and fecha and total and pago :
        cursor = db.database.cursor()
        sql = "UPDATE r_local SET nombres=%s, apellidos=%s, DUI=%s, telefono=%s, t_reservacion=%s, fecha=%s, total=%s, pago=%s WHERE id=%s"
        data = (nombres, apellidos, DUI, telefono, t_reservacion, fecha, total, pago, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msglocaledit'))
    else:
        mensaje_error = "Error al Editar, Intentelo de nuevo"
        search_term = request.args.get('search', '')
        data = datos_rlocal(search_term)
        return render_template('r_local.html', mensaje_error=mensaje_error,
                               data=data, search_term=search_term)
    
    
def datos_rlocal(search_term=''):
    cursor = db.database.cursor()

    if search_term:
        sql = "SELECT * FROM r_local WHERE nombres LIKE %s "
        data = ('%' + search_term + '%', '%' + search_term + '%')
        cursor.execute(sql, data)
    else:
        cursor.execute("SELECT * FROM r_local")

    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    return insertObject    
    
#Alertas    

#Agregar r_local:
@app.route('/msglocaladd',methods=['GET'])
def msglocaladd():
    data = datos_rlocal()
    return render_template('r_local.html', data=data, msg = "Reservacion Ingresada con Exito!", tipo=1)

#Editar r_local:
@app.route('/msglocaledit',methods=['GET'])
def msglocaledit():
    data = datos_rlocal()
    return render_template('r_local.html', data=data, msg = "Reservacion Editada con Exito!", tipo=1)

#Eliminar r_local:
@app.route('/msglocaldelete',methods=['GET'])
def msglocaldelete():
    data = datos_rlocal()
    return render_template('r_local.html', data=data, msg = "Reservacion Eliminada con Exito!", tipo=1)

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
        
        return render_template('index.html')
    elif(correo == ''or password == ''):
        return render_template('login.html',mensaje="Campos vacios, ingrese sus credenciales")
    else:
        return render_template('login.html',mensaje="Usuario o Contraseña Incorrecta, Intentelo de nuevo")
     
     
      


#--------------------------------------------------------------------------------

#Administradores

@app.route('/admin_datos')
def admin_datos():
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
    
    cursor = db.database.cursor()
    
    consulta = "SELECT * FROM administrador WHERE correo = %s"
    valores = (correo,)
    cursor.execute(consulta, valores,)
    resultado = cursor.fetchone()

    if not all([correo, password]):
        mensaje_error = "Error: Campo en blanco, llena todos los campos"
        search_term = request.args.get('search', '')
        data = admin(search_term)
        return render_template('admin.html', mensaje_error=mensaje_error, correo=correo, password=password, data=data, search_term=search_term)
    
    if resultado:
        mensaje_error = "Error: El Usuario ingresado ya existe"
        search_term = request.args.get('search', '')
        data = admin(search_term)
        return render_template('admin.html', mensaje_error=mensaje_error, correo=correo, password=password, data=data, search_term=search_term)
        
    if resultado:
        mensaje_error = "Error: El Usuario ingresado ya existe"
        search_term = request.args.get('search', '')
        data = admin(search_term)
        return render_template('admin.html', mensaje_error=mensaje_error, correo=correo, password=password, data=data, search_term=search_term)
    
    if correo and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO administrador (correo, password) VALUES (%s, %s)"
        data = (correo, password)
        cursor.execute(sql, data)
        db.database.commit()
      
        return redirect(url_for('msgadminadd'))

    else:
        mensaje_error = "Error al Guardar, Intentelo de nuevo"
        search_term = request.args.get('search', '')
        data = admin(search_term)
        return render_template('admin.html', mensaje_error=mensaje_error, 
                               correo=correo,
                               password=password,
                               data=data, search_term=search_term)
 
@app.route('/deleteadmin/<string:id>')
def deleteadmin(id):
    if id:
        cursor=db.database.cursor()
        sql= "DELETE FROM administrador WHERE id=%s"
        data = (id,)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msgadmindelete'))
    else:
        mensaje_error = "Error al Eliminar, Intentelo de nuevo"
        search_term = request.args.get('search', '')
        data = admin(search_term)
        return render_template('admin.html', mensaje_error=mensaje_error,
                               data=data, search_term=search_term)


    
@app.route('/editadmin/<string:id>', methods=['POST'])
def editadmin(id):

    correo = request.form['correo'].strip()
    password = request.form['password'].strip()
    
    cursor = db.database.cursor()
    
    consulta = "SELECT * FROM administrador WHERE correo = %s"
    valores = (correo,)
    cursor.execute(consulta, valores,)
    resultado = cursor.fetchone()
    
    if not all([correo, password]):
        mensaje_error = "Error: Campo en blanco, llena todos los campos"
        search_term = request.args.get('search', '')
        data = admin(search_term)
        return render_template('admin.html', mensaje_error=mensaje_error, data=data, search_term=search_term)
    
    if correo == correo:
        cursor = db.database.cursor()
        sql = "UPDATE administrador SET  correo=%s, password=%s WHERE id=%s"
        data = (correo, password, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msgadminedit'))
    
    if resultado: 
        mensaje_error = "Error: El Usuario ingresado ya existe"
        search_term = request.args.get('search', '')
        data = admin(search_term)
        return render_template('admin.html', mensaje_error=mensaje_error, data=data, search_term=search_term)
    
    if correo and password:
        cursor = db.database.cursor()
        sql = "UPDATE administrador SET  correo=%s, password=%s WHERE id=%s"
        data = (correo, password, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msgadminedit'))
       
    else:
        mensaje_error = "Error al Editar, Intentelo de nuevo"
        search_term = request.args.get('search', '')
        data = admin(search_term)
        return render_template('admin.html', mensaje_error=mensaje_error,
                               data=data, search_term=search_term)
        

def admin(search_term=''):
    cursor = db.database.cursor()

    if search_term:
        sql = "SELECT * FROM administrador WHERE correo LIKE %s "
        data = ('%' + search_term + '%', '%' + search_term + '%')
        cursor.execute(sql, data)
    else:
        cursor.execute("SELECT * FROM administrador")

    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    return insertObject

#Alertas Administradores...                                          $$$$
 
#Agregar Administrador:
@app.route('/msgadminadd',methods=['GET'])
def msgadminadd():
    data = admin()
    return render_template('admin.html', data=data, msg="Administrador Ingresado con Exito!", tipo=1)

#Editar Administrador:
@app.route('/msgadminedit',methods=['GET'])
def msgadminedit():
    data = admin()
    return render_template('admin.html', data=data, msg="Administrador Editado con Exito!", tipo=1)

#Eliminar Administrador:
@app.route('/msgadmindelete',methods=['GET'])
def msgadmindelete():
    data = admin()
    return render_template('admin.html', data=data, msg="Administrador Eliminado con Exito!", tipo=1)
 
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
    
    #Variable booleana en caso de que todas las condiciones sean falsas:
    if_true = False
    
    # Verifica si alguna de las variables después de aplicar strip() está vacía
    if not all([nombres, apellidos,DUI, telefono, p_pendiente, c_reservaciones]):
        if_true = True
        mensaje_error = "Error: Campo en blanco, llena todos los campos"
        search_term = request.args.get('search', '')
        data = datos_clientes(search_term)
        return render_template('clientes.html', mensaje_error=mensaje_error, 
                                nombres=nombres,
                                apellidos=apellidos,
                                DUI=DUI,
                                telefono=telefono,
                                p_pendiente=p_pendiente,
                                c_reservaciones=c_reservaciones,
                                data=data, search_term=search_term) 
    
    if nombres and apellidos and DUI and telefono and p_pendiente and c_reservaciones :
        if_true = True
        cursor = db.database.cursor()
        sql = "INSERT INTO clientes (nombres, apellidos, DUI, telefono, p_pendiente, c_reservaciones) VALUES (%s, %s, %s, %s, %s, %s)"

        data = (nombres, apellidos, DUI, telefono, p_pendiente, c_reservaciones)
        cursor.execute(sql, data)
        db.database.commit()
    
    if  if_true == True:   
        return redirect(url_for('valclient'))
    else:
        mensaje_error = "Error al Guardar, Intentelo denuevo"
        search_term = request.args.get('search', '')
        data = datos_clientes(search_term)
        return render_template('clientes.html', mensaje_error=mensaje_error, 
                                nombres=nombres,
                                apellidos=apellidos,
                                DUI=DUI,
                                telefono=telefono,
                                p_pendiente=p_pendiente,
                                c_reservaciones=c_reservaciones,
                                data=data, search_term=search_term) 
        
    
@app.route('/deleteclient/<string:id>')
def deleteclient(id):
    if id:
        cursor = db.database.cursor()
        sql = "DELETE FROM clientes WHERE id=%s"
        data = (id,)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msgclientdelete'))
    else:
        mensaje_error = "Error al Eliminar, Intentelo denuevo"
        search_term = request.args.get('search', '')
        data = datos_clientes(search_term)
        return render_template('clientes.html', mensaje_error=mensaje_error, 
                                data=data, search_term=search_term) 

@app.route('/editclient/<string:id>', methods=['POST'])
def editclient(id):
    
    nombres = request.form['nombres'].strip()
    apellidos = request.form['apellidos'].strip()
    DUI = request.form['DUI'].strip()
    telefono = request.form['telefono'].strip()
    p_pendiente = request.form['p_pendiente'].strip()
    c_reservaciones = request.form['c_reservaciones'].strip()
    
    if not all([nombres, apellidos,DUI, telefono, p_pendiente, c_reservaciones]):
        if_true = True
        mensaje_error = "Error: Campo en blanco, llena todos los campos"
        search_term = request.args.get('search', '')
        data = datos_clientes(search_term)
        return render_template('clientes.html', mensaje_error=mensaje_error, 
                                data=data, search_term=search_term) 
    

    if nombres and apellidos and DUI and telefono and p_pendiente and  c_reservaciones:
        cursor = db.database.cursor()
        sql = "UPDATE clientes SET nombres=%s, apellidos=%s, DUI=%s, telefono=%s, p_pendiente=%s, c_reservaciones=%s WHERE id=%s"

        data = (nombres, apellidos, DUI, telefono, p_pendiente, c_reservaciones, id)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('msgclientedit'))
    else:
        mensaje_error = "Error al Editar, Intentelo denuevo"
        search_term = request.args.get('search', '')
        data = datos_clientes(search_term)
        return render_template('clientes.html', mensaje_error=mensaje_error, 
                                data=data, search_term=search_term) 
    
def datos_clientes(search_term=''):
    cursor = db.database.cursor()

    if search_term:
        sql = "SELECT * FROM clientes WHERE nombres LIKE %s "
        data = ('%' + search_term + '%', '%' + search_term + '%')
        cursor.execute(sql, data)
    else:
        cursor.execute("SELECT * FROM clientes")

    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    return insertObject

#Alertas Clientes

#Mensaje agregar cliente:
@app.route('/valclient',methods=['GET'])
def valclient():
    data = datos_clientes()
    return render_template('clientes.html', data=data, msg = "Cliente Ingresado con Exito!", tipo=1)

#Editar cliente:
@app.route('/msgclientedit',methods=['GET'])
def msgclientedit():
    data = datos_clientes()
    return render_template('clientes.html', data=data, msg = "Cliente Editado con Exito!", tipo=1)

#Eliminar cliente:
@app.route('/msgclientdelete',methods=['GET'])
def msgclientdelete():
    data = datos_clientes()
    return render_template('clientes.html', data=data, msg = "Cliente Eliminado con Exito!", tipo=1)

#----------------------------------------------------------------------------------


if __name__ == '__main__':
    app.secret_key = "12345"
    app.run(debug=True, port=7000)
    
#----------------------------------------------------------------------------------