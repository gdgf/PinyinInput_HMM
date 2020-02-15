# coding: utf-8

import os


# 生成unicode字符串
def as_text(v):
    if v is None:
        return None
    elif isinstance(v, bytes):
        # 将utf-8 的v变成unicode字符返回
        return v.decode('utf-8', errors='ignore')
    elif isinstance(v, str):
        return v
    else:
        raise ValueError('Unknown type %r' % type(v))

def is_text(v):
    return isinstance(v, str)  # 判断v是str类型吗？

# 判断字符串是汉语
def is_chinese(v):
    if is_text(v):
        if len(v) == 0:
            return False
        # 汉字编码u4e00-u9fff
        # 所有字符都是中文返回true
        return all(u'\u4e00' <= c <= u'\u9fff' or c == u'〇' for c in v)
    else:
        raise ValueError('Invalid type %r' % type(v))

# 目前文件的目录
def current_dir():
    # os.path.realpath(__file__)：返回__file__的真实路径
    # os.path.dirname()返回文件路径
    return os.path.dirname(os.path.realpath(__file__))

# 拼英对应的声调
__removetone_dict = {
    'ā': 'a',
    'á': 'a',
    'ǎ': 'a',
    'à': 'a',
    'ē': 'e',
    'é': 'e',
    'ě': 'e',
    'è': 'e',
    'ī': 'i',
    'í': 'i',
    'ǐ': 'i',
    'ì': 'i',
    'ō': 'o',
    'ó': 'o',
    'ǒ': 'o',
    'ò': 'o',
    'ū': 'u',
    'ú': 'u',
    'ǔ': 'u',
    'ù': 'u',
    'ü': 'v',
    'ǖ': 'v',
    'ǘ': 'v',
    'ǚ': 'v',
    'ǜ': 'v',
    'ń': 'n',
    'ň': 'n',
    '': 'm',
}


def remove_tone(one_py):
    """ 删除拼音中的音调
    lǔ -> lu
    """
    one_py = as_text(one_py)
    r = as_text('')
    for c in one_py:
        if c in __removetone_dict:
            r += __removetone_dict[c]
        else:
            r += c
    return r

def normlize_pinyin(one_py):
    """ 规范化
    ue -> ve
    """
    if 'ue' in one_py:
        return one_py.replace('ue', 've')
    if 'ng' == one_py:  # 嗯
        return 'en'
    return one_py



# 简化拼英
def simplify_pinyin(one_py):
    # 小写、去掉声调、规范化
    return normlize_pinyin(remove_tone(one_py.lower()))


# 拼音
__pinyin = {'gu', 'qiao', 'qian', 'qve', 'ge', 'gang', 'ga', 'lian', 'liao', 'rou', 'zong', 'tu', 'seng', 'yve', 'ti',
            'te', 'jve', 'ta', 'nong', 'zhang', 'fan', 'ma', 'gua', 'die', 'gui', 'guo', 'gun', 'sang', 'diu', 'zi',
            'ze', 'za', 'chen', 'zu', 'ba', 'dian', 'diao', 'nei', 'suo', 'sun', 'zhao', 'sui', 'kuo', 'kun', 'kui',
            'cao', 'zuan', 'kua', 'den', 'lei', 'neng', 'men', 'mei', 'tiao', 'geng', 'chang', 'cha', 'che', 'fen',
            'chi', 'fei', 'chu', 'shui', 'me', 'tuan', 'mo', 'mi', 'mu', 'dei', 'cai', 'zhan', 'zhai', 'can', 'ning',
            'wang', 'pie', 'beng', 'zhuang', 'tan', 'tao', 'tai', 'song', 'ping', 'hou', 'cuan', 'lan', 'lao', 'fu',
            'fa', 'jiong', 'mai', 'xiang', 'mao', 'man', 'a', 'jiang', 'zun', 'bing', 'su', 'si', 'sa', 'se', 'ding',
            'xuan', 'zei', 'zen', 'kong', 'pang', 'jie', 'jia', 'jin', 'lo', 'lai', 'li', 'peng', 'jiu', 'yi', 'yo',
            'ya', 'cen', 'dan', 'dao', 'ye', 'dai', 'zhen', 'bang', 'nou', 'yu', 'weng', 'en', 'ei', 'kang', 'dia',
            'er', 'ru', 'keng', 're', 'ren', 'gou', 'ri', 'tian', 'qi', 'shua', 'shun', 'shuo', 'qun', 'yun', 'xun',
            'fiao', 'zan', 'zao', 'rang', 'xi', 'yong', 'zai', 'guan', 'guai', 'dong', 'kuai', 'ying', 'kuan', 'xu',
            'xia', 'xie', 'yin', 'rong', 'xin', 'tou', 'nian', 'niao', 'xiu', 'fo', 'kou', 'niang', 'hua', 'hun', 'huo',
            'hui', 'shuan', 'quan', 'shuai', 'chong', 'bei', 'ben', 'kuang', 'dang', 'sai', 'ang', 'sao', 'san', 'reng',
            'ran', 'rao', 'ming', 'null', 'lie', 'lia', 'min', 'pa', 'lin', 'mian', 'mie', 'liu', 'zou', 'miu', 'nen',
            'kai', 'kao', 'kan', 'ka', 'ke', 'yang', 'ku', 'deng', 'dou', 'shou', 'chuang', 'nang', 'feng', 'meng',
            'cheng', 'di', 'de', 'da', 'bao', 'gei', 'du', 'gen', 'qu', 'shu', 'sha', 'she', 'ban', 'shi', 'bai', 'nun',
            'nuo', 'sen', 'lve', 'kei', 'fang', 'teng', 'xve', 'lun', 'luo', 'ken', 'wa', 'wo', 'ju', 'tui', 'wu', 'le',
            'ji', 'huang', 'tuo', 'cou', 'la', 'mang', 'ci', 'tun', 'tong', 'ca', 'pou', 'ce', 'gong', 'cu', 'lv',
            'dun', 'pu', 'ting', 'qie', 'yao', 'lu', 'pi', 'po', 'suan', 'chua', 'chun', 'chan', 'chui', 'gao', 'gan',
            'zeng', 'gai', 'xiong', 'tang', 'pian', 'piao', 'cang', 'heng', 'xian', 'xiao', 'bian', 'biao', 'zhua',
            'duan', 'cong', 'zhui', 'zhuo', 'zhun', 'hong', 'shuang', 'juan', 'zhei', 'pai', 'shai', 'shan', 'shao',
            'pan', 'pao', 'nin', 'hang', 'nie', 'zhuai', 'zhuan', 'yuan', 'niu', 'na', 'miao', 'guang', 'ne', 'hai',
            'han', 'hao', 'wei', 'wen', 'ruan', 'cuo', 'cun', 'cui', 'bin', 'bie', 'mou', 'nve', 'shen', 'shei', 'fou',
            'xing', 'qiang', 'nuan', 'pen', 'pei', 'rui', 'run', 'ruo', 'sheng', 'dui', 'bo', 'bi', 'bu', 'chuan',
            'qing', 'chuai', 'duo', 'o', 'chou', 'ou', 'zui', 'luan', 'zuo', 'jian', 'jiao', 'sou', 'wan', 'jing',
            'qiong', 'wai', 'long', 'yan', 'liang', 'lou', 'huan', 'hen', 'hei', 'huai', 'shang', 'jun', 'hu', 'ling',
            'ha', 'he', 'zhu', 'ceng', 'zha', 'zhe', 'zhi', 'qin', 'pin', 'ai', 'chai', 'qia', 'chao', 'ao', 'an',
            'qiu', 'ni', 'zhong', 'zang', 'nai', 'nan', 'nao', 'chuo', 'tie', 'you', 'nu', 'nv', 'zheng', 'leng',
            'zhou', 'lang', 'e'}

# 声母
__shengmu = {'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's'}
# 韵母
__single_yunmu = {'a', 'o', 'e', 'i', 'u', 'v'}
__complex_yunmu = {'ai', 'ei', 'ui', 'ao', 'ou', 'iu', 'ie', 've', 'er', 'an', 'en', 'in', 'un', 'ang', 'eng', 'ing',
                   'ong'}

# 判断是否是拼英
def is_pinyin(v):
    return v in __pinyin

#  返回素有的拼英
def all_pinyin():
    for _ in __pinyin:
        yield _

# 判断是声母吗
def is_shengmu(v):
    return v in __shengmu

# 是简单的韵母吗
def is_single_yunmu(v):
    return v in __single_yunmu

# 是复杂的韵母吗
def is_complex_yunmu(v):
    return v in __complex_yunmu

# 是韵母吗
def is_yunmu(v):
    return is_single_yunmu(v) or is_complex_yunmu(v)

# 得到一个拼英中的声母
def get_shengmu(one_py):
    if len(one_py) == 0:
        return None
    elif len(one_py) == 1:
        if is_shengmu(one_py):
            return one_py
        else:
            return None
    else:
        if is_shengmu(one_py[:2]):
            return one_py[:2]
        elif is_shengmu(one_py[:1]):
            return one_py[:1]
        else:
            return None
