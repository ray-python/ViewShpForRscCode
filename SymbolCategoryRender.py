# -*- coding: utf-8 -*-
from qgis.core import*
from qgis.gui import*


class SymbolCategoryRenderClass:
    def __init__(self, okdict):
        self.codename = okdict
        #print self.codename

    def CategoryRender(self,style,lyr):
        fni = lyr.fieldNameIndex('ObjectKey')
        unique_values = lyr.uniqueValues(fni)
        categories = []
        for unique_value in unique_values:
            uv = str(unique_value)
            if uv not in self.codename:
                self.codename[uv] = ['None','None']
            sym = self.codename[uv][1]
            if sym == 'None':
                if 'L' in uv:
                    sym = 'NoneStyleLine'
                if 'P' in uv:
                    sym = 'NoneStyleMark'
                if 'S' in uv:
                    sym = 'NoneStylePoly'
                if 'V' in uv:
                    sym = 'NoneStyleLine'
            if 'T' in uv:
                sym = 'labeLine'
            symbol = style.symbol(sym)
            if symbol:
                category = QgsRendererCategoryV2(unique_value, symbol, self.codename[uv][0])
                categories.append(category)
            else:
                pass
        renderer = QgsCategorizedSymbolRendererV2('ObjectKey', categories)
        if renderer is not None:
            lyr.setRendererV2(renderer)