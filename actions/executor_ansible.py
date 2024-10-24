import ansible_runner
from configparser import ConfigParser
# from conf.logger import ansible_logger


class AnsibleRunner():

    def __init__(self, host_pattern='', limit=None):
        self.data_dir = '/home/public/.ansible/runner_data'
        self.inventory_path = '/home/public/.ansible/runner_data/inventory/hosts'
        self.host_pattern = host_pattern
        self.limit = limit

    def init_hosts(self):
        config = ConfigParser(allow_no_value=True)
        config.read(self.inventory_path)
        if not config.has_section(self.host_pattern):
            config.add_section(self.host_pattern)
        for host in self.limit.rstrip(',').split(','):
            if not config.has_option(self.host_pattern, host):
                config.set(self.host_pattern, host)

    def run_module(self, module, module_args, extravars=None):
        self.init_hosts()
        r = ansible_runner.run(private_data_dir=self.data_dir,
                               host_pattern=self.host_pattern, module=module,
                               module_args=module_args, limit=self.limit, extravars=extravars, quiet=True)

        # ansible_logger.info(
        #     f"执行完成！{self.host_pattern}, {module}, {module_args}, {self.limit}")
        result = self.parse_result(r)
        return result

    def parse_result(self, r):
        result = {}
        event_type_list = ['runner_on_ok', 'runner_on_failed',
                           'runner_on_unreachable', 'runner_on_skipped']
        for host in self.limit.rstrip(',').split(','):
            host_event = list(filter(
                lambda x: x['event'] in event_type_list, r.host_events(host)))
            event_res = host_event[0].get('event_data').get('res')
            single_host_res = {}
            if host_event[0].get('event') == 'runner_on_ok':
                single_host_res.update({'status': 'ok', 'data': event_res})
            if host_event[0].get('event') == 'runner_on_failed':
                single_host_res.update({'status': 'failed', 'data': event_res})
            if host_event[0].get('event') == 'runner_on_unreachable':
                single_host_res.update(
                    {'status': 'unreachable', 'msg': '主机不可达'})
            if host_event[0].get('event') == 'runner_on_skipped':
                single_host_res.update({'status': 'skipped', 'msg': '任务被忽略'})
            result.update({host: single_host_res})
        return result
