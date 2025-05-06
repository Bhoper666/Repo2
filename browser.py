import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserTab(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setUrl(QUrl("https://www.google.com"))

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RBrowser")
        self.setGeometry(100, 100, 1200, 800)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)

        self.add_new_tab(QUrl("https://www.google.com"), "Homepage")


        # Navigation Bar
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        # Back button
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.go_back)
        nav_bar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.go_forward)
        nav_bar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.reload_page)
        nav_bar.addAction(reload_btn)

        # New Tab button
        new_tab_btn = QAction("New Tab", self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        nav_bar.addAction(new_tab_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        # Update URL bar when page loads
        self.tab_widget.currentChanged.connect(self.update_url_bar)
        self.update_url_bar(0)


    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = BrowserTab()

        i = self.tab_widget.addTab(browser, label)
        self.tab_widget.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                     self.update_tab_title(browser, qurl))
        browser.loadFinished.connect(lambda ok, browser=browser:
                                      self.update_tab_title(browser, browser.url()))


    def update_tab_title(self, browser, qurl):
          index = self.tab_widget.indexOf(browser)
          if index >=0:
            title = browser.page().title()
            self.tab_widget.setTabText(index, title)


    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        browser = self.tab_widget.currentWidget()
        browser.setUrl(QUrl(url))


    def update_url_bar(self, i):
        if i >= 0:  # Check if a tab exists
            browser = self.tab_widget.widget(i)
            if browser:
                self.url_bar.setText(browser.url().toString())

    def go_back(self):
        browser = self.tab_widget.currentWidget()
        if browser:
            browser.back()

    def go_forward(self):
        browser = self.tab_widget.currentWidget()
        if browser:
            browser.forward()

    def reload_page(self):
        browser = self.tab_widget.currentWidget()
        if browser:
            browser.reload()

    def close_tab(self, i):
        if self.tab_widget.count() < 2:  # Don't allow closing the last tab
            return
        self.tab_widget.removeTab(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
