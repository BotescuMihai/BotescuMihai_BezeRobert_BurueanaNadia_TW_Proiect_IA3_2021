
from json import *
from re import compile, findall 
import os




def our_hash(text:str):
  hash=0
  for ch in text:
    hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
  return hash


def check_account_credentials(email,password,file_name):
  valid = False
  function = None 
  try:
    with open(file_name,'r') as f:
      datas = load(f)
      for data in datas:
        if data['email'] == email and data['password'] == our_hash(password):
          valid = True
          function = data['role']
          break
  except Exception as e:
    print(e)
    print('Error occured.')
  finally:
    f.close()
    return [valid,function]

#eric.foreman@princeton.plainsboro.us

def extract_name(email):
  pattern = compile('\w+.\w+@')
  res = findall(pattern,email)
  finalname = " ".join(res[0][:len(res[0])-1:].split("."))
  finalnameres = ""
  finalnameres += finalname[0].upper()
  i = 0
  while i < len(finalname):
    if finalname[i] == ' ':
      break
    finalnameres += finalname[i]
    i += 1
  finalnameres = finalname[:i:] + finalname[i].upper() + finalname[i+1::]
  return finalnameres


def write_data_toJSON(filename,data):
  size = os.path.getsize(filename)
  if size == 0:
    datas = list()
    datas.append(data)
    with open(filename, "w+") as f:
      dump(datas, f)
  else:
    with open(filename, "r") as f:
      datas = load(f)
    datas.append(data)
    with open(filename, "w") as f:
      dump(datas, f)

def get_doctors():
  with open('data_files/accounts.json','r') as f:
    datas = load(f)
    return ''.join([extract_name(data['email']) + '<br>' for data in datas if data['role'] == 'doctor'])

def get_nurses():
  with open('data_files/accounts.json','r') as f:
    datas = load(f)
    return ''.join([extract_name(data['email']) + '<br>' for data in datas if data['role'] == 'nurse'])


def get_receptionists():
  with open('data_files/accounts.json','r') as f:
    datas = load(f)
    return ''.join([extract_name(data['email'])  + '<br>' for data in datas if data['role'] == 'receptionist'])

def get_doctors_pacients(name):
  with open('data_files/patients_appointments_unencrypted.json','r') as f:
    datas = load(f)
    s = '<ul>'
    s += ''.join(['<li>' + data['name'] + ' ' + data['date'] + ' ' + data['time'] + ' Message: ' + data['message'] + '</li>' for data in datas if data['doctor'] == name])
    s += '</ul>'
    return s


def get_patients():
  with open('data_files/pacients.json','r') as f:
    datas = load(f)
    s = '<ul>'
    s += ''.join(['<li>' + data['name'] + '; DOB:' + data['date'] + '; Insurance ID:' + data['insuranceid']  + '</li>' for data in datas])
    s += '</ul>'
    return s
  
