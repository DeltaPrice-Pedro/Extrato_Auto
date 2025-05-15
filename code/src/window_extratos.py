# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window_extratos.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(712, 493)
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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_hori.sizePolicy().hasHeightForWidth())
        self.logo_hori.setSizePolicy(sizePolicy)
        self.logo_hori.setMinimumSize(QSize(580, 108))
        self.logo_hori.setPixmap(QPixmap(u"../imgs/extrato_horizontal.png"))
        self.logo_hori.setScaledContents(True)

        self.gridLayout_5.addWidget(self.logo_hori, 0, 1, 1, 1)

        self.label_titulo = QLabel(self.centralwidget)
        self.label_titulo.setObjectName(u"label_titulo")
        font = QFont()
        font.setFamilies([u"Bahnschrift"])
        font.setPointSize(28)
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
        self.horizontalLayout_3 = QHBoxLayout(self.page)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame_2 = QFrame(self.page)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.label_banco = QLabel(self.frame_2)
        self.label_banco.setObjectName(u"label_banco")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_banco.sizePolicy().hasHeightForWidth())
        self.label_banco.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"Bahnschrift"])
        font1.setPointSize(16)
        font1.setBold(False)
        self.label_banco.setFont(font1)
        self.label_banco.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_banco)

        self.comboBox = QComboBox(self.frame_2)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamilies([u"Bahnschrift"])
        font2.setPointSize(12)
        font2.setWeight(QFont.Light)
        self.comboBox.setFont(font2)

        self.verticalLayout.addWidget(self.comboBox)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_empresa = QLabel(self.frame_2)
        self.label_empresa.setObjectName(u"label_empresa")
        sizePolicy1.setHeightForWidth(self.label_empresa.sizePolicy().hasHeightForWidth())
        self.label_empresa.setSizePolicy(sizePolicy1)
        self.label_empresa.setFont(font1)
        self.label_empresa.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_empresa)

        self.scrollArea = QScrollArea(self.frame_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaLayout = QWidget()
        self.scrollAreaLayout.setObjectName(u"scrollAreaLayout")
        self.scrollAreaLayout.setGeometry(QRect(0, 0, 312, 69))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaLayout)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_aviso = QLabel(self.scrollAreaLayout)
        self.label_aviso.setObjectName(u"label_aviso")
        font3 = QFont()
        font3.setFamilies([u"Rockwell"])
        font3.setPointSize(14)
        font3.setBold(False)
        font3.setItalic(True)
        font3.setStrikeOut(False)
        self.label_aviso.setFont(font3)
        self.label_aviso.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_aviso)

        self.scrollArea.setWidget(self.scrollAreaLayout)

        self.verticalLayout.addWidget(self.scrollArea)

        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add = QPushButton(self.frame)
        self.pushButton_add.setObjectName(u"pushButton_add")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.pushButton_add.setIcon(icon)
        self.pushButton_add.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_add)

        self.pushButton_remove = QPushButton(self.frame)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.pushButton_remove.setIcon(icon1)

        self.horizontalLayout.addWidget(self.pushButton_remove)

        self.pushButton_update = QPushButton(self.frame)
        self.pushButton_update.setObjectName(u"pushButton_update")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailMessageNew))
        self.pushButton_update.setIcon(icon2)

        self.horizontalLayout.addWidget(self.pushButton_update)


        self.verticalLayout.addWidget(self.frame)


        self.horizontalLayout_3.addWidget(self.frame_2)

        self.frame_4 = QFrame(self.page)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_extrato = QLabel(self.frame_4)
        self.label_extrato.setObjectName(u"label_extrato")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_extrato.sizePolicy().hasHeightForWidth())
        self.label_extrato.setSizePolicy(sizePolicy3)
        self.label_extrato.setFont(font1)
        self.label_extrato.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_extrato)

        self.pushButton_upload = QPushButton(self.frame_4)
        self.pushButton_upload.setObjectName(u"pushButton_upload")
        sizePolicy2.setHeightForWidth(self.pushButton_upload.sizePolicy().hasHeightForWidth())
        self.pushButton_upload.setSizePolicy(sizePolicy2)
        font4 = QFont()
        font4.setFamilies([u"Lucida Fax"])
        font4.setPointSize(12)
        self.pushButton_upload.setFont(font4)
        icon3 = QIcon()
        icon3.addFile(u"../imgs/upload-icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_upload.setIcon(icon3)
        self.pushButton_upload.setIconSize(QSize(65, 63))

        self.verticalLayout_3.addWidget(self.pushButton_upload)

        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_executar = QPushButton(self.frame_3)
        self.pushButton_executar.setObjectName(u"pushButton_executar")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_executar.sizePolicy().hasHeightForWidth())
        self.pushButton_executar.setSizePolicy(sizePolicy4)
        self.pushButton_executar.setMinimumSize(QSize(150, 50))
        font5 = QFont()
        font5.setFamilies([u"Bahnschrift"])
        font5.setPointSize(14)
        font5.setWeight(QFont.ExtraLight)
        font5.setItalic(True)
        self.pushButton_executar.setFont(font5)
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSend))
        self.pushButton_executar.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.pushButton_executar)


        self.verticalLayout_3.addWidget(self.frame_3)


        self.horizontalLayout_3.addWidget(self.frame_4)

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
        font6 = QFont()
        font6.setFamilies([u"Arial Rounded MT"])
        font6.setPointSize(12)
        font6.setBold(True)
        self.label_carregando.setFont(font6)
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


        self.gridLayout_3.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.gridLayout_3.addItem(self.verticalSpacer, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 712, 22))
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
        self.label_banco.setText(QCoreApplication.translate("MainWindow", u"Escolha o Banco", None))
        self.label_empresa.setText(QCoreApplication.translate("MainWindow", u"Empresas Dispon\u00edveis", None))
        self.label_aviso.setText(QCoreApplication.translate("MainWindow", u"Primeiramente, escolha o banco", None))
        self.pushButton_add.setText("")
        self.pushButton_remove.setText("")
        self.pushButton_update.setText("")
        self.label_extrato.setText(QCoreApplication.translate("MainWindow", u"Insira o Extrato", None))
        self.pushButton_upload.setText("")
        self.pushButton_executar.setText(QCoreApplication.translate("MainWindow", u" Executar", None))
#if QT_CONFIG(shortcut)
        self.pushButton_executar.setShortcut(QCoreApplication.translate("MainWindow", u"Enter", None))
#endif // QT_CONFIG(shortcut)
        self.label_carregando.setText(QCoreApplication.translate("MainWindow", u"Carregando...", None))
        self.label_load.setText("")
    # retranslateUi

