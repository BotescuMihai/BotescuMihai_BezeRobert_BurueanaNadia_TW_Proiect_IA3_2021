from json import dump, load

class JSONImporter(object):
  def file_name(self,file_name):
    try:
      self.__file = open(file_name,'r')
    except FileNotFoundError as e:
      print(f'Error\nCause:{e.getCause()}')
    return self
  def __str__(self):
    return f'Opening {self.__filename} ...'
  def getData(self):
    try:
      self.__content = load(self.__file)
    except:
      print('Error occured')
    return self
  def getContent(self):
    return self.__content
  def nth(self,n):
    try:
      return self.__content[n]
    except IndexError as ie:
      print(f'Error\nCause:{e.getCause()}')

  


