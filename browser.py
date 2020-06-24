import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import sys
import mysql.connector

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # initializing UI for login dialog
        self.setGeometry(200,200,900,500)
        self.setWindowTitle("Browser Login!!")
        self.createUI()

        # creating vertical box object
        vbox = QVBoxLayout()
        vbox.addWidget(self.grpbox1)
        vbox.addWidget(self.grpbox2)
        vbox.addWidget(self.grpbox3)

        # setting vertical box object as layout
        self.setLayout(vbox)

        # this method call is to show UI
        self.show()

    def createUI(self):
        # creating groupbox object to group widgets together
        self.grpbox1 = QGroupBox()
        self.grpbox2 = QGroupBox()
        self.grpbox3 = QGroupBox()

        # creating horizontal box layout object
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()

        # creating label objects
        label1 = QLabel("Email : ")
        label2 = QLabel("Password: ")

        # creating lineedit objects to take inputs
        self.email = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        # creating button objects
        btn1 = QPushButton("Login")
        btn2 = QPushButton("Register")
        btn3 = QPushButton("Clear")

        # adding labels to horizontal box objects
        hbox1.addWidget(label1)
        hbox1.addWidget(self.email)
        hbox2.addWidget(label2)
        hbox2.addWidget(self.password)
        hbox3.addWidget(btn3)
        hbox3.addWidget(btn1)
        hbox3.addWidget(btn2)

        # setting groupbox layouts as horizontal box objects
        self.grpbox1.setLayout(hbox1)
        self.grpbox2.setLayout(hbox2)
        self.grpbox3.setLayout(hbox3)

        # connecting bottons to methods to make them fucntional
        btn1.clicked.connect(self.userLogin)
        btn2.clicked.connect(self.userRegistration)
        btn3.clicked.connect(self.clear)

    def clear(self):
        self.email.setText("")
        self.password.setText("")

    def userRegistration(self):
        self.setVisible(False)
        self.registration = RegistrationDialog()
        self.registration.exec_()


    def userLogin(self):
        try:
            # code to make connection to database
            cnx = mysql.connector.connect(host='localhost',user='root',password='',database='web_browser')
            crsr = cnx.cursor()
            # code to fetch information from database
            crsr.execute("SELECT email,passwd,user_id FROM users WHERE email LIKE '{}'".format(self.email.text()))
            data = crsr.fetchall()
            # check for valid username and password
            if len(data) == 0:
                QMessageBox.about(self,"Login Details","User doesn't exist!!")
            elif data[0][0]==self.email.text() and data[0][1]==self.password.text():
                # giving msg to user through msgbox
                global user_info
                user_info = int(data[0][2])
                crsr.close()
                cnx.close()
                window.close()
                self.browser = MainWindow()
            else:
                # giving msg to user through msgbox
                QMessageBox.about(self,"Login Details","Either username of password is wrong!!!")
        except:
            # giving msg to user through msgbox
            QMessageBox.about(self,"Connection","Something went wrong!!!")
        

class RegistrationDialog(QDialog):
    def __init__(self):
        super().__init__()
        # initializing UI for login dialog
        self.setGeometry(200,200,900,500)
        self.setWindowTitle("User Registration!!")
        self.createUI()

        # creating vertical box object
        vbox = QVBoxLayout()
        vbox.addWidget(self.grpbox1)
        vbox.addWidget(self.grpbox2)
        vbox.addWidget(self.grpbox3)
        vbox.addWidget(self.grpbox4)
        vbox.addWidget(self.grpbox5)

        # setting vertical box object as layout
        self.setLayout(vbox)

        # this method call is to show UI
        self.show()


    def createUI(self):
        # creating groupbox object to group widgets together
        self.grpbox1 = QGroupBox()
        self.grpbox2 = QGroupBox()
        self.grpbox3 = QGroupBox()
        self.grpbox4 = QGroupBox()
        self.grpbox5 = QGroupBox()

        # creating horizontal box layout object
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()

        # creating label objects
        label1 = QLabel("Name : ")
        label2 = QLabel("Contact No. :")
        label3 = QLabel("Email : ")
        label4 = QLabel("Password: ")

        # creating lineedit objects to take inputs
        self.name = QLineEdit()
        self.phone = QLineEdit()
        self.newEmail = QLineEdit()
        self.newPassword = QLineEdit()
        self.newPassword.setEchoMode(QLineEdit.Password)

        # creating button objects
        btn1 = QPushButton("Register")
        btn2 = QPushButton("Back")

        # adding labels to horizontal box objects
        hbox1.addWidget(label1)
        hbox1.addWidget(self.name)
        hbox2.addWidget(label2)
        hbox2.addWidget(self.phone)
        hbox3.addWidget(label3)
        hbox3.addWidget(self.newEmail)
        hbox4.addWidget(label4)
        hbox4.addWidget(self.newPassword)
        hbox5.addWidget(btn1)
        hbox5.addWidget(btn2)

        # setting groupbox layouts as horizontal box objects
        self.grpbox1.setLayout(hbox1)
        self.grpbox2.setLayout(hbox2)
        self.grpbox3.setLayout(hbox3)
        self.grpbox4.setLayout(hbox4)
        self.grpbox5.setLayout(hbox5)

        btn1.clicked.connect(self.register)
        btn2.clicked.connect(self.back)

    def register(self):
        try:
            #code to make connection to database
            cnx = mysql.connector.connect(host='localhost',user='root',password='',database='web_browser')
            crsr = cnx.cursor()
            # code to fetch information from database
            crsr.execute("SELECT email,passwd FROM users WHERE email LIKE '{}'".format(self.newEmail.text()))
            data = crsr.fetchall()
            # checking that user already exist or not
            if len(data) == 0:
                # code for inserting data into database
                crsr.execute("INSERT INTO users (user_id,name,contact_no,email,passwd) VALUES (NULL,'{}','{}','{}','{}')".format(self.name.text(),self.phone.text(),self.newEmail.text(),self.newPassword.text()))
                cnx.commit()
                crsr.close()
                cnx.close()
            elif data[0][0]==self.newEmail.text():
                # giving msg to user through msgbox
                QMessageBox.about(self,"Registration Details","User already registered!!!")
        except:
            # giving msg to user through msgbox
            QMessageBox.about(self,"Connection","Something went wrong!!!")

    def back(self):
        self.close()
        window.setVisible(True)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()

        # creating browser object
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        # creating object of status bar and adding it to MainWindow object
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # creating object of tool bar and adding it to MainWindow object
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        # creating action object and adding it to toolbar
        back_btn = QAction(QIcon(os.path.join('icons', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # creating action object and adding it to toolbar
        next_btn = QAction(QIcon(os.path.join('icons', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # creating action object and adding it to toolbar
        reload_btn = QAction(QIcon(os.path.join('icons', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # creating action object and adding it to toolbar
        home_btn = QAction(QIcon(os.path.join('icons', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # creating label object to add icon in toolbar
        self.httpsicon = QLabel()  
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        # creating lineEdit object to get url and adding it to toolbar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        # creating action object and adding it to toolbar
        stop_btn = QAction(QIcon(os.path.join('icons', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # adding menu to menubar
        history_menu = self.menuBar().addMenu("&History")

        # adding action to menubar
        show_history_action = QAction("Show History",self)
        show_history_action.triggered.connect(self.showUserHistory)
        history_menu.addAction(show_history_action)

        # adding menu to menubar
        bookmark_menu = self.menuBar().addMenu("&Bookmark")

        # adding action to menubar
        show_bookmark_action = QAction("Show Bookmarks",self)
        show_bookmark_action.triggered.connect(self.showUserBookmark)
        bookmark_menu.addAction(show_bookmark_action)

        # adding action to menubar
        save_bookmark_action = QAction("Save page as Bookmark",self)
        save_bookmark_action.triggered.connect(self.saveUserBookmark)
        bookmark_menu.addAction(save_bookmark_action)

        self.browser.urlChanged.connect(self.addHistory)

        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

        self.setCentralWidget(self.browser)
        self.setGeometry(200,200,1200,650)
        self.show()


    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    # Does not receive the Url
    def navigate_to_url(self):  
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):

        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'lock-ssl.png')))

        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - kkc Browser" % title)

    # creating object of showUserHistory class and executing it to show history
    def showUserHistory(self):
        history = showHistory()
        history.exec_()

    # creating object of showUserBookmark class and executing it to show bookmarks
    def showUserBookmark(self):
        bookmark = showBookmark()
        bookmark.exec_()

    # method to save user Bookmarks to database
    def saveUserBookmark(self):
        url = self.browser.url().toString()
        url = url[:255]
        cnx = mysql.connector.connect(host='localhost',user='root',password='',database='web_browser')
        crsr = cnx.cursor()
        # code to insert information from database
        crsr.execute("INSERT INTO user_bookmarks (user_id,bookmarks) VALUES ({},'{}')".format(user_info,url))
        cnx.commit()

    # method foe adding user history to database
    def addHistory(self):
        url = self.browser.url().toString()
        url = url[:255]
        cnx = mysql.connector.connect(host='localhost',user='root',password='',database='web_browser')
        crsr = cnx.cursor()
        # code to fetch information from database
        crsr.execute("INSERT INTO user_history (user_id,history) VALUES ({},'{}')".format(user_info,url))
        cnx.commit()
        

# class to show saved history in Qdialog object
class showHistory(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(1200,220,350,500)
        self.setWindowTitle("History")
        self.createHistoryUI()
        self.setLayout(self.vbox)
        cnx = mysql.connector.connect(host='localhost',user='root',password='',database='web_browser')
        crsr = cnx.cursor()
        crsr.execute("SELECT history FROM user_history WHERE user_id={}".format(user_info))
        history_data = crsr.fetchall()
        history = ''
        i = 1
        for data in history_data:
            history = history + str(i) + ". " +str(data[0]) + "\n"
            i = i + 1
        self.history.setPlainText(history)
        self.show()

    # creating UI to show user history
    def createHistoryUI(self):
        self.history = QPlainTextEdit()
        btn = QPushButton("Clear History")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(btn)
        self.vbox.addWidget(self.history)

        btn.clicked.connect(self.clearHistory)

    # to clear user history
    def clearHistory(self):
        self.history.setPlainText("")
        cnx = mysql.connector.connect(host='localhost',user='root',password='',database='web_browser')
        crsr = cnx.cursor()
        crsr.execute("DELETE FROM user_history WHERE user_id={}".format(user_info))
        cnx.commit()

# class to show saved bookmarks in Qdialog object
class showBookmark(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(1200,220,350,500)
        self.setWindowTitle("Bookmark")
        self.createBookmarkUI()
        self.setLayout(self.vbox)
        cnx = mysql.connector.connect(host='localhost',user='root',password='',database='web_browser')
        crsr = cnx.cursor()
        crsr.execute("SELECT bookmarks FROM user_bookmarks WHERE user_id={}".format(user_info))
        bookmark_data = crsr.fetchall()
        bookmark = ''
        i = 1
        for data in bookmark_data:
            bookmark = bookmark + str(i) + ". " +str(data[0]) + "\n"
            i = i + 1
        self.bookmark.setPlainText(bookmark)
        self.show()

    # creating UI to show user bookmarks
    def createBookmarkUI(self):
        self.bookmark = QPlainTextEdit()
        btn = QPushButton("Clear Bookmark")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(btn)
        self.vbox.addWidget(self.bookmark)

        btn.clicked.connect(self.clearBookmark)

    # to clear user bookmarks
    def clearBookmark(self):
        self.bookmark.setPlainText("")
        cnx = mysql.connector.connect(host='localhost',user='root',password='',database='web_browser')
        crsr = cnx.cursor()
        crsr.execute("DELETE FROM user_bookmarks WHERE user_id={}".format(user_info))
        cnx.commit()


if __name__=="__main__":
    # creating an application object
    app =  QApplication(sys.argv)
    # creating LoginDialog class object
    window = LoginWindow()
    # code for terminating application
    sys.exit(app.exec_())
