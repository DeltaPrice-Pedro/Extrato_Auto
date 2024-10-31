# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window_extratos.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(624, 415)
        MainWindow.setMinimumSize(QSize(624, 415))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.logo_hori = QLabel(self.centralwidget)
        self.logo_hori.setObjectName(u"logo_hori")
        self.logo_hori.setMinimumSize(QSize(580, 108))
        self.logo_hori.setPixmap(QPixmap(u"../imgs/extrato_horizontal.png"))
        self.logo_hori.setScaledContents(True)

        self.gridLayout_5.addWidget(self.logo_hori, 0, 1, 1, 1)

        self.label_titulo = QLabel(self.centralwidget)
        self.label_titulo.setObjectName(u"label_titulo")
        font = QFont()
        font.setFamilies([u"Verdana"])
        font.setPointSize(22)
        font.setBold(True)
        self.label_titulo.setFont(font)
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_titulo, 1, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 0, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_extrato = QLabel(self.page)
        self.label_extrato.setObjectName(u"label_extrato")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_extrato.sizePolicy().hasHeightForWidth())
        self.label_extrato.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Arial Rounded MT"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.label_extrato.setFont(font1)

        self.gridLayout_2.addWidget(self.label_extrato, 0, 1, 1, 1)

        self.comboBox = QComboBox(self.page)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_2.addWidget(self.comboBox, 1, 0, 1, 1)

        self.label_banco = QLabel(self.page)
        self.label_banco.setObjectName(u"label_banco")
        sizePolicy.setHeightForWidth(self.label_banco.sizePolicy().hasHeightForWidth())
        self.label_banco.setSizePolicy(sizePolicy)
        self.label_banco.setFont(font1)

        self.gridLayout_2.addWidget(self.label_banco, 0, 0, 1, 1)

        self.pushButton_upload = QPushButton(self.page)
        self.pushButton_upload.setObjectName(u"pushButton_upload")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_upload.sizePolicy().hasHeightForWidth())
        self.pushButton_upload.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamilies([u"Lucida Fax"])
        font2.setPointSize(12)
        self.pushButton_upload.setFont(font2)
        icon = QIcon()
        icon.addFile(u"../imgs/upload-icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_upload.setIcon(icon)
        self.pushButton_upload.setIconSize(QSize(65, 63))

        self.gridLayout_2.addWidget(self.pushButton_upload, 1, 1, 3, 2)

        self.label_empresa = QLabel(self.page)
        self.label_empresa.setObjectName(u"label_empresa")
        sizePolicy.setHeightForWidth(self.label_empresa.sizePolicy().hasHeightForWidth())
        self.label_empresa.setSizePolicy(sizePolicy)
        self.label_empresa.setFont(font1)

        self.gridLayout_2.addWidget(self.label_empresa, 2, 0, 1, 1)

        self.scrollArea = QScrollArea(self.page)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setEnabled(False)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 333, 69))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_aviso = QLabel(self.scrollAreaWidgetContents_2)
        self.label_aviso.setObjectName(u"label_aviso")
        font3 = QFont()
        font3.setFamilies([u"Rockwell"])
        font3.setPointSize(12)
        font3.setBold(False)
        font3.setItalic(True)
        font3.setStrikeOut(False)
        self.label_aviso.setFont(font3)
        self.label_aviso.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_aviso)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_2.addWidget(self.scrollArea, 3, 0, 1, 1)

        self.pushButton_executar = QPushButton(self.page)
        self.pushButton_executar.setObjectName(u"pushButton_executar")

        self.gridLayout_2.addWidget(self.pushButton_executar, 7, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 7, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 7, 1, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_4 = QGridLayout(self.page_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalSpacer = QSpacerItem(243, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(242, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(243, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.label_carregando = QLabel(self.page_2)
        self.label_carregando.setObjectName(u"label_carregando")
        self.label_carregando.setFont(font1)
        self.label_carregando.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_carregando, 2, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(242, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 2, 2, 1, 1)

        self.label_load = QLabel(self.page_2)
        self.label_load.setObjectName(u"label_load")
        self.label_load.setMaximumSize(QSize(128, 128))
        self.label_load.setPixmap(QPixmap(u"../imgs/load.gif"))
        self.label_load.setScaledContents(True)

        self.gridLayout_4.addWidget(self.label_load, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout.addWidget(self.stackedWidget, 1, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 624, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo_hori.setText("")
        self.label_titulo.setText(QCoreApplication.translate("MainWindow", u"Gerador de Extratos", None))
        self.label_extrato.setText(QCoreApplication.translate("MainWindow", u"Insira o extrato:", None))
        self.label_banco.setText(QCoreApplication.translate("MainWindow", u"Escolha o banco:", None))
        self.pushButton_upload.setText("")
        self.label_empresa.setText(QCoreApplication.translate("MainWindow", u"Empresas dispon\u00edveis:", None))
        self.label_aviso.setText(QCoreApplication.translate("MainWindow", u"Primeiramente, escolha o banco", None))
        self.pushButton_executar.setText(QCoreApplication.translate("MainWindow", u"Executar", None))
#if QT_CONFIG(shortcut)
        self.pushButton_executar.setShortcut(QCoreApplication.translate("MainWindow", u"Enter", None))
#endif // QT_CONFIG(shortcut)
        self.label_carregando.setText(QCoreApplication.translate("MainWindow", u"Carregando...", None))
        self.label_load.setText("")
    # retranslateUi

