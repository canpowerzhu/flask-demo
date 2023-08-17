# @Author  : kane.zhu
# @Time    : 2023/8/15 21:45
# @Software: PyCharm
# @Description:

from xpinyin import Pinyin


# 初始化拼音对象

def words_transfer_to_letter(words: str) -> str:
    """
    将汉字转换为以_拼接的全拼大写字母
    例如：你好-> NI_HAO
    :param words:
    :return:
    """
    P = Pinyin()
    r = P.get_pinyin(words)
    result = '_'.join(i.upper() for i in r.split('-'))
    return result

# print(words_transfer_to_letter("销售宝"))
