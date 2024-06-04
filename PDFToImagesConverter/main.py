import sys
from custome_errors import *
sys.excepthook = my_excepthook
import os
import fitz
import update
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        layout.addWidget(qt.QLabel(_("path")))
        self.path=qt.QLineEdit()
        self.path.setReadOnly(True)
        layout.addWidget(self.path)
        self.selectPDFFile=qt.QPushButton(_("select pdf file"))
        self.selectPDFFile.setDefault(True)
        self.selectPDFFile.clicked.connect(self.on_select_pdf_file)
        layout.addWidget(self.selectPDFFile)
        self.convert=qt.QPushButton(_("convert"))
        self.convert.setDefault(True)
        self.convert.clicked.connect(self.on_convert)
        layout.addWidget(self.convert)
        self.setting=qt.QPushButton(_("settings"))
        self.setting.setDefault(True)
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def on_select_pdf_file(self):
        file=qt.QFileDialog(self)
        file.setDefaultSuffix("pdf")
        if file.exec()==file.DialogCode.Accepted:
            self.path.setText(file.selectedFiles()[0])
            self.path.setFocus()
    def on_convert(self):
        PDFFile=fitz.open(self.path.text())
        path=self.path.text().split("/")
        path.pop(-1)
        output_folder="/".join(path) + "/output"
        if not os .path.exists(output_folder):
            os.makedirs(output_folder)
        try:
            for pageNumber in range(PDFFile.page_count):
                page=PDFFile.load_page(pageNumber)
                pagePath=output_folder + "/{}.png".format(str(pageNumber + 1))
                pix=page.get_pixmap()
                pix.save(pagePath)
            qt.QMessageBox.information(self,_("done"),_("converted "))
        except:
            qt.QMessageBox.warning(self,_("error"),_("can't convert this file"))
App=qt.QApplication([])
w=main()
w.show()
App.setStyle('fusion')
App.exec()