# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget)

from qfluentwidgets import (LineEdit, PrimaryPushButton, PushButton)

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        if not MainForm.objectName():
            MainForm.setObjectName(u"MainForm")
        MainForm.resize(377, 405)
        self.verticalLayout = QVBoxLayout(MainForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tmpButton = PushButton(MainForm)
        self.tmpButton.setObjectName(u"tmpButton")

        self.horizontalLayout.addWidget(self.tmpButton)

        self.lineEdit = LineEdit(MainForm)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.sofpButton = PushButton(MainForm)
        self.sofpButton.setObjectName(u"sofpButton")

        self.horizontalLayout_2.addWidget(self.sofpButton)

        self.lineEdit_2 = LineEdit(MainForm)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_2.addWidget(self.lineEdit_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.profitButton = PushButton(MainForm)
        self.profitButton.setObjectName(u"profitButton")

        self.horizontalLayout_3.addWidget(self.profitButton)

        self.lineEdit_3 = LineEdit(MainForm)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_3.addWidget(self.lineEdit_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.flowButton = PushButton(MainForm)
        self.flowButton.setObjectName(u"flowButton")

        self.horizontalLayout_4.addWidget(self.flowButton)

        self.lineEdit_4 = LineEdit(MainForm)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout_4.addWidget(self.lineEdit_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.startButton = PrimaryPushButton(MainForm)
        self.startButton.setObjectName(u"startButton")

        self.verticalLayout.addWidget(self.startButton)


        self.retranslateUi(MainForm)

        QMetaObject.connectSlotsByName(MainForm)
    # setupUi

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QCoreApplication.translate("MainForm", u"Form", None))
        self.tmpButton.setText(QCoreApplication.translate("MainForm", u"\u8bf7\u9009\u62e9\u6a21\u677f\u6587\u4ef6", None))
        self.sofpButton.setText(QCoreApplication.translate("MainForm", u"\u8bf7\u9009\u62e9\u8d44\u4ea7\u8d1f\u8f7d\u8868", None))
        self.profitButton.setText(QCoreApplication.translate("MainForm", u"\u8bf7\u9009\u62e9\u8d44\u5229\u6da6\u8868", None))
        self.flowButton.setText(QCoreApplication.translate("MainForm", u"\u8bf7\u9009\u62e9\u6d41\u91cf\u8868", None))
        self.startButton.setText(QCoreApplication.translate("MainForm", u"\u5f00\u59cb\u751f\u6210", None))
    # retranslateUi

