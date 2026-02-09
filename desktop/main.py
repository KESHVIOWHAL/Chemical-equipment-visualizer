import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QTableWidget, QTableWidgetItem, QMessageBox, QListWidget,
                             QSplitter, QGroupBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

class EquipmentVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_base_url = "http://127.0.0.1:8000/api"
        self.current_data = None
        self.initUI()
        self.load_datasets()
        
    def initUI(self):
        self.setWindowTitle('Chemical Equipment Parameter Visualizer - Desktop')
        self.setGeometry(100, 100, 1400, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Left panel - Upload and History
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(350)
        
        # Upload section
        upload_group = QGroupBox("Upload CSV File")
        upload_layout = QVBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setWordWrap(True)
        upload_layout.addWidget(self.file_label)
        
        btn_select = QPushButton("Select CSV File")
        btn_select.clicked.connect(self.select_file)
        upload_layout.addWidget(btn_select)
        
        btn_upload = QPushButton("Upload")
        btn_upload.clicked.connect(self.upload_file)
        btn_upload.setStyleSheet("background-color: #667eea; color: white; padding: 10px;")
        upload_layout.addWidget(btn_upload)
        
        upload_group.setLayout(upload_layout)
        left_layout.addWidget(upload_group)
        
        # History section
        history_group = QGroupBox("Dataset History (Last 5)")
        history_layout = QVBoxLayout()
        
        self.dataset_list = QListWidget()
        self.dataset_list.itemClicked.connect(self.load_dataset)
        history_layout.addWidget(self.dataset_list)
        
        btn_refresh = QPushButton("Refresh History")
        btn_refresh.clicked.connect(self.load_datasets)
        history_layout.addWidget(btn_refresh)
        
        btn_pdf = QPushButton("Download PDF Report")
        btn_pdf.clicked.connect(self.download_pdf)
        btn_pdf.setStyleSheet("background-color: #28a745; color: white; padding: 8px;")
        history_layout.addWidget(btn_pdf)
        
        history_group.setLayout(history_layout)
        left_layout.addWidget(history_group)
        
        left_layout.addStretch()
        
        # Right panel - Data display
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Summary statistics
        stats_group = QGroupBox("Summary Statistics")
        stats_layout = QHBoxLayout()
        
        self.stat_total = QLabel("Total: -")
        self.stat_flowrate = QLabel("Avg Flowrate: -")
        self.stat_pressure = QLabel("Avg Pressure: -")
        self.stat_temp = QLabel("Avg Temperature: -")
        
        for stat in [self.stat_total, self.stat_flowrate, self.stat_pressure, self.stat_temp]:
            stat.setStyleSheet("padding: 10px; background-color: #667eea; color: white; border-radius: 5px;")
            stats_layout.addWidget(stat)
        
        stats_group.setLayout(stats_layout)
        right_layout.addWidget(stats_group)
        
        # Charts
        charts_splitter = QSplitter(Qt.Horizontal)
        
        # Bar chart
        self.bar_figure = Figure(figsize=(5, 4))
        self.bar_canvas = FigureCanvas(self.bar_figure)
        charts_splitter.addWidget(self.bar_canvas)
        
        # Pie chart
        self.pie_figure = Figure(figsize=(5, 4))
        self.pie_canvas = FigureCanvas(self.pie_figure)
        charts_splitter.addWidget(self.pie_canvas)
        
        right_layout.addWidget(charts_splitter)
        
        # Data table
        table_group = QGroupBox("Equipment Details")
        table_layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.table.horizontalHeader().setStretchLastSection(True)
        table_layout.addWidget(self.table)
        
        table_group.setLayout(table_layout)
        right_layout.addWidget(table_group)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        self.selected_file = None
        
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f"Selected: {file_path.split('/')[-1]}")
    
    def upload_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Warning", "Please select a CSV file first!")
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.api_base_url}/upload/", files=files)
                
            if response.status_code == 201:
                data = response.json()
                self.current_data = data
                self.display_data(data)
                self.load_datasets()
                QMessageBox.information(self, "Success", "File uploaded successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Upload failed: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Upload failed: {str(e)}")
    
    def load_datasets(self):
        try:
            response = requests.get(f"{self.api_base_url}/datasets/")
            if response.status_code == 200:
                datasets = response.json()
                self.dataset_list.clear()
                for ds in datasets:
                    item_text = f"{ds['name']} - {ds['uploaded_at'][:19]}"
                    item = self.dataset_list.addItem(item_text)
                    self.dataset_list.item(self.dataset_list.count() - 1).setData(Qt.UserRole, ds['id'])
        except Exception as e:
            print(f"Error loading datasets: {e}")
    
    def load_dataset(self, item):
        dataset_id = item.data(Qt.UserRole)
        try:
            response = requests.get(f"{self.api_base_url}/datasets/{dataset_id}/")
            if response.status_code == 200:
                data = response.json()
                display_data = {
                    'total_count': data['total_count'],
                    'avg_flowrate': data['avg_flowrate'],
                    'avg_pressure': data['avg_pressure'],
                    'avg_temperature': data['avg_temperature'],
                    'type_distribution': data['type_distribution'],
                    'equipment': data['equipment']
                }
                self.current_data = display_data
                self.current_data['dataset_id'] = dataset_id
                self.display_data(display_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load dataset: {str(e)}")
    
    def display_data(self, data):
        # Update statistics
        self.stat_total.setText(f"Total: {data['total_count']}")
        self.stat_flowrate.setText(f"Avg Flowrate: {data['avg_flowrate']:.2f}")
        self.stat_pressure.setText(f"Avg Pressure: {data['avg_pressure']:.2f}")
        self.stat_temp.setText(f"Avg Temperature: {data['avg_temperature']:.2f}")
        
        # Update bar chart
        self.bar_figure.clear()
        ax1 = self.bar_figure.add_subplot(111)
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        values = [data['avg_flowrate'], data['avg_pressure'], data['avg_temperature']]
        colors = ['#4bc0c0', '#ff6384', '#ffce56']
        ax1.bar(parameters, values, color=colors)
        ax1.set_title('Average Parameters')
        ax1.set_ylabel('Value')
        self.bar_canvas.draw()
        
        # Update pie chart
        self.pie_figure.clear()
        ax2 = self.pie_figure.add_subplot(111)
        if data['type_distribution']:
            labels = list(data['type_distribution'].keys())
            sizes = list(data['type_distribution'].values())
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Equipment Type Distribution')
        self.pie_canvas.draw()
        
        # Update table
        equipment = data.get('equipment', [])
        self.table.setRowCount(len(equipment))
        for i, eq in enumerate(equipment):
            self.table.setItem(i, 0, QTableWidgetItem(str(eq.get('equipment_name', ''))))
            self.table.setItem(i, 1, QTableWidgetItem(str(eq.get('equipment_type', ''))))
            self.table.setItem(i, 2, QTableWidgetItem(str(eq.get('flowrate', ''))))
            self.table.setItem(i, 3, QTableWidgetItem(str(eq.get('pressure', ''))))
            self.table.setItem(i, 4, QTableWidgetItem(str(eq.get('temperature', ''))))
    
    def download_pdf(self):
        if not self.current_data or 'dataset_id' not in self.current_data:
            QMessageBox.warning(self, "Warning", "Please select a dataset first!")
            return
        
        try:
            dataset_id = self.current_data['dataset_id']
            url = f"{self.api_base_url}/datasets/{dataset_id}/pdf/"
            response = requests.get(url)
            
            if response.status_code == 200:
                file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", f"equipment_report_{dataset_id}.pdf", "PDF Files (*.pdf)")
                if file_path:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, "Success", "PDF downloaded successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to download PDF")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Download failed: {str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = EquipmentVisualizer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
