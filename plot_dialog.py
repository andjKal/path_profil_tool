from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDesktopWidget, QPushButton, QFileDialog, QMessageBox, QLabel, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotDialog(QDialog):
    def __init__(self, distances, elevations, map_layer, feature_ids, parent=None):
        super(PlotDialog, self).__init__(parent)
        self.distances = distances
        self.elevations = elevations
        self.map_layer = map_layer
        self.feature_ids = feature_ids
        self.initUI()

    def initUI(self):
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.ax = fig.add_subplot(111)
        
        # Calculate total distance
        total_distance = self.distances[-1]

        # Calculate total ascent and total descent
        total_ascent = sum(d2 - d1 for d1, d2 in zip(self.elevations, self.elevations[1:]) if d2 > d1)
        total_descent = sum(d1 - d2 for d1, d2 in zip(self.elevations, self.elevations[1:]) if d2 < d1)

        # Calculate net elevation change using the specified formula
        net_elevation_change = (-total_descent * -1) + total_ascent

        # Calculate total path distance including the elevation changes
        path_distance = total_distance + net_elevation_change
        
        # Format ascent, descent, and net change to 2 decimal places
        total_ascent_formatted = f"{total_ascent:.2f}"
        total_descent_formatted = f"{total_descent:.2f}"
        net_elevation_change_formatted = f"{net_elevation_change:.2f}"
        path_distance_formatted = f"{path_distance:.2f}"

        # Update plot with elevation data
        self.points_plot, = self.ax.plot(self.distances, self.elevations, 'o-', picker=5, markerfacecolor='blue', markersize=5, color='skyblue', linewidth=2)
        self.ax.set_xlabel('Distance (m)')
        self.ax.set_ylabel('Elevation (m)')

        layout = QHBoxLayout()

        # Add the canvas to the layout
        layout.addWidget(self.canvas)

        # Create a widget to hold the title with a fixed width
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_widget.setFixedWidth(200)

        # Add the title to the title layout
        title_layout.addWidget(QLabel(f"""Elevation Profile
        Linear Distance: {total_distance} m
        Elevation Change: {net_elevation_change_formatted} m
        Path Distance: {path_distance_formatted} m
        Total Ascent: {total_ascent_formatted} m
        Total Descent: {total_descent_formatted} m"""))

        # Add export button
        self.export_button = QPushButton("Export Line Graph")
        self.export_button.clicked.connect(self.export_graph)
        title_layout.addWidget(self.export_button)

        # Add a stretch to the title layout to push the title to the top
        title_layout.addStretch()

        # Add the title widget to the main layout
        layout.addWidget(title_widget)

        self.setLayout(layout)
        self.setWindowTitle("Elevation Along Path")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.position_window()
        self.canvas.mpl_connect('motion_notify_event', self.on_hover)

    def position_window(self):
        screen = QDesktopWidget().screenGeometry()
        width, height = 1200, 450
        x = screen.width() - width
        y = screen.height() - height
        self.setGeometry(x, y, width, height)

    def on_hover(self, event):
        if event.inaxes == self.ax:
            cont, ind = self.points_plot.contains(event)
            if cont:
                index = ind['ind'][0]
                self.highlight_point_on_map(self.feature_ids[index])

    def highlight_point_on_map(self, feature_id):
        self.map_layer.removeSelection()
        self.map_layer.selectByIds([feature_id])

    def export_graph(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.plot(self.distances, self.elevations, '-', color='skyblue', linewidth=2)
        ax.set_title('Elevation Profile')
        ax.set_xlabel('Distance (m)')
        ax.set_ylabel('Elevation (m)')

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                   "PNG Files (*.png);;JPEG Files (*.jpeg);;All Files (*)", options=options)

        if file_path:
            fig.savefig(file_path)
            QMessageBox.information(self, "Export Successful", f"Graph exported successfully to {file_path}")
        else:
            QMessageBox.warning(self, "Export Cancelled", "Export cancelled. No file was saved.")

    def closeEvent(self, event):
        # Deselect all selected features when closing the dialog
        self.map_layer.removeSelection()
        event.accept()  # Proceed with the default close event
