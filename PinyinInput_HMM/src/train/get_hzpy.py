# coding: utf-8
# 功能：统计 hanzipinyin.txt 中出现的所有汉字、拼音、每个拼音对应的所有汉字；

from src import util


SOURCE_FILE = '../../data/data2/hanzipinyin.txt'
ALL_STATES_FILE = '../../result/all_states.txt'  # 汉字（隐藏状态）
ALL_OBSERVATIONS_FILE = '../../result/all_observations.txt'  # 拼音（观测值）
PINYIN2HANZI_FILE = '../../result/pinyin2hanzi.txt'  # 每个拼音对应的所有汉字

states = set()
observations = set()
py2hz = {}

for line in open(SOURCE_FILE, encoding="utf-8"):
    # line = util.as_text(line.strip())
    hanzi, pinyin_list = line.split('=')
    pinyin_list = [util.simplify_pinyin(item.strip()) for item in pinyin_list.split(',')]
    states.add(hanzi)

    for pinyin in pinyin_list:
        observations.add(pinyin)
        py2hz.setdefault(pinyin, set())   # 将这个set的value设置成set()结构
        py2hz[pinyin].add(hanzi)   # 在后面添加汉字
        # 声母
        shengmu = util.get_shengmu(pinyin)
        if shengmu is not None:
            py2hz.setdefault(shengmu, set())
            py2hz[shengmu].add(hanzi)

# 汉字
with open(ALL_STATES_FILE, 'w') as out:
    s = '\n'.join(states)
    out.write(s)

# 拼音
with open(ALL_OBSERVATIONS_FILE, 'w') as out:
    s = '\n'.join(observations)
    out.write(s)

# 每个拼音对应的汉字
with open(PINYIN2HANZI_FILE, 'w') as out:
    s = ''
    for k in py2hz:
        s = s + k + '=' + ''.join(py2hz[k]) + '\n'
    out.write(s)

print('end')
