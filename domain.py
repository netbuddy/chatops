
class Task:
    def __init__(self, name, desc) -> None:
        self.name = name
        self.desc = desc
        self.host = None
        self.executor = ''
        self.args = {}
        self.result = ''
        self.prompts = []
        self.train_scenes = []

    def set_executor(self, executor):
        self.executor = executor

class Entity:
    def __init__(self, name, desc) -> None:
        self.name = name
        self.desc = desc

class Operate:
    def __init__(self, name, desc) -> None:
        self.name = name
        self.desc = desc

class File(Entity):
    def __init__(self, name, desc, path):
       super(Entity, self).__init__(name, desc)
       self.path=path
       self.owner=None
       self.group=None
       self.mode=None

class FileCopy(Operate):
    def __init__(self, name, desc, src, dest):
       super(Operate, self).__init__(name, desc)
       self.src=src
       self.dest=dest

