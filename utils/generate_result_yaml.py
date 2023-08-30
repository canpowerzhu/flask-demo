# @Author  : kane.zhu
# @Time    : 2023/8/23 14:19
# @Software: PyCharm
# @Description:
import yaml
from dao.ops_db_config_info import get_sys_config_list
from log_settings import logger


def get_sys_config():
    status,res = get_sys_config_list(config_group='DEPLOY')
    final_dict = {}
    if not status:
        logger.error("查询发布信息的配置项异常：{}".format(res))
    logger.info("查询发布信息的配置是{},类型是{}".format(res, type(res)))
    for item in res:
        if item['config_key'] == 'JAVA_PACKAGE_PATH':
            final_dict['JAVA_PACKAGE_PATH'] = item['config_value']

        if item['config_key'] == 'OSS_DOMAIN_ACC':
            final_dict['OSS_ACCESS_DOMAIN'] = item['config_value']

        if item['config_key'] == 'BASE_IMAGE_FOR_JAVA':
            final_dict['BASE_IMAGE_FOR_JAVA'] = item['config_value']
    return final_dict


def transfer_containers_port(my_ports: dict) -> list:
    return ['{}/{}:{}/{}'.format(k, v, k, v) for k, v in my_ports.items()] if bool(my_ports) else []

def transfer_containers_volumes(my_volumes: dict) -> list:
    return ['{}:{}'.format(k, v) for k, v in my_volumes.items()] if bool(my_volumes) else []



class MakeModuleYaml():
    def __init__(self,project_module_mixed:dict):
        self.JAVA_PACKAGE_PATH = get_sys_config()['JAVA_PACKAGE_PATH']
        self.OSS_ACCESS_DOMAIN = get_sys_config()['OSS_ACCESS_DOMAIN']
        self.base_image_name = project_module_mixed['base_image_name']
        self.image_name = '{}:{}'.format(get_sys_config()['BASE_IMAGE_FOR_JAVA'], self.base_image_name)
        self.project_code = project_module_mixed['project_code']
        self.health_check_interval = project_module_mixed['health_check_interval']
        self.health_check_timeout = project_module_mixed['health_check_timeout']
        self.health_check_retries = project_module_mixed['health_check_retries']
        self.health_check_start_period = project_module_mixed['health_check_start_period']

        # module_info表
        self.module_name = project_module_mixed['module_name']
        self.module_package_name = project_module_mixed['module_package_name']
        self.my_hosts_dict = project_module_mixed['module_host_pairs']
        self.my_volumes_dict =  transfer_containers_volumes(project_module_mixed['module_volumes_pairs'])
        self.my_env_dict = project_module_mixed['module_env_pairs']
        self.my_ports_dict =  transfer_containers_port(project_module_mixed['module_port_pairs'])
        self.module_memory = project_module_mixed['module_memory']
        self.debug_status = project_module_mixed['debug_status']
        self.debug_status_port = project_module_mixed['debug_status_port']
        self.dump_oom_status = project_module_mixed['dump_oom_status']
        self.dump_oom_path = project_module_mixed['dump_oom_path']
        self.start_define_params = project_module_mixed['start_define_params']
        # self.my_entrypoint = project_module_mixed['start_define_params']

    def combine_entrypoint(self) -> list:
        my_entrypoint = ['java', '-server', '-Xmx{}m'.format(self.module_memory), '-Xms{}m'.format(self.module_memory)]
        if self.debug_status:
            my_entrypoint.append(
                '-agentlib:jdwp=transport=dt_socket,address={},server=y,suspend=n'.format(self.debug_status_port))

        if self.dump_oom_status:
            my_entrypoint.append('-XX:+HeapDumpOnOutOfMemoryError  -XX:HeapDumpPath={}'.format(self.dump_oom_path))
        # 如果自定义启动参数不为空则需要拼接
        # {"file.encoding":"UTF-8"}  拼接成"-Dfile.encoding=UTF-8”
        # print(self.start_define_params)
        if  self.start_define_params is not None:
            for k, v in self.start_define_params.items():
                my_entrypoint.append('-D{}={}'.format(k, v))

        my_entrypoint.append('-jar')
        my_entrypoint.append('/mnt/{}'.format(self.module_package_name))

        return my_entrypoint


    def make_yaml(self):
        playbook_data = {
            'name': self.module_name,
            'hosts': '{{ dest_host }}',
            'tasks': [
                {
                    'name': 'check folder {}  status'.format(self.module_name),
                    'file': {
                        'path': "{}/{}/{}/logs".format(self.JAVA_PACKAGE_PATH, self.project_code, self.module_name),
                        'state': 'directory',
                        'owner': 'root',
                        'group': 'root',
                        'mode': '0644',
                        'recurse': True
                    }
                },
                {
                    'name': 'create docker network if not exists',
                    'docker_network': {
                        'name': self.project_code,
                        'ignore_errors': True
                    }
                },
                {
                    'name': 'download jar package',
                    'get_url': {
                        # 这里的jar包的地址 由参数传入
                        'url': '{}/{}'.format(self.OSS_ACCESS_DOMAIN,'{{ module_package_url }}'),
                        'dest': '{}/{}/{}'.format(self.JAVA_PACKAGE_PATH, self.project_code, self.module_name),
                        'mode': '0644',
                        'force': True
                    }
                },
                {
                    'name': 'create container: {}'.format(self.module_name),
                    'docker_container': {
                        'name': self.module_name,
                        'image': self.image_name,
                        'restart_policy': 'always',
                        'networks_cli_compatible': True,
                        'dns_servers': '223.6.6.6',
                        'networks': {
                            'name': self.project_code
                        },
                        'etc_hosts': self.my_hosts_dict,
                        'volumes': self.my_volumes_dict,
                        'env': self.my_env_dict,
                        'ports': self.my_ports_dict,
                        'tty': True,
                        'log_driver': 'json-file',
                        'log_options': {
                            'tag': self.module_name
                        },
                        'entrypoint': self.combine_entrypoint(),
                        'healthcheck': {
                            'interval': '{}s'.format(self.health_check_interval),
                            'start_period': '{}s'.format(self.health_check_start_period),
                            'retries': self.health_check_retries,
                            'timeout': '{}s'.format(self.health_check_timeout)
                        }

                    }
                }
            ]
        }
        playbook_yaml = yaml.dump([playbook_data], default_flow_style=False)
        return playbook_yaml

















