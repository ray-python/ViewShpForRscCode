from qgis.core import *
from qgis.gui import *

def getValue(ok, font=False, size=False, color=False):
    ok = str(ok)
    if font:
        return okdict[ok][1][0]
    if size:
        return okdict[ok][1][1]
    if color:
        return okdict[ok][1][2]
@qgsfunction(args="auto", group='Custom')
def fontProperty(ok, f, s, c, feature, parent):
    return getValue(ok, f, s, c)

class LabelProperties:
    def __init__(self, dict):
        okdict = dict
        global okdict
    def makeLabels(self,layer):
        layer.setCustomProperty("labeling", "pal")
        layer.setCustomProperty("labeling/enabled", "true")
        layer.setCustomProperty("labeling/fieldName", 'ObjectText')
        layer.setCustomProperty("labeling/placement", QgsPalLayerSettings.Curved)
        layer.setCustomProperty("labeling/textColorR", "255")
        layer.setCustomProperty("labeling/textColorG", "0")
        layer.setCustomProperty("labeling/textColorB", "176")
        layer.setCustomProperty("labeling/dataDefined/Family", u'1~~1~~fontProperty("ObjectKey",1,0,0)~~')
        layer.setCustomProperty("labeling/dataDefined/Size", u'1~~1~~fontProperty("ObjectKey",0,1,0)~~')
        layer.setCustomProperty("labeling/dataDefined/Color", u'1~~1~~fontProperty("ObjectKey",0,0,1)~~')