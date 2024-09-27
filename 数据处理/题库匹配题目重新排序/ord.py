# 这段代码主要用于将一个文件中的问题按照另一个文件中的顺序重新排序，并将结果写入一个新的文件中。以下是对其功能和逻辑的详细分析：

# 功能概述
# 文件读取：从指定路径读取两个文件的内容。
# 数据处理：从文件中提取问题，并进行模糊匹配，以确定正确的顺序。
# 重新排序：根据匹配结果重新排序问题，并确保没有重复的问题。
# 异常处理：处理匹配失败的情况，并在出现问题时停止执行。
# 结果输出：将重新排序后的问题写入一个新的文件。
from fuzzywuzzy import fuzz, process

# 这个函数用于读取文件内容，并去除每行的首尾空白字符，返回一个列表。
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]

# 这个函数用于将数据写入指定的文件路径，数据是以字符串形式的列表传递的，通过换行符连接后写入文件。
def write_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(data))

# 此函数用于执行模糊匹配，并返回最佳匹配项。如果没有找到匹配项，则抛出一个 ValueError。
def fuzzy_match(query, choices, scorer=fuzz.token_sort_ratio):
    query = query.strip()  # Remove leading/trailing whitespace
    choices = [choice.strip() for choice in choices]  # Clean up choices
    matches = process.extract(query, choices, scorer=scorer)
    if matches:
        print(f"Matching '{query}' to '{matches[0][0]}' with score {matches[0][1]}")
        return matches[0][0]  # Return the best match
    raise ValueError(f"No match found for '{query}'")

def main():
    # 新的提取顺序
    order_path = './find-new-data.txt'
    # 老的提取选项和答案
    questions_path = './find-old-data.txt'
    # 输出
    output_path = './Ordered.txt'
    
    # Read files
    # 首先，代码从 order_path 文件中读取内容，并从中提取出问题列表 order_questions
    order_lines = read_file(order_path)
    questions_lines = read_file(questions_path)
    
    # Extract questions from order.txt
    order_questions = [line.split(',')[0].strip() for line in order_lines]
    # 这里，order_lines 是从 order_path 文件中读取的所有行，order_questions 是提取了每行的第一个元素（通常是问题），并去除了首尾空格。

    # Extract questions from questionsetwithanswerOrdered.txt
    question_data = [line.split(',') for line in questions_lines]
    question_dict = {row[0].strip(): row for row in question_data}
    # 接下来，代码从 questions_path 文件中读取内容，并提取出问题及其相关信息，构建一个字典 question_dict
    # 这里，questions_lines 是从 questions_path 文件中读取的所有行，question_data 是分割后的数据，每一行作为一个列表元素。
    # question_dict 是一个字典，其中键是问题（第一个元素），值是整个分割后的行（列表形式）。

    # 上面这部分代码首先定义了文件路径，并读取了文件内容。然后，它提取了问题，并构建了一个字典，其中键是问题，值是包含问题及其相关信息的列表。

    # Reorder questionsetwithanswerOrdered.txt
    reordered_data = []
    processed_questions = set()
    # 然后，代码遍历 order_questions，使用模糊匹配来找到 question_dict 中的匹配项，并将其添加到 reordered_data 列表中：
    for question in order_questions:
        try:
            matched_question = fuzzy_match(question, question_dict.keys())
            if matched_question in processed_questions:
                print(f"Duplicate question found: '{matched_question}', skipping...")
                continue
            processed_questions.add(matched_question)
            reordered_data.append(','.join(question_dict[matched_question]))
        except ValueError as e:
            print(f"Error processing question '{question}': {e}")
            return
    # 上面这部分代码实现了重新排序的核心逻辑。
    # 这里的关键点在于 fuzzy_match 函数，它负责找到最佳匹配项。如果找到匹配项，并且该匹配项尚未被处理过（通过 processed_questions 集合检查），则将整个行（包括问题和答案）添加到 reordered_data 中。

    # 最后这部分代码首先打印原始文件和重新排序后的文件的行数，并验证它们是否一致。
    # Print and compare line counts
    original_line_count = len(question_data)
    reordered_line_count = len(reordered_data)
    print(f"Original line count: {original_line_count}")
    print(f"Reordered line count: {reordered_line_count}")

    # Check if line counts match
    # 这里通过比较 original_line_count 和 reordered_line_count 来确保数据的完整性。如果行数不一致，则抛出异常。否则，将 reordered_data 写入到指定的输出文件中
    if reordered_line_count != original_line_count:
        raise ValueError(f"Line count mismatch: {reordered_line_count} (reordered) != {original_line_count} (original)")

    # Write output
    write_file(output_path, reordered_data)
    print(f"Reordered file written to {output_path}")

if __name__ == '__main__':
    main()
