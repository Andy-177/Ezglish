import os
import random
import json

# 生成默认的配置文件
def generate_default_config(config_path):
    default_config = {
        "dictionary_path": "dictionary.txt",
        "num_words": 10
    }
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(default_config, file, indent=4)
    print(f"生成了默认的配置文件 {config_path}")

# 读取配置文件
def load_config(config_path):
    if not os.path.exists(config_path):
        generate_default_config(config_path)
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

# 读取词典文件
def parse_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    dictionary = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 2:
            continue
        word = parts[0].strip()
        definitions = parts[1].strip()
        dictionary[word] = definitions

    return dictionary

# 读取分数记录文件
def load_scores(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as file:
        scores = {}
        for line in file:
            word, score = line.strip().split('=')
            scores[word] = int(score)
    return scores

# 保存分数记录文件
def save_scores(file_path, scores):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word, score in scores.items():
            file.write(f"{word}={score}\n")

# 背单词函数
def study_words(dictionary, scores, mode, num_words):
    words = [word for word, score in scores.items() if score < 4]
    if mode == 'random':
        random.shuffle(words)

    words_to_study = words[:num_words]

    correct_count = 0
    incorrect_count = 0
    incorrect_words = []

    for word in words_to_study:
        print(f"\n定义: {dictionary[word]}")
        user_input = input("请输入这个单词的拼写: ").strip().lower()
        if user_input == word.lower():
            scores[word] = min(scores.get(word, 0) + 1, 4)
            if scores[word] == 4:
                print("恭喜，你已经完全记住这个单词了！")
            correct_count += 1
        else:
            scores[word] = max(scores.get(word, 0) - 1, 0)
            if scores[word] == 0:
                print("这个单词需要再复习一下。")
            print(f"正确答案是: {word}")
            incorrect_count += 1
            incorrect_words.append(word)

    total_words = correct_count + incorrect_count
    correct_rate = (correct_count / total_words) * 100 if total_words > 0 else 0
    incorrect_rate = (incorrect_count / total_words) * 100 if total_words > 0 else 0

    print("\n本轮总结：")
    print(f"总单词数: {total_words}")
    print(f"正确单词数: {correct_count} ({correct_rate:.2f}%)")
    print(f"错误单词数: {incorrect_count} ({incorrect_rate:.2f}%)")
    if incorrect_words:
        print("错误的单词列表:")
        for word in incorrect_words:
            print(f"  - {word}")

# 主函数
def main():
    config_path = 'config.json'
    config = load_config(config_path)
    dictionary_path = config['dictionary_path']
    num_words = config['num_words']

    if not os.path.exists(dictionary_path):
        print(f"词典文件 {dictionary_path} 不存在，请检查路径是否正确。")
        return

    dictionary = parse_dictionary(dictionary_path)
    scores_path = os.path.splitext(dictionary_path)[0] + '.cfg'
    scores = load_scores(scores_path)

    # 初始化所有单词的分数
    for word in dictionary.keys():
        if word not in scores:
            scores[word] = 0

    print("欢迎使用背单词软件！")
    print("请选择模式：")
    print("1. 顺序模式")
    print("2. 随机模式")
    mode = input("请输入模式编号 (1 或 2): ").strip()

    if mode == '1':
        study_words(dictionary, scores, 'sequential', num_words)
    elif mode == '2':
        study_words(dictionary, scores, 'random', num_words)
    else:
        print("无效的模式编号！")

    save_scores(scores_path, scores)
    print("当前的背单词任务已经完成！再见！")

if __name__ == "__main__":
    main()
