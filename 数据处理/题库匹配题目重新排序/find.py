""" 
第二段代码的功能和特点
简单文本文件读取：使用read_file函数读取简单的文本文件，返回每一行的内容作为列表。
模糊匹配：使用fuzzy_match函数进行模糊匹配，返回最佳匹配项及其得分。
主函数执行：main函数执行主要逻辑，包括读取两个文件，提取问题，找出未匹配的问题以及低得分的匹配。
输出结果：输出未匹配的问题和低得分的匹配项，便于后续处理或人工审核。

缺点

只是在出现异常时报错自动停下
要我们自己去找出问题点
因为a和b问题总数都是400
里面各换了一个题
这个程序会输出不匹配的题

 """
from fuzzywuzzy import fuzz, process

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]

def fuzzy_match(query, choices, scorer=fuzz.token_sort_ratio):
    query = query.strip()  # Remove leading/trailing whitespace
    choices = [choice.strip() for choice in choices]  # Clean up choices
    matches = process.extract(query, choices, scorer=scorer, limit=1)
    if matches:
        return matches[0]  # Return the best match (as a tuple with score)
    return None  # No match found

def find_unmatched_and_low_score(a_lines, b_lines, scorer=fuzz.token_sort_ratio):
    unmatched_a_to_b = []
    unmatched_b_to_a = []
    low_score_a_to_b = []
    low_score_b_to_a = []

    # Find unmatched and low score matches from A to B
    for a_line in a_lines:
        match = fuzzy_match(a_line, b_lines, scorer)
        if match is None:
            unmatched_a_to_b.append(a_line)
        else:
            matched_b_line, score = match
            if score < 80:
                low_score_a_to_b.append((a_line, matched_b_line, score))
    
    # Find unmatched and low score matches from B to A
    for b_line in b_lines:
        match = fuzzy_match(b_line, a_lines, scorer)
        if match is None:
            unmatched_b_to_a.append(b_line)
        else:
            matched_a_line, score = match
            if score < 80:
                low_score_b_to_a.append((b_line, matched_a_line, score))

    return unmatched_a_to_b, unmatched_b_to_a, low_score_a_to_b, low_score_b_to_a

def main():
    order_path = './find-new-data.txt'
    questions_path = './find-old-data.txt'
    
    # Read files
    order_lines = read_file(order_path)
    questions_lines = read_file(questions_path)
    
    # Extract questions from order.txt
    order_questions = [line.split(',')[0].strip() for line in order_lines]

    # Extract questions from questionsetwithanswer.txt
    questions = [line.split(',')[0].strip() for line in questions_lines]

    # Find unmatched questions and low score matches
    unmatched_a_to_b, unmatched_b_to_a, low_score_a_to_b, low_score_b_to_a = find_unmatched_and_low_score(order_questions, questions)

    # Output unmatched questions
    if unmatched_a_to_b:
        print("The following questions from order.txt could not be matched:")
        for unmatched_question in unmatched_a_to_b:
            print(f"  - {unmatched_question}")

    if unmatched_b_to_a:
        print("The following questions from questionsetwithanswer.txt could not be matched:")
        for unmatched_question in unmatched_b_to_a:
            print(f"  - {unmatched_question}")

    # Output low score matches
    if low_score_a_to_b:
        print("The following questions from order.txt had low score matches (score < 80):")
        for original_question, matched_question, score in low_score_a_to_b:
            print(f"  - Original: '{original_question}' matched to '{matched_question}' with score {score}")

    if low_score_b_to_a:
        print("The following questions from questionsetwithanswer.txt had low score matches (score < 80):")
        for original_question, matched_question, score in low_score_b_to_a:
            print(f"  - Original: '{original_question}' matched to '{matched_question}' with score {score}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")