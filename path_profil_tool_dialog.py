# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PathProfilerDialog
                                 A QGIS plugin
 Makes a profile line from a line geometry
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-04-25
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Kalundborg Kommune
        email                : andj@kalundborg.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import processing
from qgis.core import (
    QgsRasterLayer, QgsVectorLayer, QgsRectangle, QgsProject, QgsProcessingFeedback, 
    QgsMapLayerProxyModel, QgsField, QgsFeature, QgsGeometry, QgsPointXY, QgsSymbol
)
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtWidgets import QProgressDialog

from .plot_dialog import PlotDialog


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'path_profil_tool_dialog_base.ui'))


class PathProfilToolDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(PathProfilToolDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        self.setupUi(self)
        
        # Set the dialog window icon
        icon_path = ':/plugins/path_profil_tool/icon.png'
        self.setWindowIcon(QIcon(icon_path))
        
        # Connect the "analyse_button" click signal to the method
        self.analyse_button.clicked.connect(self.analyseButtonClicked)

        # Filter layers to line layers only
        self.map_layers.setFilters(QgsMapLayerProxyModel.LineLayer)
        
        self.wcs_layer = None 

        # Load the token if it exists
        self.loadToken()
                       
    def analyseButtonClicked(self):
        selected_layer = self.map_layers.currentLayer()
        buffer_distance = 0.000000001

        # Initialize the progress dialog
        self.progress_dialog = QProgressDialog("Processing...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle("Progress")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setValue(0)
        
        # Step 1: Create buffer
        buffer_layer = self.createBuffer(selected_layer, buffer_distance)
        if buffer_layer is None:
            print("Buffer creation failed.")
            return
        self.progress_dialog.setValue(25)
        
        smaller_extent = buffer_layer.extent()

        # Step 2: Load the WCS layer
        wcs_layer = self.loadWCSLayer(smaller_extent)
        if wcs_layer is None or not wcs_layer.isValid():
            print("WCS layer failed to load.")
            return
        self.progress_dialog.setValue(50)

        # Step 3: Sample elevation
        self.sampleElevationAlongPath(wcs_layer)
        self.progress_dialog.setValue(75)

        # Save the token if the checkbox is checked
        if self.save_token_checkbox.isChecked():
            self.saveToken()
        
        self.progress_dialog.setValue(100)
        self.progress_dialog.close()

        print("Analysis complete.")

    def createBuffer(self, selected_layer, buffer_distance):
        try:
            if self.selected_checkbox.isChecked():
                selected_features = selected_layer.selectedFeatures()
                if not selected_features:
                    print("No features selected.")
                    return None

                # Create a temporary layer with the selected features
                temp_layer = QgsVectorLayer("LineString?crs={}".format(selected_layer.crs().authid()), "Selected Features", "memory")
                temp_provider = temp_layer.dataProvider()
                temp_provider.addFeatures(selected_features)
                input_layer = temp_layer
            else:
                input_layer = selected_layer

            buffer_result = processing.run("native:buffer", {
                'INPUT': input_layer,
                'DISTANCE': buffer_distance,
                'SEGMENTS': 5,
                'END_CAP_STYLE': 0,
                'JOIN_STYLE': 0,
                'MITER_LIMIT': 2,
                'DISSOLVE': False,
                'OUTPUT': 'TEMPORARY_OUTPUT'
            })
            buffer_layer = buffer_result['OUTPUT']
            return buffer_layer
        except Exception as e:
            print(f"Error creating buffer: {e}")
            return None

    def loadWCSLayer(self, extent):
        # Retrieve the token from the QLineEdit widget
        token = self.token_edit.text().strip()

        # Ensure a token has been provided
        if not token:
            print("No token provided in the input field.")
            return None

        # Define the WCS URL with the correct parameters, including the provided token
        wcs_url = (
            f'crs=EPSG:25832&'
            f'format=GTiff&'
            f'identifier=dhm_terraen&'
            f'url=https://api.dataforsyningen.dk/dhm_wcs_DAF?'
            f'token={token}&'  # Use the token retrieved from the input field
            f'version=1.0.0&'
            f'service=WCS&'
            f'request=GetCoverage&'
            f'bbox=441000,6049000,894000,6403000&'
            f'width=1132500&'
            f'height=885000'
        )

        # Load the WCS layer using the constructed URL
        wcs_layer = QgsRasterLayer("wcs?" + wcs_url, "DHM Overflade", "wcs")
        
        # Check if the layer loaded successfully
        if not wcs_layer.isValid():
            print("Failed to load the WCS layer.")
            return None

        return wcs_layer
                
    def sampleElevationAlongPath(self, wcs_layer):
        line_layer = self.map_layers.currentLayer()

        if not line_layer:
            print("Selected line layer is not valid.")
            return

        # Get the buffer distance from the sampling_combobox
        try:
            sampling_distance = float(self.sampling_combobox.currentText())
        except ValueError:
            print("Invalid buffer distance.")
            return

        if self.selected_checkbox.isChecked():
            line_layer = self.getSelectedFeaturesLayer(line_layer)

        # Generate points along the line 
        points_result = processing.run("native:pointsalonglines", {
            'INPUT': line_layer,
            'DISTANCE': sampling_distance, 
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }, feedback=QgsProcessingFeedback())

        points_layer = points_result['OUTPUT'] 
        if not points_layer.featureCount():
            print("No points were generated along the line.")
            return

        # Initialize the progress dialog for sampling elevation
        total_points = points_layer.featureCount()
        self.progress_dialog.setLabelText("Sampling elevation...")
        self.progress_dialog.setMaximum(total_points)
        self.progress_dialog.setValue(0)

        # Prepare a new point layer to store elevation and distance data
        vl = QgsVectorLayer("Point?crs=epsg:25832", "Sampled Points", "memory")
        pr = vl.dataProvider()
        pr.addAttributes([QgsField("elevation", QVariant.Double), QgsField("distance", QVariant.Double)])
        vl.updateFields()

        # Initialize a variable to track the cumulative distance
        cumulative_distance = 0
        previous_point = None

        # Lists to store distances and elevations for graphing
        distances = []
        elevations = []
        feature_ids = []

        # Sample raster values for each point and calculate distances
        elevation_found = False
        for index, feature in enumerate(points_layer.getFeatures()):
            point = feature.geometry().asPoint()

            if previous_point is not None:
                cumulative_distance += QgsGeometry.fromPointXY(previous_point).distance(QgsGeometry.fromPointXY(point))
                cumulative_distance = round(cumulative_distance, 2) 

            elevation = wcs_layer.dataProvider().sample(point, 1) 
            if elevation[0] is not None:  # Check if sampling was successful
                elevation_found = True
                # Create a new feature to store this point, elevation, and distance
                fet = QgsFeature()
                fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(point)))
                fet.setAttributes([elevation[0], cumulative_distance])
                pr.addFeature(fet)
                vl.updateExtents()
                distances.append(cumulative_distance)
                elevations.append(elevation[0])
                feature_ids.append(fet.id())  # Store the ID of the newly added feature

            # Update the default symbol color 
            symbol = QgsSymbol.defaultSymbol(vl.geometryType())
            symbol.setColor(QColor(169, 0, 0))  
            vl.renderer().setSymbol(symbol)

            previous_point = point  # Update the previous point

            # Update progress dialog
            self.progress_dialog.setValue(index + 1)
            if self.progress_dialog.wasCanceled():
                break

        if elevation_found:
            # Update the layer with new features and add it to the project
            QgsProject.instance().addMapLayer(vl)
            print("Elevation and distance sampled along the path and added to the map.")

            # Show the plot dialog
            self.plot_dialog = PlotDialog(distances, elevations, vl, feature_ids, self)
            self.plot_dialog.show()  
            self.close()  # Close the PathProfilerDialog when showing the PlotDialog
        else:
            print("No elevation data could be sampled. Check if points are within the raster extent.")

    def getSelectedFeaturesLayer(self, layer):
        selected_features = layer.selectedFeatures()
        if not selected_features:
            print("No features selected.")
            return layer
        
        # Create a temporary layer with the selected features
        temp_layer = QgsVectorLayer("LineString?crs={}".format(layer.crs().authid()), "Selected Features", "memory")
        temp_provider = temp_layer.dataProvider()
        temp_provider.addFeatures(selected_features)
        return temp_layer

    def saveToken(self):
        token = self.token_edit.text().strip()
        if token:
            plugin_root_folder = os.path.dirname(__file__)
            token_file_path = os.path.join(plugin_root_folder, 'token.txt')
            try:
                with open(token_file_path, 'w') as token_file:
                    token_file.write(token)
                print(f"Token saved to {token_file_path}")
            except Exception as e:
                print(f"Failed to save token: {e}")

    def loadToken(self):
        plugin_root_folder = os.path.dirname(__file__)
        token_file_path = os.path.join(plugin_root_folder, 'token.txt')
        if os.path.exists(token_file_path):
            try:
                with open(token_file_path, 'r') as token_file:
                    token = token_file.read().strip()
                    self.token_edit.setText(token)
                    print(f"Token loaded from {token_file_path}")
            except Exception as e:
                print(f"Failed to load token: {e}")