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
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(764, 565)
        MainWindow.setMinimumSize(QSize(764, 565))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_titulo = QLabel(self.centralwidget)
        self.label_titulo.setObjectName(u"label_titulo")
        font = QFont()
        font.setFamilies([u"Bahnschrift"])
        font.setPointSize(28)
        font.setBold(True)
        self.label_titulo.setFont(font)
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_titulo, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.centralwidget)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.logo_hori = QLabel(self.frame_6)
        self.logo_hori.setObjectName(u"logo_hori")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_hori.sizePolicy().hasHeightForWidth())
        self.logo_hori.setSizePolicy(sizePolicy)
        self.logo_hori.setMinimumSize(QSize(580, 108))
        self.logo_hori.setPixmap(QPixmap(u"../imgs/extrato_horizontal.png"))
        self.logo_hori.setScaledContents(True)
        self.logo_hori.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.logo_hori)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)


        self.gridLayout_5.addWidget(self.frame_6, 0, 0, 1, 1)


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
        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setFamilies([u"Bahnschrift"])
        font1.setPointSize(18)
        self.groupBox.setFont(font1)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamilies([u"Bahnschrift"])
        font2.setPointSize(12)
        font2.setWeight(QFont.Light)
        self.comboBox.setFont(font2)

        self.verticalLayout_4.addWidget(self.comboBox)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.groupBox_2 = QGroupBox(self.frame_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font1)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget_2 = QStackedWidget(self.groupBox_2)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stackedWidget_2.sizePolicy().hasHeightForWidth())
        self.stackedWidget_2.setSizePolicy(sizePolicy2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        sizePolicy.setHeightForWidth(self.page_3.sizePolicy().hasHeightForWidth())
        self.page_3.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.page_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = QScrollArea(self.page_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaLayout = QWidget()
        self.scrollAreaLayout.setObjectName(u"scrollAreaLayout")
        self.scrollAreaLayout.setGeometry(QRect(0, 0, 300, 110))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollAreaLayout.sizePolicy().hasHeightForWidth())
        self.scrollAreaLayout.setSizePolicy(sizePolicy3)
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

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_6 = QGridLayout(self.page_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label = QLabel(self.page_4)
        self.label.setObjectName(u"label")
        font4 = QFont()
        font4.setFamilies([u"Bahnschrift"])
        font4.setPointSize(14)
        font4.setBold(True)
        self.label.setFont(font4)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 1, 1, 1)

        self.tableWidget = QTableWidget(self.page_4)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        font5 = QFont()
        font5.setFamilies([u"Bahnschrift"])
        font5.setPointSize(14)
        font5.setWeight(QFont.Light)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font5);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font5);
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font5);
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        font6 = QFont()
        font6.setFamilies([u"Bahnschrift"])
        font6.setPointSize(12)
        self.tableWidget.setFont(font6)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSortingEnabled(True)

        self.gridLayout_6.addWidget(self.tableWidget, 3, 0, 1, 2)

        self.pushButton = QPushButton(self.page_4)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy4)
        font7 = QFont()
        font7.setFamilies([u"Bahnschrift"])
        font7.setPointSize(12)
        font7.setWeight(QFont.ExtraLight)
        self.pushButton.setFont(font7)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.pushButton.setIcon(icon)

        self.gridLayout_6.addWidget(self.pushButton, 0, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page_4)

        self.verticalLayout_5.addWidget(self.stackedWidget_2)

        self.frame = QFrame(self.groupBox_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add = QPushButton(self.frame)
        self.pushButton_add.setObjectName(u"pushButton_add")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.pushButton_add.setIcon(icon1)
        self.pushButton_add.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_add)

        self.pushButton_remove = QPushButton(self.frame)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.pushButton_remove.setIcon(icon2)
        self.pushButton_remove.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_remove)

        self.pushButton_update = QPushButton(self.frame)
        self.pushButton_update.setObjectName(u"pushButton_update")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailMessageNew))
        self.pushButton_update.setIcon(icon3)
        self.pushButton_update.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_update)

        self.pushButton_save = QPushButton(self.frame)
        self.pushButton_save.setObjectName(u"pushButton_save")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.pushButton_save.setIcon(icon4)
        self.pushButton_save.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_save)


        self.verticalLayout_5.addWidget(self.frame)


        self.verticalLayout.addWidget(self.groupBox_2)


        self.horizontalLayout_3.addWidget(self.frame_2)

        self.frame_4 = QFrame(self.page)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_extrato = QLabel(self.frame_4)
        self.label_extrato.setObjectName(u"label_extrato")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_extrato.sizePolicy().hasHeightForWidth())
        self.label_extrato.setSizePolicy(sizePolicy5)
        font8 = QFont()
        font8.setFamilies([u"Bahnschrift"])
        font8.setPointSize(18)
        font8.setBold(False)
        self.label_extrato.setFont(font8)
        self.label_extrato.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.label_extrato)

        self.pushButton_upload = QPushButton(self.frame_4)
        self.pushButton_upload.setObjectName(u"pushButton_upload")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pushButton_upload.sizePolicy().hasHeightForWidth())
        self.pushButton_upload.setSizePolicy(sizePolicy6)
        font9 = QFont()
        font9.setFamilies([u"Lucida Fax"])
        font9.setPointSize(12)
        self.pushButton_upload.setFont(font9)
        icon5 = QIcon()
        icon5.addFile(u"../imgs/upload-icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_upload.setIcon(icon5)
        self.pushButton_upload.setIconSize(QSize(65, 63))

        self.verticalLayout_3.addWidget(self.pushButton_upload)

        self.line = QFrame(self.frame_4)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_executar = QPushButton(self.frame_3)
        self.pushButton_executar.setObjectName(u"pushButton_executar")
        sizePolicy4.setHeightForWidth(self.pushButton_executar.sizePolicy().hasHeightForWidth())
        self.pushButton_executar.setSizePolicy(sizePolicy4)
        self.pushButton_executar.setMinimumSize(QSize(175, 50))
        font10 = QFont()
        font10.setFamilies([u"Bahnschrift"])
        font10.setPointSize(14)
        font10.setWeight(QFont.ExtraLight)
        font10.setItalic(True)
        self.pushButton_executar.setFont(font10)
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSend))
        self.pushButton_executar.setIcon(icon6)

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
        font11 = QFont()
        font11.setFamilies([u"Arial Rounded MT"])
        font11.setPointSize(12)
        font11.setBold(True)
        self.label_carregando.setFont(font11)
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
        self.menubar.setGeometry(QRect(0, 0, 764, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_titulo.setText(QCoreApplication.translate("MainWindow", u"Gerador de Extratos", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Escolha o Banco", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Empresas Dispon\u00edveis", None))
        self.label_aviso.setText(QCoreApplication.translate("MainWindow", u"Primeiramente, escolha o banco", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Empresa", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Palavra", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Valor", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"C/D", None));
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Voltar", None))
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

