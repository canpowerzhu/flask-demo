# @Author  : kane.zhu
# @Time    : 2023/8/30 14:42
# @Software: PyCharm
# @Description:

import hashlib


def calculate_md5(input_str):
    md5_hash = hashlib.md5()
    md5_hash.update(input_str.encode())
    return md5_hash.hexdigest()