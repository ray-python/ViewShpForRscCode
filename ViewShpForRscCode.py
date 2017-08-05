# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ViewShpForRscCode
                                 A QGIS plugin
 Styling Map Render
                              -------------------
        begin                : 2017-05-09
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Author
        email                : email@mail.ru
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from PyQt4 import QtGui, uic, QtCore
from ViewShpForRscCode_dialog import ViewShpForRscCodeDialog, EditRenderDialog
from SymbolCategoryRender import SymbolCategoryRenderClass
#from LabelRender import LabelRenderClass
from UnicodeWriter import UnicodeWriter
from LabelProperties import LabelProperties
from fontEdit import fontEditDialog
import os
from qgis.core import*
from qgis.gui import*
import glob
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
import shutil
import csv
import functools

class ViewShpForRscCode:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        dir = os.path.dirname(__file__)
        self.plugin_dir = dir.decode('cp1251')
        self.labProp = None
        self.fed = None
        self.scrc = None
        self.codename = None
        self.model = None
        self.okdict = {}
        self.root = QgsProject.instance().layerTreeRoot()
        self.style = QgsStyleV2().defaultStyle()
        self.dlg = ViewShpForRscCodeDialog()
        self.editRend = EditRenderDialog()
        self.editRend.listWgt.doubleClicked.connect(self.editSymbol)
        self.editRend.closeButton.clicked.connect(self.closeEditRend)
        self.editRend.csvExpButton.clicked.connect(self.expCSV)
        self.editRend.xmlExpButton.clicked.connect(self.expXML)
        self.editRend.saveButton.clicked.connect(functools.partial(self.expCSV, True))
        self.editRend.delButton.clicked.connect(self.removeCodeItem)
        self.editRend.addButton.clicked.connect(self.addCodeItem)
        self.dlg.runButton.clicked.connect(self.setMapStyle)
        self.dlg.closeButton.clicked.connect(self.closeDial)
        self.dlg.importXmlButton.clicked.connect(self.importXML)
        self.dlg.editRenderButton.clicked.connect(self.editRender)
        self.dlg.delTabButton.clicked.connect(self.removeTab)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MapStyling_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ViewShpForRscCodePlugin')
        self.toolbar = self.iface.addToolBar(u'MapStyling')
        self.toolbar.setObjectName(u'MapStyling')

    def tr(self, message):
        return QCoreApplication.translate('MapStyling', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        self.actions.append(action)
        return action
    def GetModelForCombobox(self, list):
        model = QtGui.QStandardItemModel(1, 1)
        n = 0
        for l in list:
            item_str = l.rpartition('\\')[2]
            item = QtGui.QStandardItem(item_str)
            model.setItem(n, 0, item)
            n = n + 1
        return model 
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ViewShpForRscCode/icon.png'
        self.add_action(
            icon_path,
            text=self.tr('ViewShpForRscCode'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&MViewShpForRscCodePlugin'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        QgsExpression.unregisterFunction("fontProperty")

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        #self.dlg.show()
        # Run the dialog event loop
        self.fillCombos()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
    def fillCombos(self):
        xml = glob.glob(self.plugin_dir + '/svg/*.xml')
        tab = glob.glob(self.plugin_dir + '/tab/*.csv')
        self.dlg.scaleComboBox.setModel(self.GetModelForCombobox(xml))
        self.dlg.tabComboBox.setModel(self.GetModelForCombobox(tab))
    def reorderLayers(self, layer, node):
        lyr = self.root.findLayer(layer.id())
        lyrClone = lyr.clone()
        parent = lyr.parent()
        parent.insertChildNode(node, lyrClone)
        parent.removeChildNode(lyr)
    def setMapStyle(self):
        layers = self.iface.legendInterface().layers()
        self.scrc = SymbolCategoryRenderClass(self.makeokdict(self.getTabs(csv=True)))
        self.labProp = LabelProperties(self.okdict)
        for layer in layers:
            layerType = layer.type()
            if layerType == QgsMapLayer.VectorLayer:
                node = len(layers)
                if layer.name() == u'LAYER3-polygon':
                    self.reorderLayers(layer, node)
                if layer.name() == u'LAYER7-polygon':
                    self.reorderLayers(layer, node-1)
                if layer.name() == u'LAYER12-polygon':
                    self.reorderLayers(layer, node-2)
                if layer.name() == u'LAYER19-polygon':
                    self.reorderLayers(layer, node-3)
                if layer.name() == u'LAYER17-label':
                    self.labProp.makeLabels(layer)
                self.scrc.CategoryRender(self.style,layer)
            layer.triggerRepaint()
    def getTabs(self, csv=None, lbl=None):
        if csv:
            tabName = self.dlg.tabComboBox.currentText()
            csv_path = os.path.join(
                self.plugin_dir, 'tab/' + tabName)
        return csv_path
    def makeokdict(self,csv_path):
        with open(csv_path) as f:
            reader = csv.reader(f, delimiter =';')
            for row in reader:
                if 'T' in row[0]:
                    self.okdict[row[0]] = [row[1].decode('utf-8'), row[2].decode('utf-8').split(',')]
                else:
                    self.okdict[row[0]] = [row[1].decode('utf-8'),row[2].decode('utf-8')]
        return self.okdict
    def importXML(self):
        srcStyle = QgsStyleV2()
        dstStyle = self.style
        symLib = self.dlg.scaleComboBox.currentText()
        svg_dst = QgsApplication.svgPaths()[0]
        spath = self.plugin_dir + '/svg/'
        copylist = []
        if not os.path.isfile(spath):
            for path, dirs, filenames in os.walk(spath):
                for directory in dirs:
                    dir_path = os.path.join(svg_dst, directory)
                    if not os.path.exists(dir_path):
                        os.makedirs(os.path.join(dir_path))
                for sfile in filenames:
                    s_file = os.path.join(path, sfile)
                    d_file = os.path.join(path.replace(spath, svg_dst), sfile)
                    copylist.append([s_file, d_file])
            for c in copylist:
                shutil.copy(c[0], c[1])
        xml_path = spath + symLib
        srcStyle.importXML(xml_path)
        groupName = symLib.replace(".xml", "")
        if groupName not in dstStyle.groupNames():
            dstStyle.addGroup(groupName)
        groupid = dstStyle.groupId(groupName)
        for sym in srcStyle.symbolNames():
            symbol = srcStyle.symbol(sym)
            dstStyle.addSymbol(sym, symbol)
            dstStyle.saveSymbol(sym, symbol, groupid, [])
        QtGui.QMessageBox.information(QWidget(), u'Информация',
                                      u'Импорт завершен', QtGui.QMessageBox.Ok
                                      )
        return
    def editRender(self):
        tab = self.dlg.tabComboBox.currentText()
        self.editRend.listWgt.setIconSize(QSize(32, 32))
        self.editRend.listWgt.setEditTriggers(QtGui.QAbstractItemView.SelectedClicked)
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.model.setHorizontalHeaderItem(0, QStandardItem(u'Код'))
        self.model.setHorizontalHeaderItem(1, QStandardItem(u'Название'))
        self.model.setHorizontalHeaderItem(2, QStandardItem(u'Знак'))
        self.editRend.listWgt.setModel(self.model)
        self.editRend.listWgt.setSelectionBehavior(QTableView.SelectRows)
        self.codename = {}
        with open(self.plugin_dir + '/tab/' + tab) as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                itemCode = QStandardItem(row[0])
                itemName = QStandardItem(row[1].decode('utf-8'))
                symName = row[2].decode('utf-8')
                if symName == 'None':
                    if 'L' in itemCode.text():
                        symName = 'NoneStyleLine'
                    if 'P' in itemCode.text():
                        symName = 'NoneStyleMark'
                    if 'S' in itemCode.text():
                        symName = 'NoneStylePoly'
                    if 'V' in itemCode.text():
                        symName = 'NoneStyleLine'
                itemSymb = QStandardItem(symName)
                symbol = self.style.symbol(symName)
                if symbol:
                    itemSymb = QStandardItem(symName)
                    icon = QgsSymbolLayerV2Utils.symbolPreviewIcon(symbol, self.editRend.listWgt.iconSize())
                    itemSymb.setIcon(icon)
                self.model.appendRow([itemCode, itemName, itemSymb])
                self.codename[itemCode.text()] = symName
        self.editRend.listWgt.resizeRowsToContents()
        self.editRend.listWgt.setColumnWidth(2, 125)
        self.editRend.listWgt.setColumnWidth(1, 250)
        self.editRend.exec_()
    def editSymbol(self):
        row = self.editRend.listWgt.selectionModel().currentIndex().row()
        code = self.model.item(row, 0).text()
        name = self.model.item(row, 2).text()
        if name == 'None':
            t = QInputDialog.getItem(QWidget(), u'Создание условного знака',
                                     u'Укажите тип объекта',
                                     [u'Точка', u'Линия', u'Полигон', u'Текст'],editable = False)
            if t[1]:
                if t[0] == u'Точка':
                    name = 'NoneStyleMark'
                if t[0] == u'Линия':
                    name = 'NoneStyleLine'
                if t[0] == u'Полигон':
                    name = 'NoneStylePoly'
                if t[0] == u'Текст':
                    name = None
            else:
                return
        if 'T' in code:
            fontProps = self.fontDialog(name)
            if fontProps:
                item = QStandardItem(','.join(fontProps))
                self.model.setItem(row, 2, item)
            return
        symbol = self.style.symbol(name)
        if not symbol:
            return
        d = QgsSymbolV2SelectorDialog(symbol, self.style, None)
        if d.exec_() == 0:
            return
        if 'None' in name:
            name = ''
        newName = QInputDialog.getText(QWidget(),u"Имя условного знака", u"Введите имя условного знака:",text=name)
        if newName[1]:
            name = newName[0]
        if not newName[1]:
            return
        self.style.addSymbol(name, symbol, True)
        itemSymb = QStandardItem(name)
        icon = QgsSymbolLayerV2Utils.symbolPreviewIcon(symbol, self.editRend.listWgt.iconSize())
        itemSymb.setIcon(icon)
        self.model.setItem(row, 2, itemSymb)
    def fontDialog(self,name=False):
        fsc = None
        if name:
            fsc = name.split(',')
        self.fed = fontEditDialog(fsc)
        return self.fed.showDial()
    def removeTab(self):
        tab = self.dlg.tabComboBox.currentText()
        if tab == 'codeNameTab_100k.csv':
            QtGui.QMessageBox.information(QWidget(), u'Информация',
                                          u'Невозможно удалить этот файл', QtGui.QMessageBox.Ok
                                          )
            return
        tpath = self.plugin_dir + '/tab/' + tab
        os.remove(tpath)
        self.fillCombos()
    def closeDial(self):
        self.dlg.close()
    def closeEditRend(self):
        self.editRend.close()
        self.fillCombos()
    def expXML(self):
        QgsStyleV2ManagerDialog(self.style).exportItems()
    def expCSV(self,save=False):
        if not save:
            nameInput = QInputDialog.getText(QWidget(), u"Название таблицы", u"Введите название таблицы")
            if nameInput[1]:
                name = nameInput[0]
            else:
                return
        if save:
            name = self.dlg.tabComboBox.currentText().replace('.csv','')
        with open(self.plugin_dir + '/tab/' + name + '.csv', 'wb') as fout:
            writer = UnicodeWriter(fout, delimiter=';')
            for r in range(self.model.rowCount()):
                itemCode = self.model.item(r, 0).text()
                itemName = self.model.item(r, 1).text()
                itemSymb = self.model.item(r, 2).text()
                writer.writerow([itemCode, itemName, itemSymb])
    def removeCodeItem(self):
        indexList = []
        for r in self.editRend.listWgt.selectionModel().selectedRows():
            row = r.row()
            indexList.append(row)
        for i in indexList[::-1]:
            self.model.removeRows(i, 1)
    def addCodeItem(self):
        itemCode = QStandardItem('None')
        itemName = QStandardItem('None')
        itemSymb = QStandardItem('None')
        itemList =[itemCode,itemName,itemSymb]
        selection = self.editRend.listWgt.selectionModel().selectedRows()
        if selection:
            self.model.insertRow(selection[-1::][0].row()+1,itemList)
        else:
            self.model.appendRow(itemList)