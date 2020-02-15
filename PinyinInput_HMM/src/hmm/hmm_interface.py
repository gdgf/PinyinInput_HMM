# coding: utf-8
class AbstractHmmParams(object):

    def start(self, state):
        """
         得到初始状态（汉字的概率）
        """
        pass

    def emission(self, state, observation):
        """
        得到汉字到拼音的概率
        """
        pass

    def transition(self, from_state, to_state):
        """
        得到上一个汉字到当前汉字转移概率
        """
        pass

    def get_states(self, observation):
        """
        得到当前观测值（拼音）的状态值（汉字）
        """
        pass

