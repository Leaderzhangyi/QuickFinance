import sys
import pandas as pd
import os
import re
import date 
import openpyxl
from views.Ui_main import Ui_MainForm
from qframelesswindow import FramelessWindow, StandardTitleBar, FramelessDialog
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog
from PySide6.QtCore import Qt

class MainWindow(QWidget, Ui_MainForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("QuickFine - ZinkCas v0.1")
        self.init_signal()

    def init_signal(self):
        self.tmpButton.clicked.connect(self.select_tmp_file)
        self.sofpButton.clicked.connect(self.select_sofp_file)
        self.profitButton.clicked.connect(self.select_profit_file)
        self.flowButton.clicked.connect(self.select_flow_file)
        self.startButton.clicked.connect(self.start_generate)

    def select_tmp_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择模板文件", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_name:
            self.lineEdit.setText(file_name)

    def select_sofp_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择资产负债表", "", "Excel Files (*.xls *.xlsx);;All Files (*)")
        if file_name:
            self.lineEdit_2.setText(file_name)

    def select_profit_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择利润表文件", "", "Excel Files (*.xls *.xlsx);;All Files (*)")
        if file_name:
            self.lineEdit_3.setText(file_name)

    def select_flow_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择现金流量表", "", "Excel Files (*.xls *.xlsx);;All Files (*)")
        if file_name:
            self.lineEdit_4.setText(file_name)

    def start_generate(self):
        from datetime import datetime
        today = datetime.today()
        date_str = today.strftime("%Y%m%d")
        output_path = f'{today}_演示.xlsx'
        template_path = self.lineEdit.text() or 'indexCal.xlsx'
        input_ofp_path = self.lineEdit_2.text() or '2023SOFP.xls'

        try:
            clean_data = self._process_data(input_ofp_path)
            self._write_data(clean_data, template_path, output_path)
            QMessageBox.information(self, "成功", f"数据成功写入 {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def _get_data(self, path, flag=None) -> pd.DataFrame:
        if flag == 'OFP':
            data = pd.read_excel(path, header=3)
        else:
            data = pd.read_excel(path)
        data.columns = data.columns.str.replace(" ", "", regex=False)
        return data

    def _process_data(self, input_ofp_path):
        ofpDf = self._get_data(input_ofp_path, 'OFP')
        ofpDf1 = ofpDf.iloc[:, :3]
        ofpDf2 = ofpDf.iloc[:, 4:-1]
        ofpDf2.columns = ofpDf1.columns
        odf = pd.concat([ofpDf1, ofpDf2], axis=0).reset_index(drop=True)
        odf = odf.dropna(subset=['期末余额'])
        odf.drop(columns=['行次'], inplace=True)
        odf.loc[:, '项目'] = odf.loc[:, '项目'].apply(lambda x: re.sub(r'^[△☆▲]', '', x.strip()).strip())
        odf = odf.set_index('项目')['期末余额']
        return dict(odf)

    def _write_data(self, data, temp_path, output_path):
        worksheet = openpyxl.load_workbook(temp_path)
        accounting_format = '#,##0.00'
        sheet = worksheet['Sheet1']
        for row in range(2, sheet.max_row + 1):
            item = sheet[f"B{row}"].value
            if item:
                item = item.strip()
                if item in data.keys():
                    sheet[f"C{row}"] = data[item]
                    sheet[f"C{row}"].number_format = accounting_format
        worksheet.save(output_path)

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    app.exec()