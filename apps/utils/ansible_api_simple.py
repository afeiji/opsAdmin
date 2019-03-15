#encoding:utf-8

from ansible import constants
from collections import namedtuple

# 用于读取yaml，json格式的文件
from ansible.parsing.dataloader import DataLoader
# 存储着角色列表，任务，处理代码块
from ansible.playbook.play import Play
# 用于创建和管理inventory，导入inventory文件
from ansible.inventory.manager import InventoryManager
# 用于管理变量的类，包括主机，组，扩展等变量
from ansible.vars.manager import VariableManager

# 执行playboy
from ansible.executor.playbook_executor import PlaybookExecutor
# ansible底层用到的任务队列
from ansible.executor.task_queue_manager import TaskQueueManager

# 回调基类，用来定义回调事件，比如返回失败成功等信息
from ansible.plugins.callback import CallbackBase

import json


class MyInventory:
    """
    Ansible Inventory
    """

    def __init__(self, resource):
        self.resource = resource
        self.loader = DataLoader()
        # ansible主机配置文件路径
        self.inventory = InventoryManager(loader=self.loader, sources=['/etc/ansible/hosts'])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)


class ModelResultsCollector(CallbackBase):
    """
    执行AD-HOC命令
    """
    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        print(result)
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        print(result)
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        print(result)
        self.host_failed[result._host.get_name()] = result


class PlayBookResultsCollector(CallbackBase):
    """
    执行playbook并返回结果
    """
    CALLBACK_VERSION = 2.0

    def __init__(self, *args, **kwargs):
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        print(result)
        self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        print(result)
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        print(result)
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()] = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                "ok": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }


class ANSRunner(object):
    """
    This is a General object for parallel execute modules.
    """

    def __init__(self, resource=None):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.passwords = None
        self.options = None
        self.callback = None
        self.__initializeData()
        self.results_raw = {}

    def __initializeData(self):
        """
        初始化ansible

        """
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                         'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                         'verbosity','check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])

        self.loader = DataLoader()
        self.options = Options(connection='smart', module_path=None, forks=5, timeout=10,
                               remote_user='vagrant', ask_pass=False, private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                               become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False, diff=True)

        myinventory = MyInventory(self.resource)
        self.inventory = myinventory.inventory
        self.variable_manager = myinventory.variable_manager

    def run_model(self, host_list, module_name, module_args):
        """
        run module from andible ad-hoc.
        module_name: ansible module_name
        module_args: ansible module args
        """
        play_source = dict(
            name = "Ansible Play",
            hosts = host_list,
            gather_facts = 'no',
            tasks = [dict(action=dict(module=module_name, args=module_args))]
        )

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        self.callback = ModelResultsCollector()
        import traceback
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback="minimal",
            )
            tqm._stdout_callback = self.callback
            constants.HOST_KEY_CHECKING = False
            tqm.run(play)
        except Exception as err:
            print(traceback.print_exc())
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, playbook_path, extra_vars=None):
        """
        运行playbook
        """
        try:
            self.callback = PlayBookResultsCollector()
            if extra_vars:
                self.variable_manager.extra_vars = extra_vars
            executor = PlaybookExecutor(
                playbooks=[playbook_path], inventory=self.inventory, variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options, passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.callback
            constants.HOST_KEY_CHECKING = False
            executor.run()
        except Exception as err:
            return False

    def get_model_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['success'][hostvisiable] = result._result

        for host, result in self.callback.host_failed.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['failed'][hostvisiable] = result._result

        for host, result in self.callback.host_unreachable.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['unreachable'][hostvisiable] = result._result

        return self.results_raw

    def get_playbook_result(self):
        self.results_raw = {'skipped': {}, 'failed': {}, 'ok': {}, "status": {}, 'unreachable': {}, "changed": {}}
        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result._result

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result._result

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result._result
        return self.results_raw


if __name__ == '__main__':
    rbt = ANSRunner()
    rbt.run_playbook(playbook_path='/vagrant/devops/playbook/19/02/play.yaml')
    result = json.dumps(rbt.get_playbook_result(), indent=4)
    # rbt.run_model("all", 'shell', 'uptime')
    # result = json.dumps(rbt.get_model_result(), indent=4)
    print(result)
