from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
import sys

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		self.browser =QWebEngineView()
		self.browser.setUrl(QUrl('https://google.com'))
		self.setCentralWidget(self.browser)
		self.showMaximized()
		#navigation bar
		navbar=QToolBar()
		self.addToolBar(navbar)
		back_btn=QAction('<<<',self)
		back_btn.triggered.connect(self.browser.back)
		navbar.addAction(back_btn)
		forward_btn=QAction('>>>',self)
		forward_btn.triggered.connect(self.browser.forward)
		navbar.addAction(forward_btn)
		reload_btn=QAction('(())',self)
		reload_btn.triggered.connect(self.browser.reload)
		navbar.addAction(reload_btn)
		home_btn=QAction('home',self)
		home_btn.triggered.connect(self.navigate_to_home)
		navbar.addAction(home_btn)
		self.url_bar=QLineEdit()
		navbar.addWidget(self.url_bar)
		self.url_bar.returnPressed.connect(self.navigate_to_url)
		
		self.browser.urlChanged.connect(self.update_url)



	def navigate_to_home(self):
		home_page=r'https://google.com'
		self.browser.setUrl(QUrl(home_page))

	def navigate_to_url(self):
		url=self.url_bar.text()
		self.browser.setUrl(QUrl(url))

	def update_url(self,new_url):
		self.url_bar.setText(new_url.toString())





app=QApplication(sys.argv)
QApplication.setApplicationName("My Simple Browser")
window=MainWindow()
app.exec()
