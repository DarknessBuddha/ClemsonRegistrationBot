import sys
import registration_bot as rb
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QApplication, QStackedWidget
from threading import Thread
import os


# UI for bot
class BotUi(QDialog):
    def __init__(self):
        super().__init__()
        self.script_thread: Thread = Thread()
        loadUi('BotUI.ui', self)
        self.start_button.clicked.connect(self.start_script)

    def get_username(self):
        return self.username_box.text()

    def get_password(self):
        return self.password_box.text()

    def get_time(self):
        time = self.time_box.time()
        return time.hour(), time.minute()

    def start_script(self):
        self.script_thread = Thread(target=rb.script,
                                    args=(self.get_username(), self.get_password(), self.get_time())
                                    )
        self.script_thread.start()


# set up app
app = QApplication(sys.argv)

# set up widgets
widgets = QStackedWidget()
botUI = BotUi()
widgets.addWidget(botUI)
widgets.setFixedWidth(852)
widgets.setFixedHeight(480)
widgets.show()

# run app
try:
    sys.exit(app.exec())

finally:
    print('Finished')
    os._exit(0)