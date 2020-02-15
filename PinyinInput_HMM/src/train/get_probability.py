# coding: utf-8
"""
根据 pinyin2hanzi.txt 和步骤四输出的三个文件，统计计算得到模型对应的两个矩阵和
一个向量，以及某个拼音（符号）对应的所有汉字（状态）；
"""
import json
from src import util

SOURCE_FILE = '../../data/data2/hanzipinyin.txt'
BASE_START_FILE = '../../result/base_start.txt'
BASE_EMISSION_FILE = '../../result/base_emission.txt'
BASE_TRANSITION_FILE = '../../result/base_transition.txt'

ALL_STATES_FILE = '../../result/all_states.txt'  # 所有的字
ALL_OBSERVATIONS_FILE = '../../result/all_observations.txt'  # 所有的拼音
PY2HZ_FILE = '../../result/pinyin2hanzi.txt'  # 一个拼音对应的所有汉字

HZ2PY_FILE = '../../data/data2/hanzipinyin.txt'

FIN_PY2HZ_FILE = '../hmm/data/hmm_py2hz.txt'  # 将 pinyin2hanzi.txt 中的无效行去掉；
FIN_START_FILE = '../hmm/data/hmm_start.txt'  # 将 base_start.txt中的次数转换为频率；
FIN_EMISSION_FILE = '../hmm/data/hmm_emission.txt'  # 将 base_emission.txt 中的次数转换为频率；
FIN_TRANSITION_FILE = '../hmm/data/hmm_transition.txt'  # 将 base_transition.txt 中的次数转换为频率；

PINYIN_NUM = 411.    # 所有的拼音的数目
HANZI_NUM = 20903.   # 所有的汉字个数


# 写入
def writejson2file(obj, filename):
    with open(filename, 'w') as outfile:
        data = json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(data)

# 读取
def readdatafromfile(filename):
    with open(filename, encoding="gbk") as outfile:
        return json.load(outfile)


# 将无效行去掉
def gen_py2hz():
    data = {}
    for line in open(PY2HZ_FILE):
        line = util.as_text(line.strip())
        ls = line.split('=')
        if len(ls) != 2:
            raise Exception('错误')
        py, chars = ls
        py = py.strip()  # 拼音
        chars = chars.strip()  # 对应的汉字
        if len(py) > 0 and len(chars) > 0:
            data[py] = chars
    writejson2file(data, FIN_PY2HZ_FILE)

# 将base_start.json 中的次数转换为频率；
def gen_start():
    data = {'default': 1, 'data': None}  # 数据基本结构

    start = readdatafromfile(BASE_START_FILE)
    count = HANZI_NUM
    # 计算总基数时，所有的汉字都计为1，在语料库中的的按找其出现次数再相加
    for hanzi in start:
        count += start[hanzi]

    print(count)
    # 计算语料库中出现的和汉字的概率
    for hanzi in start:
        start[hanzi] = start[hanzi] / count

    data['default'] = 1.0 / count
    data['data'] = start
    writejson2file(data, FIN_START_FILE)

# 将 base_emission.json 中一个汉字的各个拼音的次数转换为频率；
def gen_emission():
    data = {'default': 1.e-200, 'data': None}
    emission = readdatafromfile(BASE_EMISSION_FILE)

    for line in open(SOURCE_FILE, encoding="utf-8"):
        line = util.as_text(line.strip())
        hanzi, pinyin_list = line.split('=')
        # 一个汉字对应的所有拼音
        pinyin_list = [util.simplify_pinyin(item.strip()) for item in pinyin_list.split(',')]
        # 将汉字数目和拼音数目一致
        char_list = [hanzi] * len(pinyin_list)
        # 组成元组
        for hanzi, pinyin in zip(char_list, pinyin_list):
            emission.setdefault(hanzi, {})
            emission[hanzi].setdefault(pinyin, 0.)
            emission[hanzi][pinyin] += 1.

    for hanzi in emission:
        num_sum = 0.
        # 一个汉字的拼音总共出现的次数
        for pinyin in emission[hanzi]:
            num_sum += emission[hanzi][pinyin]
        # 算出一个汉字的拼音的概率
        for pinyin in emission[hanzi]:
            emission[hanzi][pinyin] = emission[hanzi][pinyin] / num_sum

    data['data'] = emission
    writejson2file(data, FIN_EMISSION_FILE)


# 将 base_transition.json 中的次数转换为频率；一个汉字后面出现另外一个汉字的概率
def gen_tramsition():
    data = {'default': 1. / HANZI_NUM, 'data': None}
    transition = readdatafromfile(BASE_TRANSITION_FILE)
    for c1 in transition:
        num_sum = HANZI_NUM  # 默认每个字都有机会
        # 基数
        for c2 in transition[c1]:
            num_sum += transition[c1][c2]

        for c2 in transition[c1]:
            transition[c1][c2] = float(transition[c1][c2] + 1) / num_sum
        transition[c1]['default'] = 1. / num_sum

    data['data'] = transition
    writejson2file(data, FIN_TRANSITION_FILE)


def main():
    gen_py2hz()
    gen_start()
    gen_emission()
    gen_tramsition()


if __name__ == '__main__':
    main()
