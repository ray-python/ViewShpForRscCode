# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import functools

class fontEditDialog:
    def __init__(self,fsc=False):
        self.stat = False
        self.dial = QDialog()
        boxlayout = QHBoxLayout()
        butlayout = QHBoxLayout()
        hlayout = QVBoxLayout()
        fcb = QFontComboBox()
        ccb = QComboBox()
        sdsb = QDoubleSpinBox()
        okbtn = QPushButton("Ok")
        rejbtn = QPushButton("Cancel")
        okbtn.clicked.connect(functools.partial(self.closeDial, sdsb, fcb,ccb))
        rejbtn.clicked.connect(functools.partial(self.closeDial, False, False))
        m = fcb.model()
        m.setStringList([u'Aa1', u'A431', u'Bm431', u'Bo2', u'Ch122', u'Ch131',
                         u'Ch132', u'D231', u'D431', u'D432', u'Do431',
                         u'P112', u'P131', u'P151', u'P152',
                         u'T132', u'T1_131', u'T2_131'])
        self.createColorCombox(ccb)
        sdsb.setDecimals(1)
        boxlayout.addWidget(fcb)
        boxlayout.addWidget(sdsb)
        boxlayout.addWidget(ccb)
        butlayout.addWidget(okbtn)
        butlayout.addWidget(rejbtn)
        hlayout.addLayout(boxlayout)
        hlayout.addLayout(butlayout)
        self.dial.setLayout(hlayout)
        if fsc:
            self.setcomboxtext(fsc,sdsb,fcb,ccb)
    def setcomboxtext(self, fsc, sdsb, *comboxes):
        for value in fsc:
            for cb in comboxes:
                i = cb.findText(value)
                if i != -1:
                    cb.setCurrentIndex(i)
            try:
                v = float(value)
                sdsb.setValue(v)
            except:
                pass
    def showDial(self):
        self.dial.exec_()
        if self.stat:
            return self.stat
    def closeDial(self, sdsb, *comboxes):
        if sdsb and comboxes:
            self.stat = []
            for c in comboxes:
                if c:
                    self.stat.append(c.currentText())
            self.stat.insert(1,str(sdsb.value()*4))
        self.dial.close()
    def fillcombox(self,color, combox):
        globals()[color] = QPixmap(15, 15)
        globals()[color].fill(QColor(QColor(color)))
        icon = QIcon(globals()[color])
        combox.addItem(icon, color)
    def createColorCombox(self,combox):
        colornames = ['yellow','red', 'black','blue', 'green', 'magenta']
        for color in colornames:
            self.fillcombox(color, combox)