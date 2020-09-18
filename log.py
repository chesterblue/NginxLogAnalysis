from time import asctime
import os

dir = os.path.dirname(os.path.abspath(__file__))
filepath = dir+"/logs.txt"
def write(error):
  with open(filepath,"a+") as fp:
    fp.write(error+"\t"+asctime()+"\n")