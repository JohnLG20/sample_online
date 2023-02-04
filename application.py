import re
import MySQLdb.cursors
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
import datetime
import urllib3

app = Flask(__name__)

app.secret_key = 'kasjdbsdf'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'brgydb'
 
mysql = MySQL(app)
 
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staff WHERE username = % s AND userpass = % s', (username, password, ))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM admin WHERE adname = % s AND adpassword = % s', (username, password, ))
        admin = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            f = datetime.datetime.now()
            d = f.strftime(" %A %m,%Y Time: %I:%M%p")
            g = 'Logging in'
            cursor.execute('INSERT INTO stafflogs VALUES (NULL,%s,%s,%s)', (username, d,g))
            mysql.connection.commit()
            return render_template('client.html', msg = msg,) 
        if admin:
            session['loggedin'] = True
            session['id'] = admin['id']
            session['username'] = admin['adname']
            return render_template('admin.html', msg = msg,) 
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))




@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staff WHERE username = % s AND userpass = % s', (username, password))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        else:      
            cursor.execute('INSERT INTO staff VALUES (NULL,%s,%s,%s)', (username, password,email,))
            mysql.connection.commit()
            msg = 'Success'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('reg_acc.html', msg = msg)







@app.route('/deleterecord', methods =['GET', 'POST'])
def deleterecord():
    msg = ''
    if request.method == 'POST' and 'username' in request.form:
        username = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staff WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            cursor.execute('DELETE FROM staff WHERE username = %s', (username,))
            mysql.connection.commit()
            msg = 'successfully'
        else:
            msg = 'ACCOUNT NOT EXIST !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('delete_resident.html', msg = msg)






@app.route("/view_info")
def view():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    resultValue = cur.execute('SELECT * FROM staff')
    if resultValue:
        userDetails = cur.fetchall()
        return render_template('acc_info.html',userDetails=userDetails)
    

@app.route("/view_logs")
def view_logs():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    res = cur.execute('SELECT * FROM stafflogs')
    if res:
        logs = cur.fetchall()
        return render_template('logs.html',logs=logs)





@app.route("/Home")
def home():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    resultValue = cur.execute('SELECT * FROM user')
    if resultValue:
        userDetails = cur.fetchall()
        return render_template('admin.html',userDetails=userDetails)








@app.route("/Home2")
def Home2():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM resident')
    name1 = len(cursor.fetchall())
    cursor.execute("SELECT * FROM resident WHERE pwdorsenior = 'senior'")
    name2 = len(cursor.fetchall())
    cursor.execute("SELECT * FROM resident WHERE pwdorsenior = 'pwd'")
    name3 = len(cursor.fetchall())
    cursor.execute("SELECT * FROM resident WHERE gender = 'female'")
    name4 = len(cursor.fetchall())
    cursor.execute("SELECT * FROM resident WHERE gender = 'male'")
    name5 = len(cursor.fetchall())
    cursor.execute("SELECT * FROM appointments")
    name6 = len(cursor.fetchall())
    return render_template('client.html',name1=name1, name2=name2, name3=name3, name4=name4, name5=name5,name6=name6)






@app.route('/saverecord', methods =['GET', 'POST'])
def saverecord():
    msg = ''
    if request.method == 'POST' and 'fname' in request.form and 'gender' in request.form and 'age' in request.form and 'bdate' in request.form and 'bplace' in request.form and 'civilstatus' in request.form and 'religion' in request.form and 'nationality' in request.form and 'contact' in request.form and 'city' in request.form and 'brgy' in request.form and 'purok' in request.form and 'lengthofstay' in request.form and 'pwdorsenior' in request.form and 'occupation' in request.form:
        f = request.form['fname']
        g = request.form['gender']
        a = request.form['age']
        bd = request.form['bdate']
        bp = request.form['bplace']
        civ = request.form['civilstatus']
        reg = request.form['religion']
        nat = request.form['nationality']
        con = request.form['contact']
        cit = request.form['city']
        b = request.form['brgy']
        p = request.form['purok']
        le = request.form['lengthofstay']
        sen = request.form['pwdorsenior']
        fn = request.form['occupation']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM resident')
        k = cursor.fetchall()
        if k == f:
            msg = 'Resident already exists !'
        else:
            cursor.execute('INSERT INTO resident VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (f,g,a,bd,bp,civ,reg,nat,con,cit,b,p,le,sen,fn,))
            mysql.connection.commit()
            msg = "Success"
    return render_template('add_resident.html', msg = msg)







@app.route('/updaterecord', methods=['GET','POST'])
def updaterecord():
    msg = ''
    if request.method == 'POST' and 'id' in request.form:
        f = request.form['fname']
        g = request.form['gender']
        a = request.form['age']
        bd = request.form['bdate']
        bp = request.form['bplace']
        civ = request.form['civilstatus']
        reg = request.form['religion']
        nat = request.form['nationality']
        con = request.form['contact']
        cit = request.form['city']
        b = request.form['brgy']
        p = request.form['purok']
        le = request.form['lengthofstay']
        sen = request.form['pwdorsenior']
        fn = request.form['occupation']
        fa = request.form['elementaryschool']
        fbd = request.form['highschool']
        fbp = request.form['collage']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM resident WHERE id =%s", (f,))
        account = cur.fetchone()
        if account:
            cur.execute('UPDATE resident SET fname=%s,gender=%s,age=%s,dob=%s,bp=%s,civilstatus=%s,religion=%s,nationality=%s,contact=%s,city=%s,brgy=%s,purok=%s,lengthofstay=%s,pwdorsenior=%s,occupation=%s,elementaryschool=%s,highschool=%s,collage=%s WHERE id =%s', (f,g,a,bd,bp,civ,reg,nat,con,cit,b,p,le,sen,fn,fa,fbd,fbp,mo,ma,mbd,mbp,tth,hf,))
            mysql.connection.commit()
            msg = 'SUCCESSFULLY UPDATE'
            return render_template('resident_info.html',msg=msg)        
    return render_template('updaterecord.html',msg=msg)



@app.route("/residentinfo", methods=['GET','POST'])
def residentinfo():
    if request.method == 'POST' and 'rname' in request.form:
        gname = request.form['rname']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM resident")
        p = cur.fetchall()
        if p:
            cur.execute("SELECT * FROM resident WHERE fname =%s",(gname,))
            f = cur.fetchall()
            return render_template('updaterecord.html',f=f,)







@app.route('/health_info', methods =['GET', 'POST'])
def health_info():
    msg = ''
    if request.method == 'POST' and 'fname' in request.form and 'gender' in request.form and 'age' in request.form and 'contact' in request.form and 'dob' in request.form and 'city' in request.form and 'brgy' in request.form and 'purok' in request.form and 'ps' in request.form :
        fname = request.form['fname']
        gender = request.form['gender']
        age = request.form['age']
        con = request.form['contact']
        dob = request.form['dob']
        ci = request.form['city']
        br = request.form['brgy']
        pu = request.form['purok']
        ps = request.form['ps']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM resident')
        k = cursor.fetchone()
        if k:
            msg = 'Resident already exists !'
        else:      
            cursor.execute('INSERT INTO resident VALUES (NUll,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (fname,gender,age,con,dob,ci,br,pu,ps))
            mysql.connection.commit()
            msg = "Success"
    return render_template('health_service_info.html', msg = msg)





@app.route("/resident_info",methods=['GET','POST'])
def resident_info():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM resident')
    name = cur.fetchall()
    cur.execute("SELECT * FROM resident WHERE pwdorsenior = 'senior'")
    name2 = cur.fetchall()
    cur.execute("SELECT * FROM resident WHERE pwdorsenior = 'pwd'")
    name3= cur.fetchall()
    cur.execute("SELECT * FROM resident")
    view4= cur.fetchall()
    cur.execute("SELECT * FROM resident WHERE gender = 'male'")
    name5 = cur.fetchall()
    cur.execute("SELECT * FROM resident WHERE gender = 'female'")
    name6 = cur.fetchall()
    cur.execute("SELECT * FROM resident")
    name7 = cur.fetchall()
    return render_template('resident_info.html',name=name, name2=name2, name3=name3, view4=view4, name5=name5, name6=name6, name7=name7)




    
    
        
    
        


            
        







    

@app.route("/view_appointments")
def view_appointments():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM appointments")
    view1 = cur.fetchall()
    return render_template('appointments.html',view1=view1)








@app.route("/resident_appointments", methods=['GET','POST'])
def resident_appointments():
    if request.method == 'POST' and 'fname' in request.form and 'contact' in request.form and 'dateandtime' in request.form and 'address' in request.form and 'purpose' in request.form:
        f = request.form['fname']
        co = request.form['contact']
        d = request.form['dateandtime']
        a = request.form['address']
        pur = request.form['purpose']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM appointments')
        cursor.fetchall()
        cursor.execute('INSERT INTO appointments VALUES (NUll,%s,%s,%s,%s,%s)', (f,co,d,a,pur,))
        mysql.connection.commit()
    return render_template('index.html')





@app.route("/appointment", methods = ['GET','POST'])
def appointment():
    msg = ''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM appointments")
    view1 = cur.fetchall()
    if request.method == 'POST' and 'contact' in request.form:
        http = urllib3.PoolManager()
        message = 'Confirm Appointments'
        contact = request.form['contact']
        http.request('POST',
        'https://api.semaphore.co/api/v4/messages',
        fields={
        'apikey': '8c0bc3925af627aaea9cd0e809757e32',
        'sendername': 'SEMAPHORE',
        'number': contact,
        'message': message,
        })
        msg = 'success......'
    return render_template('appointments.html',view1=view1,msg=msg)





@app.route('/delete_resident', methods =['GET', 'POST'])
def delete_resident():
    msg = ''
    if request.method == 'POST' and 'fname' in request.form:
        fname = request.form['fname']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM resident')
        account = cursor.fetchall()
        if account:
            cursor.execute('DELETE FROM resident WHERE fname = %s', (fname,))
            mysql.connection.commit()
            msg = 'successfully'
    return render_template('delete.html',msg=msg)




if __name__ == "__main__":
    app.run(debug = True)  
