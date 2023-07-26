# @Author  : kane.zhu
# @Time    : 2023/3/23 15:11
# @Software: PyCharm
# @Description:

from flask import Blueprint, jsonify, request

from log_settings import logger
from src.jenkins_bp.v1 import init_jenkins_object

jenkins_ops_bp = Blueprint('jenkins_ops_bp', __name__)
client = init_jenkins_object()


@jenkins_ops_bp.route("/get_jobs", methods=['GET'])
def jenkins_get_jenkins():
    jobs_list = client.get_jobs()
    logger.info("拉取同步jobs信息数量:{};详情是{}".format(len(jobs_list), jobs_list))
    return jsonify({"code": 200, "status": "success", "data": {"job_list": jobs_list, "job_count": len(jobs_list)}})


# 获取job的配置信息
@jenkins_ops_bp.route("/get_config/<job_name>", methods=['GET'])
def jenkins_get_job_config(job_name):
    try:
        jobs_config = client.get_job_config(job_name)
        status = "success"
    except Exception as e:
        jobs_config = str(e)
        status = "failed"
    return jsonify({"code": 200, "status": status, "data": {"job_name": job_name, "job_config": jobs_config}})


@jenkins_ops_bp.route("/build_job/<job_name>", methods=["POST"])
def jenkins_job_build(job_name):
    get_build_params = request.json
    print(get_build_params)

    try:
        build_info = client.build_job(job_name, get_build_params)
        status = "success"
        logger.info("构建任务{}----下发成功".format(job_name))
    except Exception as e:
        status = "failed"
        build_info = str(e)
        logger.error("构建任务{}失败----{}".format(job_name, str(e)))
    return jsonify({"code": 200, "status": status, "data": {"job_name": job_name, "build_info": build_info}})


@jenkins_ops_bp.route("/build_job/<job_name>/<last_build_number>")
def jenkins_job_build_info(job_name, last_build_number):
    build_info = client.get_build_info(job_name, int(last_build_number))

    return jsonify({"code": 200, "data": {"job_name": job_name, "build_info": build_info}})
