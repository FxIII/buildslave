from buildslave.commands import base

class Echo(base.Command):
    header = "echo"
    requiredArgs = ['msg']
    def start(self):
        self.sendStatus({'pong': self.args['msg']})
        self.sendStatus({'rc': 0})
