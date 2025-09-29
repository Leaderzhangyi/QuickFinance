import sys
import pandas as pd
import os
import re
import openpyxl
from datetime import datetime
from views.Ui_main import Ui_MainForm
from omegaconf import OmegaConf
from qfluentwidgets import CommandBar,Action,FluentIcon,CommandBarView
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog, QMenuBar,QWidgetAction
from PySide6.QtGui import QIcon,QDesktopServices
from PySide6.QtCore import Qt, QUrl
import resource_rc

if sys.platform == 'win32':
    try:
        import ctypes  # type: ignore
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("bai.ImageCDSSystem")
    except Exception:
        pass

CONFIG_FILE = "config.yaml"

def ensure_config():
    if not os.path.exists(CONFIG_FILE):
        cfg = OmegaConf.create({"PATH": {"OSFP": "", "PROFIT": "", "FLOW": "", "TMP": ""}})
        OmegaConf.save(cfg, CONFIG_FILE)
    return OmegaConf.load(CONFIG_FILE)
class MainWindow(QWidget, Ui_MainForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("QuickFine - ZinkCas v0.1")
        self.setWindowIcon(QIcon(":/imgs/logo.png"))
        self.init_signal()
        self.init_status()
        self.init_menu()

    def init_menu(self):
        # 创建菜单栏
        commandBar = CommandBar()
        commandBar.addAction(Action(FluentIcon.GITHUB, '分享', triggered=lambda: QDesktopServices.openUrl(QUrl("https://github.com/Leaderzhangyi/QuickFinance"))))
  

        self.verticalLayout.insertWidget(0, commandBar)
     
    def init_status(self):
        self.comboBox.addItems(["2022", "2023", "2024", "2025"])
        self.config = ensure_config()
        self.path_map = {
            "TMP": self.lineEdit,
            "OSFP": self.lineEdit_2,
            "PROFIT": self.lineEdit_3,
            "FLOW": self.lineEdit_4,
        }
         # 初始化 lineEdit
        for key, lineedit in self.path_map.items():
            if self.config.PATH.get(key):
                lineedit.setText(self.config.PATH[key])

    def init_signal(self):
        button_map = {
            self.tmpButton: ("选择模板文件", "Excel Files (*.xlsx *.xls);;All Files (*)", "TMP"),
            self.sofpButton: ("选择资产负债表", "Excel Files (*.xls *.xlsx);;All Files (*)", "OSFP"),
            self.profitButton: ("选择利润表文件", "Excel Files (*.xls *.xlsx);;All Files (*)", "PROFIT"),
            self.flowButton: ("选择现金流量表", "Excel Files (*.xls *.xlsx);;All Files (*)", "FLOW"),
        }

        # 循环绑定
        for btn, (title, ffilter, key) in button_map.items():
            btn.clicked.connect(lambda _, t=title, f=ffilter, k=key: self.select_file(t, f, k))

        self.startButton.clicked.connect(self.start_generate)

    def select_file(self, title, file_filter, key):
        file_name, _ = QFileDialog.getOpenFileName(self, title, "", file_filter)
        if file_name:
            # 更新 UI
            self.path_map[key].setText(file_name)
            # 更新 config
            self.config.PATH[key] = file_name
            OmegaConf.save(self.config, CONFIG_FILE)


    def start_generate(self):
        today = int(datetime.now().timestamp())
        output_path = f'{today}_自动填充表.xlsx'
        template_path = self.lineEdit.text() 
        input_ofp_path = self.lineEdit_2.text() 
        input_profit_path = self.lineEdit_3.text() 
        input_flow_path = self.lineEdit_4.text() 
        if template_path == '':
            QMessageBox.critical(self, "错误", "请选择模板文件")
            return
        elif input_ofp_path == '':
            QMessageBox.critical(self, "错误", "请选择资产负债表文件")
            return
        try:
            clean_data = self._process_data(input_ofp_path,input_profit_path,input_flow_path)
            self._write_data(clean_data, template_path, output_path)
            QMessageBox.information(self, "成功", f"数据成功写入 {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def _get_data(self, path) -> pd.DataFrame:
        data = pd.read_excel(path, header=3,na_values=['0'])
        data.columns = data.columns.str.replace(" ", "", regex=False)
         # 自定义去重逻辑，给重复列名加下标
        seen = {}
        new_cols = []
        for c in data.columns:
            if c not in seen:
                seen[c] = 0
                new_cols.append(c)
            else:
                seen[c] += 1
                new_cols.append(f"{c}.{seen[c]}")
        data.columns = new_cols
        return data


    def _parse_data(self,pdfunit:tuple) -> pd.Series:

        """
        解析df单元格数据
        """
        df,flag = pdfunit
        if flag == 'OFP':
            colName = '期末余额'
        else:
            colName = '本期金额'
        df1 = df.loc[:,["项目",colName]]
        df2 = df.loc[:,["项目.1",f"{colName}.1"]]
        # import ipdb;ipdb.set_trace()
        df2.columns = df1.columns
        df = pd.concat([df1, df2], axis=0).reset_index(drop=True)
        df = df.dropna(subset=[colName])
        # 只保留字符串
        df = df[df['项目'].apply(lambda x: isinstance(x, str))]
        # 去掉 '0' 和空字符串
        df = df[~df['项目'].str.strip().isin(["0", ""])]
        # 去掉开头符号
        df.loc[:, '项目'] = df['项目'].apply(lambda x: re.sub(r'^[△☆▲*# ]', '', x.strip()))
        # 去掉序号 (一、二、三... / （一）（二）... / 1. 2. ...)
        df.loc[:, '项目'] = df['项目'].apply(lambda x: re.sub(r'^[一二三四五六七八九十]+、|^（[一二三四五六七八九十]+）|^\d+\.', '', x.strip()).strip())
        # 去掉空格
        df.loc[:, '项目'] = df['项目'].str.replace(' ', '', regex=False)
        # 转成 Series
        dseries = df.set_index('项目')[colName]
        return dseries



    def _process_data(self, input_ofp_path,input_profit_path,input_flow_path) -> dict:
        # data load ``
        ofpDf = self._get_data(input_ofp_path)
        pseries = pd.Series()
        fseries = pd.Series()
        if input_profit_path != '' or input_flow_path != '':
            profitDf = self._get_data(input_profit_path)
            flowDf = self._get_data(input_flow_path)
            pseries = self._parse_data((profitDf,'PROFIT'))
            fseries = self._parse_data((flowDf,'FLOW'))

        oseries = self._parse_data((ofpDf,'OFP'))
        print(oseries)

        return dict(oseries) | dict(pseries) | dict(fseries)

    def _write_data(self, data, temp_path, output_path):
        print(data.keys())
        worksheet = openpyxl.load_workbook(temp_path)
        accounting_format = '#,##0.00'
        sheet = worksheet['Sheet1']
        year = self.comboBox.currentText()
        if year == "2022":
            col = "C"
        elif year == "2023":
            col = "D"
        elif year == "2024":
            col = "F"
        elif year == "2025":
            col = "H"
        sheet[f"{col}1"] = f"{year}-12-31"
        for row in range(2, sheet.max_row + 1):
            item = sheet[f"B{row}"].value
            if item:
                item = item.strip()
                if item in data.keys():
                    sheet[f"{col}{row}"] = data[item]
                    sheet[f"{col}{row}"].number_format = accounting_format
        worksheet.save(output_path)

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    app.exec()