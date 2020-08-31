from time import asctime
def write(error):
  with open("logs.txt","a+") as fp:
    fp.write(error+"\t"+asctime()+"\n")