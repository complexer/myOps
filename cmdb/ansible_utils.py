import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import ansible.constants as C


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result



class MyInventory(InventoryManager):
    """
    用于动态生成Inventory的类.
    """

    def __init__(self, loader, resource=None, sources=None):
        """
        resource的数据格式是一个列表字典，比如
            {
                "group1": {
                    "hosts": [{"ip": "10.0.0.0", "port": "22", "username": "test", "password": "pass"}, ...],
                    "group_vars": {"var1": value1, "var2": value2, ...}
                }
            }
             如果你只传入1个列表，这默认该列表内的所有主机属于default 组,比如
            [{"ip": "10.0.0.0", "port": "22", "username": "test", "password": "pass"}, ...]
        sources是原生的方法，参数是配置的inventory文件路径，可以指定一个，也可以以列表的形式可以指定多个
        """
        super(MyInventory, self).__init__(loader=loader, sources=sources)
        self.resource = resource
        self.dynamic_inventory()

    def add_dynamic_group(self, hosts, group_name, group_vars=None):
        """
        将从数据库读取的组信息，主机信息等生成的resource信息解析成ansible可以读取的内容
        :param hosts: 包含主机所有信息的的列表
        :type hosts: list
        :param group_name:
        :param group_vars:
        :type group_vars: dict
        :return:
        """
        # 添加主机组
        self.add_group(group_name)

        # 添加主机组变量
        if group_vars:
            for key, value in group_vars.items():
                self.groups[group_name].set_variable(key, value)

        for host in hosts:
            ip = host.get('ip')
            port = host.get('port')

            # 添加主机到主机组
            self.add_host(ip, group_name, port)

            username = host.get('username')
            password = host.get('password')

            # 生成ansible主机变量
            self.get_host(ip).set_variable('ansible_ssh_host', ip)
            self.get_host(ip).set_variable('ansible_ssh_port', port)
            self.get_host(ip).set_variable('ansible_ssh_user', username)
            self.get_host(ip).set_variable('ansible_ssh_pass', password)
            self.get_host(ip).set_variable('ansible_sudo_pass', password)

            # 如果使用同一个密钥管理所有机器，只需把下方的注释去掉，ssh_key指定密钥文件，若是不同主机使用不同密钥管理，则需要单独设置主机变量或组变量
            # self.get_host(ip).set_variable('ansible_ssh_private_key_file', ssh_key)

            # set other variables
            for key, value in host.items():
                if key not in ["ip", "port", "username", "password"]:
                    self.get_host(ip).set_variable(key, value)

    def dynamic_inventory(self):
        if isinstance(self.resource, list):
            self.add_dynamic_group(self.resource, 'default')
        elif isinstance(self.resource, dict):
            for groupname, hosts_and_vars in self.resource.items():
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("group_vars"))



class AnsibleApi(object):
    def __init__(self, resource=None, sources=None):
        self.Options = namedtuple('Options',
                                  ['connection',
                                   'remote_user',
                                   'ask_sudo_pass',
                                   'verbosity',
                                   'ack_pass',
                                   'module_path',
                                   'forks',
                                   'become',
                                   'become_method',
                                   'become_user',
                                   'check',
                                   'listhosts',
                                   'listtasks',
                                   'listtags',
                                   'syntax',
                                   'sudo_user',
                                   'sudo',
                                   'diff'])

        self.ops = self.Options(connection='smart',
                                remote_user=None,
                                ack_pass=None,
                                sudo_user=None,
                                forks=5,
                                sudo=None,
                                ask_sudo_pass=False,
                                verbosity=5,
                                module_path=None,
                                become=None,
                                become_method=None,
                                become_user=None,
                                check=False,
                                diff=False,
                                listhosts=None,
                                listtasks=None,
                                listtags=None,
                                syntax=None)

        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        # self.inventory = InventoryManager(loader=self.loader, sources=['/etc/ansible/hosts'])
        self.inventory = MyInventory(resource=resource, loader=self.loader, sources=sources)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def runansible(self, host_list, task_list):

        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.ops,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreachable'] = {}

        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = json.dumps(result._result)

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result['msg']

        print(results_raw)
        return results_raw

    def runplaybook(self, playbook_path):

        self.variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes'}
        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.ops, passwords=self.passwords)
        result = playbook.run()
        return result


if __name__ == "__main__":
    resource = [{"ip": "192.168.34.20", "port": "22", "username": "root", "password": "111111"}]
    a = AnsibleApi(resource=resource)
    host_list = ['192.168.34.20']
    tasks_list = [
        # dict(action=dict(module='command', args='ls')),
        dict(action=dict(module='setup')),
        # dict(action=dict(module='shell', args='python sleep.py')),
        # dict(action=dict(module='synchronize', args='src=/home/op/test dest=/home/op/ delete=yes')),
    ]
    res = a.runansible(host_list, tasks_list)
    exit()
    # a.runplaybook(playbook_path=['/etc/ansible/test.yml'])
    for k, v in res:
        if k == "success":
            pass
        elif k == "failed":
            pass
        elif k == "unreachable":
            pass

