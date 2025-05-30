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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(667, 697)
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
        self.logo_hori.setMaximumSize(QSize(580, 108))
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
        self.frame_5 = QFrame(self.groupBox_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.line_2 = QFrame(self.frame_5)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setMinimumSize(QSize(0, 5))
        self.line_2.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        self.line_2.setFrameShadow(QFrame.Shadow.Plain)
        self.line_2.setLineWidth(-1)
        self.line_2.setFrameShape(QFrame.Shape.HLine)

        self.horizontalLayout_4.addWidget(self.line_2)

        self.pushButton_reload = QPushButton(self.frame_5)
        self.pushButton_reload.setObjectName(u"pushButton_reload")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_reload.sizePolicy().hasHeightForWidth())
        self.pushButton_reload.setSizePolicy(sizePolicy2)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SyncSynchronizing))
        self.pushButton_reload.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.pushButton_reload)


        self.verticalLayout_5.addWidget(self.frame_5)

        self.stackedWidget_companie = QStackedWidget(self.groupBox_2)
        self.stackedWidget_companie.setObjectName(u"stackedWidget_companie")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.stackedWidget_companie.sizePolicy().hasHeightForWidth())
        self.stackedWidget_companie.setSizePolicy(sizePolicy3)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        sizePolicy.setHeightForWidth(self.page_3.sizePolicy().hasHeightForWidth())
        self.page_3.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.page_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_companie_info = QLabel(self.page_3)
        self.label_companie_info.setObjectName(u"label_companie_info")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_companie_info.sizePolicy().hasHeightForWidth())
        self.label_companie_info.setSizePolicy(sizePolicy4)
        font3 = QFont()
        font3.setFamilies([u"Bahnschrift"])
        font3.setPointSize(12)
        font3.setItalic(True)
        self.label_companie_info.setFont(font3)
        self.label_companie_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_companie_info, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(self.page_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setEnabled(False)
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy5)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaLayout = QWidget()
        self.scrollAreaLayout.setObjectName(u"scrollAreaLayout")
        self.scrollAreaLayout.setGeometry(QRect(0, 0, 366, 134))
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.scrollAreaLayout.sizePolicy().hasHeightForWidth())
        self.scrollAreaLayout.setSizePolicy(sizePolicy6)
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaLayout)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_aviso = QLabel(self.scrollAreaLayout)
        self.label_aviso.setObjectName(u"label_aviso")
        font4 = QFont()
        font4.setFamilies([u"Rockwell"])
        font4.setPointSize(14)
        font4.setBold(False)
        font4.setItalic(True)
        font4.setStrikeOut(False)
        self.label_aviso.setFont(font4)
        self.label_aviso.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_aviso)

        self.scrollArea.setWidget(self.scrollAreaLayout)

        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.stackedWidget_companie.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_6 = QGridLayout(self.page_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.stackedWidget_reference = QStackedWidget(self.page_4)
        self.stackedWidget_reference.setObjectName(u"stackedWidget_reference")
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.horizontalLayout_6 = QHBoxLayout(self.page_6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.table_reference = QTableWidget(self.page_6)
        if (self.table_reference.columnCount() < 3):
            self.table_reference.setColumnCount(3)
        font5 = QFont()
        font5.setFamilies([u"Bahnschrift"])
        font5.setPointSize(14)
        font5.setWeight(QFont.Light)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font5);
        self.table_reference.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font5);
        self.table_reference.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font5);
        self.table_reference.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_reference.setObjectName(u"table_reference")
        self.table_reference.setMinimumSize(QSize(350, 0))
        font6 = QFont()
        font6.setFamilies([u"Bahnschrift"])
        font6.setPointSize(12)
        self.table_reference.setFont(font6)
        self.table_reference.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_reference.setAlternatingRowColors(True)
        self.table_reference.setSortingEnabled(True)
        self.table_reference.horizontalHeader().setDefaultSectionSize(116)
        self.table_reference.verticalHeader().setVisible(False)

        self.horizontalLayout_6.addWidget(self.table_reference)

        self.stackedWidget_reference.addWidget(self.page_6)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.gridLayout_8 = QGridLayout(self.page_7)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.pushButton_6 = QPushButton(self.page_7)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMaximumSize(QSize(23, 23))
        font7 = QFont()
        font7.setFamilies([u"Bahnschrift"])
        font7.setPointSize(19)
        self.pushButton_6.setFont(font7)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout))
        self.pushButton_6.setIcon(icon1)

        self.gridLayout_8.addWidget(self.pushButton_6, 0, 0, 1, 1)

        self.label_5 = QLabel(self.page_7)
        self.label_5.setObjectName(u"label_5")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy7)
        font8 = QFont()
        font8.setFamilies([u"Bahnschrift"])
        font8.setPointSize(12)
        font8.setWeight(QFont.Thin)
        self.label_5.setFont(font8)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_5, 0, 1, 1, 1)

        self.lineEdit_word = QLineEdit(self.page_7)
        self.lineEdit_word.setObjectName(u"lineEdit_word")
        sizePolicy2.setHeightForWidth(self.lineEdit_word.sizePolicy().hasHeightForWidth())
        self.lineEdit_word.setSizePolicy(sizePolicy2)
        self.lineEdit_word.setMaximumSize(QSize(150, 16777215))
        font9 = QFont()
        font9.setFamilies([u"Bahnschrift"])
        font9.setPointSize(16)
        self.lineEdit_word.setFont(font9)

        self.gridLayout_8.addWidget(self.lineEdit_word, 0, 2, 1, 1)

        self.spinBox_value = QSpinBox(self.page_7)
        self.spinBox_value.setObjectName(u"spinBox_value")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.spinBox_value.sizePolicy().hasHeightForWidth())
        self.spinBox_value.setSizePolicy(sizePolicy8)
        self.spinBox_value.setFont(font9)
        self.spinBox_value.setMaximum(99999999)

        self.gridLayout_8.addWidget(self.spinBox_value, 1, 2, 1, 1)

        self.label_6 = QLabel(self.page_7)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font8)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_6, 2, 0, 1, 2)

        self.comboBox_release = QComboBox(self.page_7)
        self.comboBox_release.addItem("")
        self.comboBox_release.addItem("")
        self.comboBox_release.setObjectName(u"comboBox_release")
        sizePolicy2.setHeightForWidth(self.comboBox_release.sizePolicy().hasHeightForWidth())
        self.comboBox_release.setSizePolicy(sizePolicy2)
        self.comboBox_release.setFont(font9)

        self.gridLayout_8.addWidget(self.comboBox_release, 2, 2, 1, 1)

        self.label_7 = QLabel(self.page_7)
        self.label_7.setObjectName(u"label_7")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy9)
        self.label_7.setFont(font8)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_7, 1, 1, 1, 1)

        self.stackedWidget_reference.addWidget(self.page_7)

        self.gridLayout_6.addWidget(self.stackedWidget_reference, 2, 0, 1, 2)

        self.pushButton_exit = QPushButton(self.page_4)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        sizePolicy2.setHeightForWidth(self.pushButton_exit.sizePolicy().hasHeightForWidth())
        self.pushButton_exit.setSizePolicy(sizePolicy2)
        font10 = QFont()
        font10.setFamilies([u"Bahnschrift"])
        font10.setPointSize(12)
        font10.setWeight(QFont.ExtraLight)
        self.pushButton_exit.setFont(font10)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.pushButton_exit.setIcon(icon2)

        self.gridLayout_6.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.page_4)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_current_companie = QLabel(self.frame_7)
        self.label_current_companie.setObjectName(u"label_current_companie")
        font11 = QFont()
        font11.setFamilies([u"Bahnschrift"])
        font11.setPointSize(14)
        font11.setBold(True)
        self.label_current_companie.setFont(font11)
        self.label_current_companie.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_current_companie)

        self.label = QLabel(self.frame_7)
        self.label.setObjectName(u"label")
        self.label.setFont(font6)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.label)


        self.gridLayout_6.addWidget(self.frame_7, 0, 1, 1, 1)

        self.stackedWidget_companie.addWidget(self.page_4)

        self.verticalLayout_5.addWidget(self.stackedWidget_companie)

        self.frame_operations = QFrame(self.groupBox_2)
        self.frame_operations.setObjectName(u"frame_operations")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.frame_operations.sizePolicy().hasHeightForWidth())
        self.frame_operations.setSizePolicy(sizePolicy10)
        self.frame_operations.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_operations.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_operations)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_cancel = QPushButton(self.frame_operations)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMaximumSize(QSize(150, 16777215))
        font12 = QFont()
        font12.setFamilies([u"Bahnschrift"])
        font12.setPointSize(14)
        self.pushButton_cancel.setFont(font12)

        self.horizontalLayout_7.addWidget(self.pushButton_cancel)

        self.pushButton_confirm = QPushButton(self.frame_operations)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMaximumSize(QSize(150, 16777215))
        self.pushButton_confirm.setFont(font12)

        self.horizontalLayout_7.addWidget(self.pushButton_confirm)


        self.verticalLayout_5.addWidget(self.frame_operations)

        self.frame = QFrame(self.groupBox_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add = QPushButton(self.frame)
        self.pushButton_add.setObjectName(u"pushButton_add")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.pushButton_add.setIcon(icon3)
        self.pushButton_add.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_add)

        self.pushButton_remove = QPushButton(self.frame)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.pushButton_remove.setIcon(icon4)
        self.pushButton_remove.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_remove)

        self.pushButton_update = QPushButton(self.frame)
        self.pushButton_update.setObjectName(u"pushButton_update")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailMessageNew))
        self.pushButton_update.setIcon(icon5)
        self.pushButton_update.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pushButton_update)

        self.pushButton_save = QPushButton(self.frame)
        self.pushButton_save.setObjectName(u"pushButton_save")
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.pushButton_save.setIcon(icon6)
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
        sizePolicy10.setHeightForWidth(self.label_extrato.sizePolicy().hasHeightForWidth())
        self.label_extrato.setSizePolicy(sizePolicy10)
        font13 = QFont()
        font13.setFamilies([u"Bahnschrift"])
        font13.setPointSize(18)
        font13.setBold(False)
        self.label_extrato.setFont(font13)
        self.label_extrato.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.label_extrato)

        self.pushButton_upload = QPushButton(self.frame_4)
        self.pushButton_upload.setObjectName(u"pushButton_upload")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.pushButton_upload.sizePolicy().hasHeightForWidth())
        self.pushButton_upload.setSizePolicy(sizePolicy11)
        font14 = QFont()
        font14.setFamilies([u"Lucida Fax"])
        font14.setPointSize(12)
        self.pushButton_upload.setFont(font14)
        icon7 = QIcon()
        icon7.addFile(u"../imgs/upload-icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_upload.setIcon(icon7)
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
        self.pushButton_execute = QPushButton(self.frame_3)
        self.pushButton_execute.setObjectName(u"pushButton_execute")
        sizePolicy2.setHeightForWidth(self.pushButton_execute.sizePolicy().hasHeightForWidth())
        self.pushButton_execute.setSizePolicy(sizePolicy2)
        self.pushButton_execute.setMinimumSize(QSize(175, 50))
        font15 = QFont()
        font15.setFamilies([u"Bahnschrift"])
        font15.setPointSize(14)
        font15.setWeight(QFont.ExtraLight)
        font15.setItalic(True)
        self.pushButton_execute.setFont(font15)
        icon8 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSend))
        self.pushButton_execute.setIcon(icon8)

        self.horizontalLayout_2.addWidget(self.pushButton_execute)


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
        font16 = QFont()
        font16.setFamilies([u"Arial Rounded MT"])
        font16.setPointSize(12)
        font16.setBold(True)
        self.label_carregando.setFont(font16)
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
        self.menubar.setGeometry(QRect(0, 0, 667, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_companie.setCurrentIndex(0)
        self.stackedWidget_reference.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_titulo.setText(QCoreApplication.translate("MainWindow", u"Gerador de Extratos", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Escolha o Banco", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Empresas Dispon\u00edveis", None))
        self.pushButton_reload.setText("")
        self.label_companie_info.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">clique 2x com o bot\u00e3o </span><span style=\" font-size:10pt; font-weight:700; font-style:italic; text-decoration: underline;\">direito</span><span style=\" font-size:10pt; font-style:italic;\"> para selecionar</span></p></body></html>", None))
        self.label_aviso.setText(QCoreApplication.translate("MainWindow", u"Primeiramente, escolha o banco", None))
        ___qtablewidgetitem = self.table_reference.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Palavra", None));
        ___qtablewidgetitem1 = self.table_reference.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Conta", None));
        ___qtablewidgetitem2 = self.table_reference.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Lan\u00e7amento", None));
        self.pushButton_6.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Palavra", None))
        self.lineEdit_word.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Insira aqui", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Lan\u00e7amento", None))
        self.comboBox_release.setItemText(0, QCoreApplication.translate("MainWindow", u"C", None))
        self.comboBox_release.setItemText(1, QCoreApplication.translate("MainWindow", u"D", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Conta", None))
        self.pushButton_exit.setText(QCoreApplication.translate("MainWindow", u"Voltar", None))
        self.label_current_companie.setText(QCoreApplication.translate("MainWindow", u"Empresa", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">clique 2x para selecionar</span></p></body></html>", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("MainWindow", u"Cancelar", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("MainWindow", u"Confirmar", None))
        self.pushButton_add.setText("")
        self.pushButton_remove.setText("")
        self.pushButton_update.setText("")
        self.label_extrato.setText(QCoreApplication.translate("MainWindow", u"Insira o Extrato", None))
        self.pushButton_upload.setText("")
        self.pushButton_execute.setText(QCoreApplication.translate("MainWindow", u" Executar", None))
#if QT_CONFIG(shortcut)
        self.pushButton_execute.setShortcut(QCoreApplication.translate("MainWindow", u"Enter", None))
#endif // QT_CONFIG(shortcut)
        self.label_carregando.setText(QCoreApplication.translate("MainWindow", u"Carregando...", None))
        self.label_load.setText("")
    # retranslateUi

