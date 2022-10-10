import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from numpy.lib.type_check import imag
from pymongo import *
import pymongo
from threading import *
import json,codecs
import time
from bson import json_util
import shutil

sys.path.append("/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream")
from ALPR_APP.deepstream_lpr_app import *
try:
    # Creating a client
    client = MongoClient('mongodbUrl')
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)
# Greating a database name GFG
db = client['TrafficDatabase']

# Created or Switched to collection 
records =db.records

data={"_id": {"$oid": ""}, "color": "", "licencePlateNumber": "", "make": "", "model": "", "name": ""}

with codecs.open('/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/ALPR_APP/MyFile.json', 'w', 'utf8') as f:
    f.write(json_util.dumps(data, sort_keys = True, ensure_ascii=False))
repl="/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/ALPR_APP/imagesdb/imagedb.jpg"
new_image="/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/background.jpg"
shutil.copyfile(new_image,repl)

class WorkerThread(QtCore.QObject):
    dis = QtCore.pyqtSignal()
 
    def __init__(self):
        super().__init__()
 
    @QtCore.pyqtSlot()
    def run(self):
        while True:
            # Long running task ...
            self.dis.emit()
            time.sleep(5)
 
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/welcome.ui",self)
        self.login.clicked.connect(self.gotologin)
        
    
    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/login.ui",self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.back1.clicked.connect(self.gotoWelcome)
        self.back1.setIcon(QtGui.QIcon('/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/index1.png'))
        self.back1.setIconSize(QtCore.QSize(40,40))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login1.clicked.connect(self.loginfunction)
    
   
        
  
    def loginfunction(self):
        user = self.username.text()
        password = self.password.text()

        if len(user)==0 or len(password)==0:
            self.error.setText("Please fill all fields.")

        elif user=="nerd" and password=="123456":
            Main = MainMenu()
            widget.addWidget(Main)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.error.setText("Incorrect Username or Password")            



    def gotoWelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
     
class MainMenu(QDialog):
    def __init__(self):
        super(MainMenu, self).__init__()
        loadUi("/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/MainMenu.ui",self)
        self.insert.clicked.connect(self.gotoInsert)
        self.search.clicked.connect(self.gotoSearch)
        self.ALPR.clicked.connect(self.gotoALPR)
        self.back2.clicked.connect(self.gotologin)
        self.back2.setIcon(QtGui.QIcon('/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/index1.png'))
        self.back2.setIconSize(QtCore.QSize(40,40))

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
  

    def gotoInsert(self):
        insert = Insert()
        widget.addWidget(insert)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoSearch(self):
        search = Search()
        widget.addWidget(search)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoALPR(self):
        alpr = ALPR()
        widget.addWidget(alpr)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class Insert(QDialog):
    def __init__(self):
        super(Insert, self).__init__()
        loadUi("/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/Insert.ui",self)
        self.back3.clicked.connect(self.gotoMainMenu)
        self.back3.setIcon(QtGui.QIcon('/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/index1.png'))
        self.back3.setIconSize(QtCore.QSize(40,40))
        self.add.clicked.connect(self.inputdata)

    def inputdata(self):
        
        new_data = {
        'name': self.name.text(),
        'make': self.make.text(),
        'model': self.model.text(),
        'color': self.color.text(),
        'licencePlateNumber':self.pl.text()
                    }
        if len(self.name.text())==0 or len(self.make.text())==0 or len(self.model.text())==0 or len(self.color.text())==0 or len(self.pl.text())==0:
            self.error1.setText("Please fill all fields.")
        else:
            self.error1.setText("Loading....")
            records.insert_one(new_data)
            self.error1.setText("Data inserted to the Database.")


    def gotoMainMenu(self):
        Main = MainMenu()
        widget.addWidget(Main)
        widget.setCurrentIndex(widget.currentIndex()+1)
  
class Search(QDialog):
    def __init__(self):
        super(Search, self).__init__()
        loadUi("/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/Search.ui",self)
        self.back4.clicked.connect(self.gotoMainMenu)
        self.back4.setIcon(QtGui.QIcon('/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/index1.png'))
        self.back4.setIconSize(QtCore.QSize(40,40))
        self.search.clicked.connect(self.gofind)
        self.search.setIcon(QtGui.QIcon('/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/search.png'))
        self.search.setIconSize(QtCore.QSize(40,40))
    
    def gofind(self):
        for doc in records.find({"licencePlateNumber":self.pl2.text()}):
            name=doc["name"]
            self.namedb.setText(name)
            make=doc["make"]
            self.makedb.setText(make)
            model=doc["model"]
            self.modeldb.setText(model)
            color=doc["color"]
            self.colordb.setText(color) 
            pldb=doc["licencePlateNumber"]
            self.pldb.setText(pldb)          
        num=db.records.find({"licencePlateNumber":self.pl2.text()}).count()
        if num==0:
            self.namedb.setText('')
            self.makedb.setText('')
            self.modeldb.setText('')
            self.colordb.setText('')
            self.pldb.setText('')
            self.error.setText("NO Results Found.")    
       


    def gotoMainMenu(self):
        Main = MainMenu()
        widget.addWidget(Main)
        widget.setCurrentIndex(widget.currentIndex()+1)

class ALPR(QDialog):
    global doc1
    def __init__(self):
        super(ALPR, self).__init__()
        loadUi("/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/ALPR.ui",self)  
        self.worker = WorkerThread()
        self.workerThread = QtCore.QThread()
        self.workerThread.started.connect(self.worker.run)  # Init worker run() at startup (optional)
        self.worker.dis.connect(self.display)  # Connect your signals/slots
        self.worker.moveToThread(self.workerThread)  # Move the Worker object to the Thread object
        self.workerThread.start() 
       
        self.back5.clicked.connect(self.gotoMainMenu)
        self.back5.setIcon(QtGui.QIcon('/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/GUI/index1.png'))
        self.back5.setIconSize(QtCore.QSize(40,40))
        self.login1.clicked.connect(self.startAI)

    def startAI(self):
        args=['/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/ALPR_APP/deepstream_lpr_app.py', '1', '3', '/opt/nvidia/deepstream/deepstream-5.1/samples/streams/AA.mp4', 'output.mp4']
        main(args)

    def display(self):
        print('==========Refreshing UI=============')
        f = open('/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/ALPR_APP/MyFile.json',)    
        data = json.load(f)
        name=data["name"]
        self.label_12.setText(name)
        make=data["make"]       
        self.label_13.setText(make)
        model=data["model"]
        self.label_14.setText(model)
        color=data["color"]
        self.label_11.setText(color) 
        pldb=data["licencePlateNumber"]
        self.label_10.setText(pldb)  
         # Closing file
        f.close()
        

        #for image detacted
        img = QtGui.QPixmap('/opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/ALRP_APP_Using_Deepstream/ALPR_APP/imagesdb/imagedb.jpg')
        self.imagedb.setPixmap(img)
        self.imagedb.setScaledContents(True)
  
    def gotoMainMenu(self):
        Main = MainMenu()
        widget.addWidget(Main)
        widget.setCurrentIndex(widget.currentIndex()+1)           
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")