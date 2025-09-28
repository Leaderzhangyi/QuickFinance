#!/usr/bin/env python3
"""
编译Qt资源文件和UI文件的脚本
支持编译.qrc文件和.ui文件
"""

import os
import sys
import subprocess
import glob
from pathlib import Path

class QtResourceBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        print(self.project_root)
        self.resource_dir = self.project_root / "resource"
        self.views_dir = self.resource_dir / "ui"
        
    def find_qrc_files(self):
        """查找所有的.qrc文件"""
        qrc_files = []
        
        # 查找resource目录下的.qrc文件
        if self.resource_dir.exists():
            qrc_files.extend(self.resource_dir.glob("*.qrc"))
        
        # 查找views目录下的.qrc文件
        if self.views_dir.exists():
            qrc_files.extend(self.views_dir.rglob("*.qrc"))
        
        return qrc_files
    
    def find_ui_files(self):
        """查找所有的.ui文件"""
        ui_files = []
        
        # 查找views目录下的.ui文件
        if self.views_dir.exists():
            ui_files.extend(self.views_dir.rglob("*.ui"))
        
        return ui_files
    
    def compile_qrc_file(self, qrc_file):
        """编译单个.qrc文件"""
        try:
            # 生成输出文件名
            output_file = qrc_file.parent / f"{qrc_file.stem}_rc.py"
            
            # 使用pyside6-rcc编译
            cmd = ["pyside6-rcc", str(qrc_file), "-o", str(output_file)]
            
            print(f"编译资源文件: {qrc_file.name} -> {output_file.name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                print(f"✅ 成功编译: {qrc_file.name}")
                return True
            else:
                print(f"❌ 编译失败: {qrc_file.name}")
                print(f"错误信息: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 编译失败: {qrc_file.name}")
            print(f"错误信息: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ 编译异常: {qrc_file.name}")
            print(f"异常信息: {e}")
            return False
    
    def compile_ui_file(self, ui_file):
        """编译单个.ui文件"""
        try:
            # 生成输出文件名
            output_file = ui_file.parent / f"Ui_{ui_file.stem}.py"
            
            # 使用pyside6-uic编译
            cmd = ["pyside6-uic", str(ui_file), "-o", str(output_file)]
            
            print(f"编译UI文件: {ui_file.name} -> {output_file.name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                print(f"✅ 成功编译: {ui_file.name}")
                return True
            else:
                print(f"❌ 编译失败: {ui_file.name}")
                print(f"错误信息: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 编译失败: {ui_file.name}")
            print(f"错误信息: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ 编译异常: {ui_file.name}")
            print(f"异常信息: {e}")
            return False
    
    def check_tools(self):
        """检查编译工具是否可用"""
        tools = {
            "pyside6-rcc": "资源文件编译器",
            "pyside6-uic": "UI文件编译器"
        }
        
        missing_tools = []
        
        for tool, description in tools.items():
            try:
                result = subprocess.run([tool, "--help"], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                if result.returncode == 0:
                    print(f"✅ {tool} ({description}) - 可用")
                else:
                    missing_tools.append(tool)
                    print(f"❌ {tool} ({description}) - 不可用")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                missing_tools.append(tool)
                print(f"❌ {tool} ({description}) - 未找到")
        
        return len(missing_tools) == 0
    
    def build_all(self):
        """编译所有资源文件和UI文件"""
        print("=" * 50)
        print("开始编译Qt资源文件和UI文件")
        print("=" * 50)
        
        # 检查工具
        if not self.check_tools():
            print("\n❌ 编译工具检查失败，请确保已正确安装PySide6")
            return False
        
        print("\n" + "=" * 50)
        
        # 编译.qrc文件
        qrc_files = self.find_qrc_files()
        if qrc_files:
            print(f"\n找到 {len(qrc_files)} 个资源文件:")
            for qrc_file in qrc_files:
                print(f"  - {qrc_file}")
            
            print("\n开始编译资源文件...")
            qrc_success = 0
            for qrc_file in qrc_files:
                if self.compile_qrc_file(qrc_file):
                    qrc_success += 1
            
            print(f"\n资源文件编译结果: {qrc_success}/{len(qrc_files)} 成功")
        else:
            print("\n未找到.qrc文件")
        
        # 编译.ui文件
        ui_files = self.find_ui_files()
        if ui_files:
            print(f"\n找到 {len(ui_files)} 个UI文件:")
            for ui_file in ui_files:
                print(f"  - {ui_file}")
            
            print("\n开始编译UI文件...")
            ui_success = 0
            for ui_file in ui_files:
                if self.compile_ui_file(ui_file):
                    ui_success += 1
            
            print(f"\nUI文件编译结果: {ui_success}/{len(ui_files)} 成功")
        else:
            print("\n未找到.ui文件")
        
        print("\n" + "=" * 50)
        print("编译完成!")
        print("=" * 50)
        
        return True
    
    def clean_generated_files(self):
        """清理生成的文件"""
        print("清理生成的文件...")
        
        # 清理生成的资源文件
        for pattern in ["*_rc.py", "Ui_*.py"]:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    try:
                        file_path.unlink()
                        print(f"删除: {file_path}")
                    except Exception as e:
                        print(f"删除失败 {file_path}: {e}")
        
        print("清理完成!")

def main():
    """主函数"""
    builder = QtResourceBuilder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "clean":
            builder.clean_generated_files()
        elif command == "check":
            builder.check_tools()
        elif command == "help":
            print("""
Qt资源文件编译脚本

用法:
    python build_resources.py [命令]

命令:
    build     - 编译所有资源文件和UI文件 (默认)
    clean     - 清理生成的文件
    check     - 检查编译工具是否可用
    help      - 显示帮助信息

示例:
    python build_resources.py build
    python build_resources.py clean
    python build_resources.py check
            """)
        else:
            print(f"未知命令: {command}")
            print("使用 'python build_resources.py help' 查看帮助")
    else:
        # 默认执行编译
        builder.build_all()

if __name__ == "__main__":
    main()
