# coding: utf-8
from src.hmm.priorityset import PrioritySet
from .hmm_interface import AbstractHmmParams
import math


def viterbi(hmm_params, observations, path_num=8, min_prob=3.14e-200):

    V = [{}]
    t = 0
    cur_obs = observations[t]  # 拼音

    cur_states = hmm_params.get_states(cur_obs)  # 汉字
    for state in cur_states:

        # 以 每一个汉字的概率+这个汉字对应这个拼音的概率  作为评估值
        __score = (max(hmm_params.start(state), min_prob)) + \
                  (max(hmm_params.emission(state, cur_obs), min_prob))
        __path = [state]

        V[0].setdefault(state, PrioritySet(path_num))  # 设置结构，并得到每一组的的前6个
        V[0][state].put(__score, __path)
        # print(V)

    for t in range(1, len(observations)):
        cur_obs = observations[t]

        if len(V) == 2:
            V = [V[-1]]
        V.append({})

        prev_states = cur_states  # 上一个拼音对应的汉字
        cur_states = hmm_params.get_states(cur_obs)  # 现在拼音对应的汉字

        for y in cur_states:  # 拼音对应的每一个汉字
            V[1].setdefault( y, PrioritySet(path_num) )   # 设置结构，并得到当前组的前6个
            for y0 in prev_states:  # 上一个拼音汉字
                for item in V[0][y0]:
                    # 评分：上一个汉字到当前汉字的概率+转移概率+ 当前汉字出现的概率
                    _s = item.score + \
                         (max(hmm_params.transition(y0, y), min_prob)) + \
                         (max(hmm_params.emission(y, cur_obs), min_prob))
                    _p = item.path + [y]
                    V[1][y].put(_s, _p)

   # print("----------------------------------------------")
    result = PrioritySet(path_num)
    #print(V[-1])
    for last_state in V[-1]:
        for item in V[-1][last_state]:
            result.put(item.score, item.path)
    #print(result)
    result = [item for item in result]
    # print(result)
    # 按照结果排序
    result=sorted(result, key=lambda item: item.score, reverse=True)
    #print(result)
    return result