# @Author  : kane.zhu
# @Time    : 2022/11/8 21:48
# @Software: PyCharm
# @Description:
import base64
import json

import oss2
from settings.conf import PrdConfig
from utils.aliyun_cloud import access_key_id, access_key_secret, bucket_name


class OssOpsUpload():

    def __init__(self, bucket_name,project_name):
        """
        :param bucket_name: 需要操作的Bucket名称
        :param project_name: 来源子系统的名称
        """
        self.bucketName = bucket_name
        self.projectName = project_name

    @staticmethod
    def create_oss_client(self):
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, bucket_name)
        return bucket

    @staticmethod
    # 定义回调参数Base64编码函数。
    def encode_callback(callback_params):
        cb_str = json.dumps(callback_params).strip()
        return oss2.compat.to_string(base64.b64encode(oss2.compat.to_bytes(cb_str)))

    @staticmethod
    # 上传回调相关
    def upload_callback(self, callback_url: str, project_name: str) -> dict:
        callback_params = {
            'callbackUrl': callback_url,
            'callbackBody': 'bucket=${bucket}&object=${object}',
            'callbackBodyType': 'application/x-www-form-urlencoded'
        }
        encoded_callback = self.encode_callback(callback_params)

        callback_var_params = {'x:projectName': project_name}
        encoded_callback_var = self.encode_callback(callback_var_params)

        return {'x-oss-callback': encoded_callback, 'x-oss-callback-var': encoded_callback_var}

    # 采用分片上传
    # headers无需设置
    def multi_upload(self, local_object, preferred_size, is_verification):
        upload_id = self.bucket.init_multipart_upload(local_object).upload_id

    # 进行断点续传
    def resume_upload(self, remote_object, local_object):
        """
        :param remote_object:  远端对象
        :param local_object: 本地需要上传的对象
        :return:
        """
        oss2.resumable_upload(self.bucket, remote_object, local_object,
                              multipart_threshold=PrdConfig.OSS_MULTI_THRESHOLD,
                              part_size=PrdConfig.OSS_PART_SIZE,
                              progress_callback=self.percentage,
                              # 如果使用num_threads设置并发上传线程数，
                              # 请将oss2.defaults.connection_pool_size设置为大于或等于并发上传线程数。
                              # 默认并发上传线程数为1。
                              num_threads=PrdConfig.OSS_NUM_THREADS)

    # 普通上传
    ## 普通上传 字符串模式
    def ordinary_upload_string(self, upload_string_obj: str, object_full_path: str):
        bucket = OssOpsUpload.create_oss_client()
        bucket.put_object(object_full_path, upload_string_obj)

    ## 普通上传 Stream模式
    def ordinary_upload_stream(self, file, oss_file_path: str, **kwargs):
        callback_url = kwargs.get("callback_url")


        # 是否进行回调的流式上传
        params_obj = None if callback_url is None else self.upload_callback(callback_url,self.projectName)

        bucket = OssOpsUpload.create_oss_client()
        try:
            bucket.put_object(oss_file_path, file, progress_callback=self.percentage,params=params_obj)
        except Exception as err:
            return False, err
        return True, oss_file_path


    def percentage(self, consumed_bytes, total_bytes):
        import sys
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print('\r{0}% '.format(rate), end='')
            sys.stdout.flush()
