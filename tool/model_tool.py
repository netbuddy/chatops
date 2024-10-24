#!/usr/bin/env python
"""A simple cmd2 application."""
import cmd2
from prompt_toolkit import prompt
import json

class FirstApp(cmd2.Cmd):
    """A simple cmd2 application."""
    def __init__(self):
        super().__init__()

        # Make maxrepeats settable at runtime
        # self.maxrepeats = 3
        # self.add_settable(cmd2.Settable('maxrepeats', int, 'max repetitions for speak command', self))

    creat_entity_parser = cmd2.Cmd2ArgumentParser()
    creat_entity_parser.add_argument('name', help='entity name')

    @cmd2.with_argparser(creat_entity_parser)
    def do_creat_entity(self, args):
        """Repeats what you tell me to."""
        name = args.name
        features = prompt('请输入实体的特性列表，每行一个特性，Alt+Enter键结束输入:\n', multiline=True)
        # self.poutput(features)
        with open("{}.json".format(name), "w") as entity_file:
            entity = {}
            entity['type'] = 'object'
            entity['properties'] = {}
            entity['properties']['id'] = {'type': 'number'}
            for feature in features.split('\n'):
                feature_name = feature.split()[1]
                feature_type = feature.split()[0]
                entity['properties'][feature_name] = {'type': feature_type}
            json.dump(entity, entity_file)

    creat_service_parser = cmd2.Cmd2ArgumentParser()
    creat_service_parser.add_argument('name', help='service name')

    @cmd2.with_argparser(creat_service_parser)
    def do_creat_service(self, args):
        """Repeats what you tell me to."""
        name = args.name
        entities = prompt('请输入被操作的实体列表，以空格分隔开:')
        executor_type = int(prompt('请选择执行器类型，1-snaible 2-shell:'))
        # self.poutput(features)
        with open("{}.json".format(name), "w") as service_file:
            service = {}
            service['entities'] = []
            for entity in entities.split():
                service['entities'].append(entity)
            match executor_type:
                case 1:
                    service['executor'] = 'ansible'
                    module = prompt('请输入ansible的模块名称:')
                    service['ansible_module'] = module
                case 2:
                    service['executor'] = 'shell'
                case _:
                    print('Unknown executor type')
                    return
            json.dump(service, service_file)

if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())
