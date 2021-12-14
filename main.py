from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import random
from flask import url_for
from data_manager import *
from json import *


app = Flask(  # Create a flask app
	__name__,
	template_folder='',  # Name of html file folder
	static_folder=''  # Name of directory for static files
)

@app.route('/contact')
def contact_page():
  return render_template('contact_us.html')

@app.route('/about')
def about_page():
  return render_template('about.html')

@app.route('/sentinel', methods=['GET', 'POST'])
def getSelectedDate():
    information = request.data.decode(encoding='utf-8')
 #  print(information)
    session['selectedDate'] = information
    return information


@app.route('/calendar')
def calendar():
  name = session.get('name')
  if name is None:
    return redirect(url_for('home_page'))
  role = session['role']
  name = extract_name(name)
  img_name = f'img/{name.split()[1]}.jpeg'
  if role != "doctor" and role != "nurse" and role != "receptionist" and role != "admin":
      return redirect(url_for(role))
  data = session.get('selectedDate')
  print(data)
  if data is not None:
    flash(data, 'primary')
    session['selectedDate'] = None
  return render_template('calendar.html',name=name,img_name = img_name, sname=session.get('name'))

#from JSON_Importer import *
#print(JSONImporter().file_name('data_files/doctors_calendars.json').getData().nth(0)["tasks"])


@app.route('/admin')
def admin():
  name = session.get('name')
  if name is None:
    return redirect(url_for('home_page'))
  role = session['role']
  if role != "admin":
    return redirect(url_for(role))
  name = extract_name(name)
  return render_template('admin.html',name=name)

@app.route('/personal_registration',methods = ['POST','GET'])
def personal_registration():
  name = session.get('name')
  if name is None:
    return redirect(url_for('home_page'))
  role = session['role']
  if role != 'admin':
    return redirect(url_for(role))

  if request.method == 'GET':
    return render_template('personal_registration.html')
    
  if request.method == 'POST':
    datas = dict()
    datas["first_name"] = str(request.form["name1"])
    datas["last_name"] = str(request.form["name2"])
    datas["email"] = str(request.form["email"])
    datas["date"] = str(request.form["date"])
    datas["time"] = str(request.form["time"])
    datas["cnp"] = str(request.form["cnp"])
    datas["type"] = str(request.form["type"])
    datas["department"] = str(request.form["department"])
    datas["school"] = str(request.form["school"])
    datas["year"] = str(request.form["year"])
    datas["speciality"] = str(request.form["speciality"])
    write_data_toJSON('data_files/staff.json',datas)
    return redirect(url_for('admin'))

@app.route('/login', methods=['POST','GET'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  if request.method == 'POST':
    username = request.form['email']
    password = request.form['password']
    datas = check_account_credentials(username,password,'data_files/accounts.json')
    if datas[0] == True:
      session['name'] = username
      session['role'] = datas[1]
      return redirect(url_for(session['role']))
    else:
      return redirect('login')

app.secret_key = 'fasfgdsgs'


@app.route('/')
def home_page():
  return render_template('index.html')

@app.route('/doctor')
def doctor():
  name = session.get('name')
  if name is None:
    return redirect(url_for('home_page'))
  role = session['role']
  if role != "doctor":
    return redirect(url_for(role))
  name = extract_name(name)
  img_name = f'img/{name.split()[1]}.jpeg'
  return render_template('doctor.html',name=name,img_name = img_name)# img_name = img_name
  #sau se poate si cu lista
  #daca faci cu lista dupa nu o sa mai mearga {{ name }} in fisierele html
  #ok
  #am modificat
  

@app.route('/pacient_appointment')
def pacient_appointment_page():
  return render_template('pacient_appointment.html')


@app.route('/receptioner')
def receptionist():
  name = session.get('name')
  if name is None:
    return redirect(url_for('home_page'))
  name = extract_name(name)
  role = session['role']
  if role != "receptionist":
    return redirect(url_for(role))
  return render_template('receptioner.html', name=name)

@app.route('/nurse')
def nurse():
  name = session.get('name')
  if name is None:
    return redirect(url_for('home_page'))
  name = extract_name(name)
  role = session['role']
  if role != "nurse":
    return redirect(url_for(role))
  return render_template('nurse.html', name=name)


@app.route('/appointment-receptionist')
def appointment_receptionist():
  name = session.get('name')
  if name is None:
    return redirect(url_for('home_page'))
  name = extract_name(name)
  role = session['role']
  if role != "receptionist":
    return redirect(url_for(role))
  return render_template('appointment.html', name=name)

@app.route('/register-patient')
def register_patient():
  name = session.get('name')
  if name is None:
    return redirect(url_for('home_page'))
  name = extract_name(name)
  role = session['role']
  if role != "receptionist":
      return redirect(url_for(role))
  return render_template('registration.html', name=name)



if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=8080,  # Randomly select the port the machine hosts on.
    debug = True,
	)