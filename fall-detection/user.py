from flask import *  
import sqlite3
import io
import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
source="one.1993.player@gmail.com"
destination="sraja5@hawk.iit.edu"
app = Flask(__name__)  
 
#@app.route("/location")  
#def location(): 
 #   url = "https://us1.unwiredlabs.com/v2/process.php"
  #  payload = "{\"token\": \"15cae6580f73a9\",\"radio\": \"gsm\",\"mcc\": 310,\"mnc\": 410,\"cells\": [{\"lac\": 7033,\"cid\": 17811}],\"wifi\": [{\"bssid\": \"00:17:c5:cd:ca:aa\",\"channel\": 11,\"frequency\": 2412,\"signal\": -51}, {\"bssid\": \"d8:97:ba:c2:f0:5a\"}],\"address\": 1}"
   # response = requests.request("POST", url, data=payload)

    #print(response.text)
   
def moniter():
    msg = MIMEMultipart()
    msg['From'] = source
    msg['To'] = destination
    msg['Subject'] = "Patient Alert"
    body = 'Patient has fallen. Please login to the portal and access your patients login or click https://locationmagic.org/locate'
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo
    server.starttls()
    server.login(source, "ece442project")
    text = msg.as_string()
    server.sendmail(source, destination, text)
    server.quit()
 
@app.route("/")  
def index():
    if not session.get('logged_in'):
        return render_template("index.html");
    else:
        return 'Hello Boss!  <a href="/logout">Logout</a>';
    
@app.route('/patientlogin')
def patientlogin():
       # if request.method == "POST":  
        #    try:
         #       msg = request.form['loginEmail']
          #  except:   
           #     msg = "We can not add the User to the list"  
           # finally:  
    return render_template("patientlogin.html")   
    #if  request.form['inputEmail'] == 'admin@123':
        #session['logged_in'] = True
    #else:
     #   flash('wrong password!')
      #  return render_template("home.html")
      
@app.route('/homePhysician')
def loginPhysician():
    return render_template("physicianhome.html")

@app.route('/physicianlogin')
def physicianlogin():
        #if request.method == "POST":  
         #   try:
          #      msg = request.form['loginEmail']
           # except:   
            #    msg = "We can not add the User to the list"  
            #finally:  
   return render_template("physicianlogin.html")

@app.route('/loginPatient')
def loginPatient():
   return render_template("patienthome.html")    

@app.route("/add")  
def add():  
    return render_template("add.html")  
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            category = request.form.get["Category"]
            name = request.form["name"]
            email = request.form["email"]  
            password = request.form["password"]
            Physicianid = request.form["inputPhysician"]
            with sqlite3.connect("FallDetection.db") as con:  
                cur = con.cursor()
                #if category == "Patient":
                cur.execute("INSERT into Patient (name, emailid, password, physicianid) values (?,?,?,?)",(name,email,password,Physicianid))  
                #else:
                #cur.execute("INSERT into Physician (name, emailid, password) values (?,?,?)",(category,email,password))  
                con.commit()  
                msg = "User successfully Added"  
        except:  
            con.rollback()  
            msg = "We can not add the User to the list"  
        finally:  
            return render_template("success.html",msg = msg)  
            con.close()  
 
@app.route("/view")  
def view():  
    con = sqlite3.connect("FallDetection.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Patient")  
    rows = cur.fetchall()
    moniter()
    return render_template("view.html",rows = rows)  
 
@app.route("/viewsensordata")  
def chart():  
    con = sqlite3.connect("FallDetection.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("select * from sensordata limit 100")
    rows = cur.fetchall()
    moniter()
    for row in cur.execute("select * from sensordata limit 1"):
        blood = row[3]
        heartrate = row[4]
        temp = row[7]
    labels = ["Blood","Heart Rate","Temperature"]
    values = [4, 2, 4]
    return render_template("viewsensordata.html",rows = rows, values=values, labels=labels)

@app.route("/delete")  
def delete():  
    return render_template("delete.html")  
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id = request.form["id"]  
    with sqlite3.connect("FallDetection.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Employees where id = ?",id)  
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_record.html",msg = msg)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
  
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug = True)  