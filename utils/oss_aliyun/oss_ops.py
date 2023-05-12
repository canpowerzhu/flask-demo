# @Author  : kane.zhu
# @Time    : 2022/11/8 21:48
# @Software: PyCharm
# @Description:
import oss2
from settings.conf import PrdConfig


class OssOpsUpload():

    def __init__(self, bucket):
        self.bucket = bucket

    # 采用分片上传
    # headers无需设置
    def multi_upload(self, local_object, preferred_size, is_verification):
        upload_id = self.bucket.init_multipart_upload(local_object).upload_id

    # 进行断点续传
    def resume_upload(self,remote_object,local_object):
        """
        :param remote_object:  远端对象
        :param local_object: 本地需要上传的对象
        :return:
        """
        oss2.resumable_upload(self.bucket,remote_object,local_object,
                              multipart_threshold=PrdConfig.OSS_MULTI_THRESHOLD,
                              part_size=PrdConfig.OSS_PART_SIZE,
                              progress_callback=self.percentage,
                              num_threads=PrdConfig.OSS_NUM_THREADS)

    #普通上传
    def ordinary_upload(self):
        pass

    def percentage(self, consumed_bytes, total_bytes):
        import sys
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print('\r{0}% '.format(rate), end='')
            sys.stdout.flush()




def oss_upload():
    pass