from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
import sys
import os

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		global engine
		engines=["http://www.google.com/","http://bing.com/","https://in.yahoo.com/",
				"https://duckduckgo.com/","https://www.wolframalpha.com/","http://baidu.com/"]
		engine=engines[0]
		self.showMaximized()
		#navigation bar
		navbar=QToolBar()
		self.addToolBar(navbar)
		back_btn=QAction('🡰',self)
		back_btn.triggered.connect(lambda:self.tabs.currentWidget().back())
		navbar.addAction(back_btn)
		forward_btn=QAction('🡲',self)
		forward_btn.triggered.connect(lambda:self.tabs.currentWidget().forward())
		navbar.addAction(forward_btn)
		reload_btn=QAction('⭮',self)
		reload_btn.triggered.connect(lambda:self.tabs.currentWidget().reload())
		navbar.addAction(reload_btn)
		home_btn=QAction('⌂',self)
		home_btn.triggered.connect(self.navigate_to_home)
		navbar.addAction(home_btn)
		self.url_bar=QLineEdit()
		navbar.addWidget(self.url_bar)
		self.url_bar.returnPressed.connect(self.navigate_to_url)
		
		#self.browser.urlChanged.connect(self.update_url)
		self.tabs=QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleClick)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.setCentralWidget(self.tabs)

		self.add_new_tab()



	def navigate_to_home(self):
		home_page=engine
		self.tabs.currentWidget().setUrl(QUrl(home_page))

	def navigate_to_url(self):	
		url=self.url_bar.text()
		try:
			self.tabs.currentWidget().setUrl(QUrl(url))
		except 
   			raise
		else:
			self.open_file_in_browser(url)

		self.tabs.currentWidget().setUrl(QUrl(url))

	def update_url(self,new_url,browser=None):

		if browser is not self.tabs.currentWidget():
			return
		self.url_bar.setText(new_url.toString())

	def add_new_tab(self,qurl=None,label="Blank"):
		if qurl is None:
		    qurl=QUrl(engine)
		tab=QWebEngineView()
		tab.setUrl(qurl)
		i=self.tabs.addTab(tab,label)

		tab.urlChanged.connect(lambda qurl,browser=tab:self.update_url(qurl,tab))
		tab.loadFinished.connect(lambda _,i=i,browser=tab:
		                            self.tabs.setTabText(i,tab.page().title()))

	def tab_open_doubleClick(self,i):
		if i== -1:
			self.add_new_tab()
	def current_tab_changed(self,i):
		qurl=self.tabs.currentWidget().url()
		self.update_url(qurl,self.tabs.currentWidget())
		#self.update_title(self.tabs.currentWidget())
	def close_current_tab(self,i):
		if self.tabs.count()<2:
			return
		self.tabs.removeTab(i)
	def update_title(self,browser):
		if browse is not self.tabs.currentWidget():
			return
		title=self.tabs.currentWidget().page().title()
		self.setWindowTitle(title)

	def open_file_in_browser(self,path):
		f = open('temp.html','w')
		html=f"""
				<!DOCTYPE html>
				<html>
				  <head>
				    <title>Title of the document</title>
				  </head>
				  <body>
				    <h1>PDF Example</h1>
				    <p>Open a PDF file <a href={path}>example</a>.</p>
				  </body>
				</html>
			"""
		f.write(html)
		f.close()
		path=os.path.abspath("temp.html")
		self.tabs.currentWidget().setUrl(QUrl(path))



app=QApplication(sys.argv)
QApplication.setApplicationName("My Simple Browser")
window=MainWindow()
app.exec()
