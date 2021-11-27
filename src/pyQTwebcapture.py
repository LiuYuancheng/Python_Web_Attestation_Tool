import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

# https://stackoverflow.com/questions/55231170/taking-a-screenshot-of-a-web-page-in-pyqt5
# https://stackoverflow.com/questions/51154871/python-3-7-0-no-module-named-pyqt5-qtwebenginewidgets
class Screenshot(QWebEngineView):

    def capture(self, url, output_file):
        self.output_file = output_file
        self.load(QUrl(url))
        self.loadFinished.connect(self.on_loaded)
        # Create hidden view without scrollbars
        self.setAttribute(Qt.WA_DontShowOnScreen)
        self.page().settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, False)
        self.show()

    def on_loaded(self):
        size = self.page().contentsSize().toSize()
        self.resize(size)
        # Wait for resize
        QTimer.singleShot(1000, self.take_screenshot)

    def take_screenshot(self):
        self.grab().save(self.output_file, b'PNG')
        self.app.quit()


app = QApplication(sys.argv)
s = Screenshot()
s.app = app
s.capture('https://pypi.org/project/PyQt5/', 'webpage.png')
sys.exit(app.exec_())