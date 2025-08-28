# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1044, 584)
        MainWindow.setStyleSheet(u"background-color: #3a404d;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.icon_only_widgect = QWidget(self.centralwidget)
        self.icon_only_widgect.setObjectName(u"icon_only_widgect")
        self.icon_only_widgect.setStyleSheet(u"QWidget{\n"
"background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton{\n"
"	color: white;\n"
"	height: 30px;\n"
"	border: none;\n"
"	border-radius: 10px;\n"
"}\n"
"QPushButton:checked{\n"
"	background-color: #3a404d;\n"
"	font-weight: bold;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.icon_only_widgect)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.icon_only_widgect)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label.setPixmap(QPixmap(u":/icon/logo.ico"))
        self.label.setScaledContents(False)

        self.horizontalLayout_3.addWidget(self.label)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 16, -1, -1)
        self.home_1 = QPushButton(self.icon_only_widgect)
        self.home_1.setObjectName(u"home_1")
        icon = QIcon()
        icon.addFile(u":/icon/house-48 (3).ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.home_1.setIcon(icon)
        self.home_1.setCheckable(True)
        self.home_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.home_1)

        self.pet_1 = QPushButton(self.icon_only_widgect)
        self.pet_1.setObjectName(u"pet_1")
        icon1 = QIcon()
        icon1.addFile(u":/icon/rabbit-48.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pet_1.setIcon(icon1)
        self.pet_1.setCheckable(True)
        self.pet_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.pet_1)

        self.startdetection_1 = QPushButton(self.icon_only_widgect)
        self.startdetection_1.setObjectName(u"startdetection_1")
        icon2 = QIcon()
        icon2.addFile(u":/icon/slr-camera-48 (1).ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.startdetection_1.setIcon(icon2)
        self.startdetection_1.setCheckable(True)
        self.startdetection_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.startdetection_1)

        self.history_1 = QPushButton(self.icon_only_widgect)
        self.history_1.setObjectName(u"history_1")
        icon3 = QIcon()
        icon3.addFile(u":/icon/book-2-48.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.history_1.setIcon(icon3)
        self.history_1.setCheckable(True)
        self.history_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.history_1)

        self.settings_1 = QPushButton(self.icon_only_widgect)
        self.settings_1.setObjectName(u"settings_1")
        icon4 = QIcon()
        icon4.addFile(u":/icon/settings-4-48 (1).ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings_1.setIcon(icon4)
        self.settings_1.setCheckable(True)
        self.settings_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.settings_1)

        self.profile_1 = QPushButton(self.icon_only_widgect)
        self.profile_1.setObjectName(u"profile_1")
        icon5 = QIcon()
        icon5.addFile(u":/icon/group-48.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.profile_1.setIcon(icon5)
        self.profile_1.setCheckable(True)
        self.profile_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.profile_1)

        self.help_1 = QPushButton(self.icon_only_widgect)
        self.help_1.setObjectName(u"help_1")
        icon6 = QIcon()
        icon6.addFile(u":/icon/help-48 (1).ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.help_1.setIcon(icon6)
        self.help_1.setCheckable(True)
        self.help_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.help_1)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 141, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.signout_1 = QPushButton(self.icon_only_widgect)
        self.signout_1.setObjectName(u"signout_1")
        icon7 = QIcon()
        icon7.addFile(u":/icon/logout-48.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.signout_1.setIcon(icon7)
        self.signout_1.setCheckable(True)

        self.verticalLayout_3.addWidget(self.signout_1)


        self.gridLayout.addWidget(self.icon_only_widgect, 0, 0, 1, 1)

        self.icon_name_widgect = QWidget(self.centralwidget)
        self.icon_name_widgect.setObjectName(u"icon_name_widgect")
        self.icon_name_widgect.setStyleSheet(u"QWidget{\n"
"background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton{\n"
"	color: white;\n"
"	text-align: left;\n"
"	height: 30px;\n"
"	border: none;\n"
"	padding-left: 10px;\n"
"	border-top-left-radius: 10px;\n"
"	border-bottom-left-radius: 10px;\n"
"}\n"
"QPushButton:checked{\n"
"	background-color: #3a404d;\n"
"	font-weight: bold;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.icon_name_widgect)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 14, 10, -1)
        self.label_2 = QLabel(self.icon_name_widgect)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.icon_name_widgect)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.label_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 30, -1, -1)
        self.home_2 = QPushButton(self.icon_name_widgect)
        self.home_2.setObjectName(u"home_2")
        self.home_2.setIcon(icon)
        self.home_2.setCheckable(True)
        self.home_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.home_2)

        self.pet_2 = QPushButton(self.icon_name_widgect)
        self.pet_2.setObjectName(u"pet_2")
        self.pet_2.setIcon(icon1)
        self.pet_2.setCheckable(True)
        self.pet_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.pet_2)

        self.startdetection_2 = QPushButton(self.icon_name_widgect)
        self.startdetection_2.setObjectName(u"startdetection_2")
        self.startdetection_2.setIcon(icon2)
        self.startdetection_2.setCheckable(True)
        self.startdetection_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.startdetection_2)

        self.history_2 = QPushButton(self.icon_name_widgect)
        self.history_2.setObjectName(u"history_2")
        self.history_2.setIcon(icon3)
        self.history_2.setCheckable(True)
        self.history_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.history_2)

        self.settings_2 = QPushButton(self.icon_name_widgect)
        self.settings_2.setObjectName(u"settings_2")
        self.settings_2.setIcon(icon4)
        self.settings_2.setCheckable(True)
        self.settings_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.settings_2)

        self.profile_2 = QPushButton(self.icon_name_widgect)
        self.profile_2.setObjectName(u"profile_2")
        self.profile_2.setIcon(icon5)
        self.profile_2.setCheckable(True)
        self.profile_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.profile_2)

        self.help_2 = QPushButton(self.icon_name_widgect)
        self.help_2.setObjectName(u"help_2")
        self.help_2.setIcon(icon6)
        self.help_2.setCheckable(True)
        self.help_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.help_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 141, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.signout_2 = QPushButton(self.icon_name_widgect)
        self.signout_2.setObjectName(u"signout_2")
        self.signout_2.setIcon(icon7)
        self.signout_2.setCheckable(True)

        self.verticalLayout_4.addWidget(self.signout_2)


        self.gridLayout.addWidget(self.icon_name_widgect, 0, 1, 1, 1)

        self.main_manu = QWidget(self.centralwidget)
        self.main_manu.setObjectName(u"main_manu")
        self.main_manu.setStyleSheet(u"background-color: #3a404d;")
        self.verticalLayout_5 = QVBoxLayout(self.main_manu)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(11, -1, -1, -1)
        self.header_widgect = QWidget(self.main_manu)
        self.header_widgect.setObjectName(u"header_widgect")
        self.horizontalLayout_4 = QHBoxLayout(self.header_widgect)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.menu = QPushButton(self.header_widgect)
        self.menu.setObjectName(u"menu")
        self.menu.setStyleSheet(u"border: none;\n"
"")
        icon8 = QIcon()
        icon8.addFile(u":/icon/menu-4-48.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu.setIcon(icon8)
        self.menu.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.menu)

        self.horizontalSpacer = QSpacerItem(214, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.header_widgect)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #8f8f91;\n"
"    border-radius: 6px;\n"
"    padding: 0 8px;\n"
"	height: 25px;\n"
"	width: 200px;\n"
"	background-color: rgb(255, 255, 255);\n"
"	color: #3a404d;\n"
"}")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton_18 = QPushButton(self.header_widgect)
        self.pushButton_18.setObjectName(u"pushButton_18")
        self.pushButton_18.setStyleSheet(u"QPushButton {\n"
"    border-radius: 4px;         /* Rounded corners */\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u":/icon/search-12-48 (1).ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_18.setIcon(icon9)

        self.horizontalLayout.addWidget(self.pushButton_18)


        self.horizontalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalSpacer_2 = QSpacerItem(214, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.profile_3 = QPushButton(self.header_widgect)
        self.profile_3.setObjectName(u"profile_3")
        self.profile_3.setStyleSheet(u"border: none;")
        icon10 = QIcon()
        icon10.addFile(u":/icon/change-user-48.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.profile_3.setIcon(icon10)

        self.horizontalLayout_4.addWidget(self.profile_3)


        self.verticalLayout_5.addWidget(self.header_widgect)

        self.stackedWidget = QStackedWidget(self.main_manu)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background-color: rgb(86, 95, 115);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius: 10px;\n"
"border-bottom-left-radius: 10px;\n"
"border-bottom-right-radius: 10px;")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.label_4 = QLabel(self.home_page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(240, 230, 321, 20))
        font2 = QFont()
        font2.setPointSize(20)
        self.label_4.setFont(font2)
        self.stackedWidget.addWidget(self.home_page)
        self.pet_page = QWidget()
        self.pet_page.setObjectName(u"pet_page")
        self.label_5 = QLabel(self.pet_page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(250, 230, 321, 20))
        self.label_5.setFont(font2)
        self.stackedWidget.addWidget(self.pet_page)
        self.start_detection_page = QWidget()
        self.start_detection_page.setObjectName(u"start_detection_page")
        self.label_6 = QLabel(self.start_detection_page)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(230, 230, 321, 20))
        self.label_6.setFont(font2)
        self.stackedWidget.addWidget(self.start_detection_page)
        self.history_page = QWidget()
        self.history_page.setObjectName(u"history_page")
        self.label_7 = QLabel(self.history_page)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(290, 250, 321, 20))
        self.label_7.setFont(font2)
        self.stackedWidget.addWidget(self.history_page)
        self.settings_page = QWidget()
        self.settings_page.setObjectName(u"settings_page")
        self.label_8 = QLabel(self.settings_page)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(260, 250, 321, 20))
        self.label_8.setFont(font2)
        self.stackedWidget.addWidget(self.settings_page)
        self.profile_page = QWidget()
        self.profile_page.setObjectName(u"profile_page")
        self.label_9 = QLabel(self.profile_page)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(240, 230, 321, 20))
        self.label_9.setFont(font2)
        self.stackedWidget.addWidget(self.profile_page)
        self.help_page = QWidget()
        self.help_page.setObjectName(u"help_page")
        self.label_10 = QLabel(self.help_page)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(160, 20, 571, 31))
        font3 = QFont()
        font3.setPointSize(15)
        font3.setBold(True)
        font3.setUnderline(False)
        self.label_10.setFont(font3)
        self.label_10.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.plainTextEdit = QPlainTextEdit(self.help_page)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(73, 120, 671, 241))
        self.plainTextEdit.setStyleSheet(u"color: white;\n"
"font-size: 20px;\n"
"text-align: center;\n"
"border: none;\n"
"")
        self.pushButton = QPushButton(self.help_page)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(200, 420, 171, 28))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(33, 37, 43);\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #0056b3;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #004080;\n"
"    padding-top: 10px;\n"
"    padding-left: 10px;\n"
"}\n"
"")
        self.pushButton_2 = QPushButton(self.help_page)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(430, 420, 171, 28))
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(33, 37, 43);\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #0056b3;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #004080;\n"
"    padding-top: 10px;\n"
"    padding-left: 10px;\n"
"}\n"
"")
        self.stackedWidget.addWidget(self.help_page)

        self.verticalLayout_5.addWidget(self.stackedWidget)


        self.gridLayout.addWidget(self.main_manu, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.menu.toggled.connect(self.icon_only_widgect.setHidden)
        self.menu.toggled.connect(self.icon_name_widgect.setVisible)
        self.help_1.toggled.connect(self.help_2.setChecked)
        self.profile_1.toggled.connect(self.profile_2.setChecked)
        self.settings_1.toggled.connect(self.settings_2.setChecked)
        self.history_1.toggled.connect(self.history_2.setChecked)
        self.startdetection_1.toggled.connect(self.startdetection_2.setChecked)
        self.pet_1.toggled.connect(self.pet_2.setChecked)
        self.home_1.toggled.connect(self.home_2.setChecked)
        self.home_2.toggled.connect(self.home_1.setChecked)
        self.pet_2.toggled.connect(self.pet_1.setChecked)
        self.startdetection_2.toggled.connect(self.startdetection_1.setChecked)
        self.history_2.toggled.connect(self.history_1.setChecked)
        self.settings_2.toggled.connect(self.settings_1.setChecked)
        self.profile_2.toggled.connect(self.profile_1.setChecked)
        self.help_2.toggled.connect(self.help_1.setChecked)
        self.signout_1.toggled.connect(MainWindow.close)
        self.signout_2.toggled.connect(MainWindow.close)

        self.stackedWidget.setCurrentIndex(6)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"M", None))
        self.home_1.setText("")
        self.pet_1.setText("")
        self.startdetection_1.setText("")
        self.history_1.setText("")
        self.settings_1.setText("")
        self.profile_1.setText("")
        self.help_1.setText("")
        self.signout_1.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MoodMate", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"SideBar", None))
        self.home_2.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.pet_2.setText(QCoreApplication.translate("MainWindow", u"Pet", None))
        self.startdetection_2.setText(QCoreApplication.translate("MainWindow", u"Start Detection", None))
        self.history_2.setText(QCoreApplication.translate("MainWindow", u"History", None))
        self.settings_2.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.profile_2.setText(QCoreApplication.translate("MainWindow", u"Profile", None))
        self.help_2.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.signout_2.setText(QCoreApplication.translate("MainWindow", u"Sign Out", None))
        self.menu.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search..", None))
        self.pushButton_18.setText("")
        self.profile_3.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Home Page", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Pet Page", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Start Detection Page", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"History Page", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Settings Page", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Profile Page", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Help / About Page \u2013 Info and Contact", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("MainWindow", u"MoodMate is your emotional companion designed to detect and respond to your feelings in real-time.\n"
"\n"
"Version: 1.0\n"
"Developers: Nexora (Group 01 \u2013 SLTC) \n"
"Contact Support: moodmate@yourmail.com \n"
"", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Open Documentation", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Send Feedback", None))
    # retranslateUi

