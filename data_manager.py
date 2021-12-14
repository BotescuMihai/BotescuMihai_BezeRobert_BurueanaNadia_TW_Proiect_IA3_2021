
from json import *
from re import compile, findall 
import os

def check_account_credentials(email,password,file_name):
  valid = False
  function = None 
  try:
    with open(file_name,'r') as f:
      datas = load(f)
      for data in datas:
        if data['email'] == email and data['password'] == password:
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
    with open(filename, "w") as f:
      dump(datas, f)
  else:
    with open(filename, "r") as f:
      datas = load(f)
    datas.append(data)
    with open(filename, "w") as f:
      dump(datas, f)
