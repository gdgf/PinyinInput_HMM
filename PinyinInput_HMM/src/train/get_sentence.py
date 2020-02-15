import os
from src import util

ARTICLE_DIR = '../../data/data1'
SENTENCE_FILE = '../../result/sentence.txt'


# 从文本中得到句子，
def extract_chinese_sentences(content):
    # 变为unicode字符
    content = util.as_text(content)
    content = content.replace(' ', '')  # 删除空格
    content = content.replace('\t', '') # 去掉制表符
    sentences = []
    s = ''
    for c in content:
        if util.is_chinese(c):  # 如果是汉字
            s += c
        else:
            sentences.append(s)   # 遇到非汉字编码就算一个句子
            s = ''
    sentences.append(s)
    # 一个句子去除多余的空格后，长度大于1的返回，防止返回一些空串
    return [s.strip() for s in sentences if len(s.strip()) > 1]

def get_sentence():
    all_files = []
    filenames = os.listdir(ARTICLE_DIR)
    # 得到带有路径的文件名
    for filename in filenames:
        p = os.path.join(ARTICLE_DIR, filename)
        if p.endswith('.txt'):
            all_files.append(p)

    newsentence = open(SENTENCE_FILE, 'w', encoding="utf-8")
    for fp in all_files:
        print('处理文件: ' + fp)
        with open(fp, encoding="utf-8") as out:
            content = out.read()
            sentences = extract_chinese_sentences(content)
            newsentence.write('\n'.join(sentences) + '\n')
    newsentence.close()


def main():
    get_sentence()


if __name__ == '__main__':
    main()
