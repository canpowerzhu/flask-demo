# @Author  : kane.zhu
# @Time    : 2022/11/8 21:48
# @Software: PyCharm
# @Description:


class OssOpsUpload():

    def __init__(self, bucket):
        self.bucket = bucket

    # 采用分片上传
    def multi_upload(self, filename, preferred_size, is_verification):

        pass

    def resume_upload(self):
        pass


