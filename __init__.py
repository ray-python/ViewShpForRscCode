# -*- coding: utf-8 -*-
"""
/***************************************************************************
ViewShpForRscCode
                                 A QGIS plugin
 Styling Map Render
                             -------------------
        begin                : 2017-05-09
        copyright            : (C) 2017 by Author
        email                : email@mail.ru
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MapStyling class from file MapStyling.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ViewShpForRscCode import ViewShpForRscCode
    return ViewShpForRscCode(iface)
