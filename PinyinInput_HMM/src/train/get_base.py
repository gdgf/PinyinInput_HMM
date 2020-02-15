# coding: utf-8
"""
功能：根据sentence.txt、word.txt、hanzipinyin.txt，统计计算得到三个文件；
输入：sentence1.txt、word.txt、hanzipinyin.txt；
输出：
result/base_start.txt，一个汉字出现在序列（sentence or word）开头的次数，为了计算初始状态概率分布；
result/base_emission.txt，一个汉字对应的各种拼音（多音字）在语料 （sentence1.txt、word.txt）中出现的次数，为了计算从某个状态观察到特定符号的概率分布矩阵；
result/base_transition.txt，一个汉字后面出现某个汉字的次数，为了计算状态转移矩阵；
"""
import sys
import json
from ChineseTone import PinyinHelper
from src import util

SENTENCE_FILE = '../../result/sentence.txt'
WORD_FILE = '../../data/data2/word.txt'
HANZI2PINYIN_FILE = '../../data/data2/hanzipinyin.txt'

BASE_START = '../../result/base_start.txt'
BASE_EMISSION = '../../result/base_emission.txt'
BASE_TRANSITION = '../../result/base_transition.txt'


def writejson2file(data, filename):
    with open(filename, 'w') as outfile:
        data = json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False)
        #data = json.dumps(data, indent=4, sort_keys=True)
        outfile.write(data)


def topinyin(s):
    """
    s都是汉字
    """
    s = util.as_text(s)
    py_list = PinyinHelper.convertToPinyinFromSentence(s)
    result = []
    for py in py_list:
        py = util.as_text(py)
        if py == '〇':
            result.append('ling')
        else:
            result.append(util.simplify_pinyin(py))

    if ',' in ''.join(result):
        print(s)
        print(''.join(result))
        sys.exit()
    return result


def extract_chinese_sentences(content):
    content = util.as_text(content)
    content = content.replace(' ', '')
    content = content.replace('\t', '')
    sentences = []
    s = ''
    for c in content:
        if util.is_chinese(c):
            s += c
        else:
            sentences.append(s)
            s = ''
    sentences.append(s)

    return [s.strip() for s in sentences if len(s.strip()) > 1]


def process_hanzipinyin(emission):
    # ./hanzipinyin.txt
    print('read from hanzipinyin.txt')
    for line in open(HANZI2PINYIN_FILE, encoding="utf-8"):
        line = util.as_text(line.strip())
        if '=' not in line:
            continue
        hanzi, pinyins = line.split('=')
        pinyins = pinyins.split(',')
        pinyins = [util.simplify_pinyin(py) for py in pinyins]
        for pinyin in pinyins:
            emission.setdefault(hanzi, {})
            emission[hanzi].setdefault(pinyin, 0)  # 不存在key=pinyin时，设置value=0
            emission[hanzi][pinyin] += 1


def read_from_sentence_txt(start, emission, transition):
    # ./result/sentence1.txt
    print('read from sentence.txt')
    for line in open(SENTENCE_FILE, encoding="utf-8"):
        line = util.as_text(line.strip())
        if len(line) < 2:
            continue
        if not util.is_chinese(line):
            continue
        # for start
        start.setdefault(line[0], 0)
        start[line[0]] += 1

        # for emission
        # 汉字句子变为拼音，
        pinyin_list = topinyin(line)
        char_list = [c for c in line]

        for hanzi, pinyin in zip(char_list, pinyin_list):
            emission.setdefault(hanzi, {})
            emission[hanzi].setdefault(pinyin, 0)
            emission[hanzi][pinyin] += 1

        # for transition
        """
            组成一个元表，（汉字，拼音）
            结构如下：
            {
               key:  汉字
               value:{
                    key：后面出现的汉字
                    value: 次数
                }
            }
        """
        """
         print(line)
         ziped=line[:-1], line[1:]
         print(list(ziped))
        人生何处不相逢
        ['人生何处不相', '生何处不相逢']
        人：生
        生：何
        ...
        """
        for f, t in zip(line[:-1], line[1:]):
            transition.setdefault(f, {})
            transition[f].setdefault(t, 0)
            transition[f][t] += 1


def gen_base():

    start = {}
    emission = {}
    transition = {}

    process_hanzipinyin(emission)
    read_from_sentence_txt(start, emission, transition)

    # write to file
    writejson2file(start, BASE_START)
    writejson2file(emission, BASE_EMISSION)
    writejson2file(transition, BASE_TRANSITION)


def main():
    gen_base()

if __name__ == '__main__':
    main()
