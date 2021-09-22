import shutil,os

s = "C:\Users\jimenez\Desktop\PythonScripts"
foo = os.path.join(s,"foo")
des = os.path.join(s,"boo")
shutil.copytree(foo,des,symlinks=True)