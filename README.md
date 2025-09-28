### QuickFinance

一款基于 PySide6 的轻量级财务报表填充工具。将资产负债表等原始 Excel 数据读取并按模板规则写入到模板文件中，便于快速生成演示/汇报用的指标表。

---

## 功能概览
- **选择模板**: 选择 Excel 模板文件（默认 `indexCal.xlsx`）。
- **读取财务表**: 读取资产负债表（.xls 或 .xlsx）。
- **自动清洗**: 去除前缀符号（如 △/☆/▲）、剔除空值、按“项目/期末余额”对齐。
- **写入模板**: 将匹配到的“项目”的“期末余额”写入模板 `Sheet1` 的 `C` 列，并设置会计数值格式。
- **结果输出**: 在程序目录生成 `YYYYMMDD_演示.xlsx`（当日时间戳）。

> 模板要求：`Sheet1` 表内，`B` 列为项目名称，`C` 列为数值列（程序会写入/覆盖）。

## 运行环境
- Windows 10/11
- Python >= 3.11

## 依赖
项目使用以下主要依赖（已在 `pyproject.toml`/`uv.lock` 中声明）：
- `pandas`
- `openpyxl`
- `xlrd`
- `pyside6-fluent-widgets[full]`

## 快速开始

### 方式一：使用 uv（推荐）
1) 安装 uv（若未安装）
   - 可参考 uv 官方安装指引，或通过包管理器安装。
2) 在项目根目录执行：
```bash
uv sync
```
3) 编译 UI（可选，若已存在 `views/Ui_main.py` 可跳过）：
```bash
uv run python build_resources.py build
# 或直接双击/运行 Windows 批处理：
build.bat
```
4) 运行：
```bash
uv run python main.py
```

### 方式二：使用 venv + pip
```bash
# 创建虚拟环境（Windows）
py -3.11 -m venv .venv
.\.venv\Scripts\activate

# 安装依赖
pip install -U pip
pip install openpyxl pandas "pyside6-fluent-widgets[full]" xlrd

# 编译 UI（可选）
python build_resources.py build

# 运行
python main.py
```

## 使用说明
1) 打开程序后，依次点击：
   - “选择模板文件” → 选择模板（如 `indexCal.xlsx`）
   - “选择资产负债表” → 选择 `.xls/.xlsx` 源数据（默认 `2023SOFP.xls`）
   - 其它表（利润表/现金流量表）控件已预留，当前版本仅使用资产负债表输入
2) 点击“开始生成”
3) 程序会将匹配到的“项目”的“期末余额”写入模板 `Sheet1!C列`，并在程序目录生成 `YYYYMMDD_演示.xlsx`

### 源数据要求（资产负债表）
- 建议表头在第 4 行（程序对 OFP 使用 `header=3` 读取），并包含至少以下中文列：
  - `项目`、`期末余额`（若存在 `行次` 列会被自动移除）
- 程序会：
  - 标准化列名（移除空格）
  - 去除 `项目` 前缀符号（正则 `^[△☆▲]`）
  - 丢弃 `期末余额` 为空的记录

### 模板要求
- `Sheet1`：
  - `B2:B*` 为项目名称；
  - `C2:C*` 为待写入的数值列；
  - 数字格式会设置为 `#,##0.00`。

## 目录结构
```
QuickFinance/
├─ main.py                 # 入口，启动 PySide6 窗口
├─ build_resources.py      # 编译 .ui/.qrc 到 Python 文件
├─ build.bat               # Windows 编译辅助脚本（支持 uv 调用）
├─ resource/ui/main.ui     # Qt Designer 生成的 UI
├─ views/Ui_main.py        # 由 UI 编译生成的 Python 类
├─ pyproject.toml          # 依赖与元数据
└─ README.md
```

## 常见问题
- 无法读取 `.xls`：请确保安装了 `xlrd>=2.0.2`。
- 无法读取 `.xlsx`：`pandas` 会使用 `openpyxl` 处理 `.xlsx`，确保已安装 `openpyxl`。
- 找不到 `pyside6-uic`/`pyside6-rcc`：
  - 使用 `uv run python build_resources.py check` 检查工具；
  - 或在已激活的虚拟环境中重新安装 `pyside6-fluent-widgets[full]`（会带入 PySide6）。
- 字段未写入模板：请检查模板 `Sheet1` 的 `B` 列项目名称与源数据的 `项目` 一致（去除了前缀符号）。

## 许可
本项目采用 `LICENSE` 中所述的开源许可协议。

## 致谢
- UI 基于 PySide6 与 Fluent Widgets。
- 感谢社区对数据处理与桌面开发生态的贡献。


