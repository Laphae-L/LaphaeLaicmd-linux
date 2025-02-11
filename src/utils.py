"""其他函数"""

import time
import sys
import re
import os

import config as cf
import globals as gl



def extract_command(text):
    """匹配被"///"包裹的文本"""
    pattern = r'///(.*?)///'
    match = re.search(pattern, text)  # 查找第一个匹配项
    return match.group(1) if match else ""  # 如果没有匹配项则返回空



def set_color(text, color="37"):
    """转为带颜色的字符串"""
    return f"\033[{color}m" + text + "\033[0m"



def print_and_record(text, end='\n'):
    """打印文本并记录到历史"""
    print(text, end=end)
    
    gl.history += text + end



def slow_print(text, print_time=0.10, max_delay=0.01, end='\n', record=True):
    """逐字打印文本"""

    delay = print_time / len(text)
    if delay > max_delay:
        delay = max_delay

    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

    print("", end=end)

    if record:
        gl.history += text + end



_last_spoker = ""
def print_spoker(spoker=None, raw_name=None, end='', record=True):
    """打印发言人"""
    global _last_spoker
    
    if spoker is None:
        spoker = set_color(cf.program_name, cf.program_name_color)
        raw_name = cf.program_name
    
    if _last_spoker!= spoker:
        print(spoker + ": ", end=end)
        _last_spoker = spoker

    if record:
        if raw_name is not None:
            gl.history += raw_name + ": " + end
        else:
            gl.history += spoker + ": " + end


def confirm(printstr = "是否同意?", program_name = ""):
    """打印[Y/n]确认界面"""

    print_spoker()
    print_and_record(printstr + "[Y/n]", end="")

    result = input()
    gl.history += result + "\n"

    return True if result.lower() == 'y' or (not result) else False # 如果输入y或无输入，则返回True



def read_file(file_path):
    """读取文件"""

    if not os.path.exists(file_path):
        raise Exception("文件不存在") from None
        
    else:
        try:
            # 打开文件，指定相对路径
            with open(file_path, 'r', encoding='utf-8') as file:
                # 返回文件内容到字符串
                return file.read()
        except Exception as e:
            raise Exception(str(e)) from None