""" 
    第一个文件是tst.py

    第一段代码的功能和特点

    只是一段测试代码,只能操作测试的数据
    读取CSV文件的第一列：使用自定义函数read_first_column来读取CSV文件的第一列（即问题列）。
    模糊匹配：使用fuzzy_match函数来寻找给定查询与选择列表中的最佳匹配项，匹配分数超过80才认为是匹配。
    处理文件：主要处理函数process_files用于读取两个文件，并尝试用处理后的文件中的问题来更新处理前的文件中的问题。
    去重检查：确保更新后的文件中没有重复的问题。
    文件更新：如果匹配成功，则用匹配的问题替换原始问题，并将更新后的内容写回到处理前的文件中。

    问题

    直接操作数据,会破坏元数据
    只是单纯提取新题库的问题作为一行数据,没有保留老问题的答案
    没有改变顺序
    没有达成其他目标
 """
import pandas as pd
from fuzzywuzzy import process, fuzz

# 读取 CSV 文件的第一列（问题列）
def read_first_column(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        for line in file:
            parts = line.strip().split(',')
            if parts:
                questions.append(parts[0])  # 获取每行的第一列
    return questions

# 使用模糊匹配查找最佳匹配项
def fuzzy_match(query, choices):
    match, score = process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
    return match if score > 80 else None

# 主要处理函数
def process_files(before_file, after_file):
    # 读取文件
    before_questions = read_first_column(before_file)
    after_questions = read_first_column(after_file)
    
    # 打印前后问题列表以检查
    print(f"处理前文件中的问题数: {len(before_questions)}")
    print(f"处理后文件中的问题数: {len(after_questions)}")
    
    # 对处理前数据进行更新
    updated_questions = []
    for question in before_questions:
        match = fuzzy_match(question, after_questions)
        if match:
            updated_questions.append(match)
        else:
            print(f"警告: 问题 '{question}' 在处理后文件中没有找到匹配项")
            updated_questions.append(question)
    
    # 检查是否有重复的问题
    if len(updated_questions) != len(set(updated_questions)):
        raise ValueError("更新后的文件中存在重复的问题，请检查匹配结果")
    
    # 更新处理前文件
    with open(before_file, 'w', encoding='utf-8-sig') as file:
        for question in updated_questions:
            file.write(f"{question}\n")
    
    print(f"处理前文件已更新并保存为 {before_file}")

# 设置文件路径
before_file_path = r'C:\Users\a\Desktop\pyt\处理前.csv'
after_file_path = r'C:\Users\a\Desktop\pyt\处理后.csv'

# 执行处理
process_files(before_file_path, after_file_path)
