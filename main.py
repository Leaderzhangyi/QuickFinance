import sys
import pandas as pd
import os
import re
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
        self.tmpButton.clicked.connect(lambda: self.select_file("选择模板文件", "Excel Files (*.xlsx);;All Files (*)", self.lineEdit))
        self.sofpButton.clicked.connect(lambda: self.select_file("选择资产负债表", "Excel Files (*.xls *.xlsx);;All Files (*)", self.lineEdit_2))
        self.profitButton.clicked.connect(lambda: self.select_file("选择利润表文件", "Excel Files (*.xls *.xlsx);;All Files (*)", self.lineEdit_3))
        self.flowButton.clicked.connect(lambda: self.select_file("选择现金流量表", "Excel Files (*.xls *.xlsx);;All Files (*)", self.lineEdit_4))
        self.startButton.clicked.connect(self.start_generate)

    def select_file(self, title, file_filter, target_lineedit):
        file_name, _ = QFileDialog.getOpenFileName(self, title, "", file_filter)
        if file_name:
            target_lineedit.setText(file_name)


    def start_generate(self):
        from datetime import datetime
        today = datetime.today()
        date_str = today.strftime("%Y%m%d")
        output_path = f'{today}_演示.xlsx'
        template_path = self.lineEdit.text() 
        input_ofp_path = self.lineEdit_2.text() 
        if template_path == '':
            QMessageBox.critical(self, "错误", "请选择模板文件")
            return
        elif input_ofp_path == '':
            QMessageBox.critical(self, "错误", "请选择资产负债表文件")
            return

        

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


    def _process_ofp_data(self,ofpDf) -> pd.DataFrame:
        ofpDf1 = ofpDf.iloc[:, :3]
        ofpDf2 = ofpDf.iloc[:, 4:-1]
        ofpDf2.columns = ofpDf1.columns
        odf = pd.concat([ofpDf1, ofpDf2], axis=0).reset_index(drop=True)
        odf = odf.dropna(subset=['期末余额'])
        odf.drop(columns=['行次'], inplace=True)
        odf.loc[:, '项目'] = odf.loc[:, '项目'].apply(lambda x: re.sub(r'^[△☆▲]', '', x.strip()).strip())
        odf = odf.set_index('项目')['期末余额']
        return odf

    def _process_data(self, input_ofp_path):
        ofpDf = self._get_data(input_ofp_path, 'OFP')
        odf = self._process_ofp_data(ofpDf)

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