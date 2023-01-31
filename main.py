from PyQt5.QtWidgets import QApplication,QWidget,QStackedWidget,QHBoxLayout

from user_data.login import PageController
from Dashboard.dashboard import DashboardPageController,LOG_OUT_PAGE,ADD_PATIENT_PAGE,FIND_PATIENT_PAGE,PATIENT_PAGE
from data.Database_win import DatabasePageController,ADD_PATIENT,PATIENTS,SEARCH_PATIENT

import sys
import os


LOGIN_PAGE = 0
DASHBOARD_PAGE = 1
DATABASE_PAGE = 2

################################### #TODO: comment it after
DASHBOARD_PATH = "./Dashboard"
DATABASE_PATH = "./data"

###################################


def resource_path():
    try: 
        base_path = sys._MEIPASS
    
    except:
        base_path = os.path.abspath(".")

    return base_path

#PATH = os.path.dirname(os.path.abspath(__file__))

PATH = resource_path()

DASHBOARD_PATH = PATH
DATABASE_PATH = PATH



class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.app_pages_init()
        self.stack_init()
        self.signal_init()

    def app_pages_init(self):
        self.login = PageController()
        self.dashboard = DashboardPageController(DASHBOARD_PATH)
        self.database = DatabasePageController(DATABASE_PATH)    
        
    def stack_init(self):
        self.stack = QStackedWidget()
        self.stack.addWidget(self.login)
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.database)
        self.box = QHBoxLayout()
        self.box.setContentsMargins(0,0,0,0)
        self.box.addWidget(self.stack)
        self.setLayout(self.box)
        
    def signal_init(self):
        self.login.pageSignal.connect(lambda: self.page_change(DASHBOARD_PAGE))
        self.database.db_controller_signal.connect(lambda: self.page_change(DASHBOARD_PAGE))
        self.dashboard.dashboard_controller_signal.connect(self.dashboard_signal)

    def dashboard_signal(self,type_signal:int): 
        if type_signal == LOG_OUT_PAGE:
            self.page_change(LOGIN_PAGE)
        elif type_signal == ADD_PATIENT_PAGE:
            self.page_change(DATABASE_PAGE)
            self.database.db_show_signal.emit(ADD_PATIENT)
        elif type_signal == FIND_PATIENT_PAGE:
            self.page_change(DATABASE_PAGE)
            self.database.db_show_signal.emit(SEARCH_PATIENT)
        elif type_signal == PATIENT_PAGE:
            self.page_change(DATABASE_PAGE)
        else:
            raise AttributeError

    def page_change(self,index:int):
        self.stack.setCurrentIndex(index) 

    def leaveEvent(self, a0):
        
        return super().leaveEvent(a0)



def main():
    try:
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    except:
        pass

    app = QApplication([])
    main_win = MainWin()
    main_win.showMaximized()
    app.exec()



if __name__ == "__main__":
    main()