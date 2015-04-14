from buildslave.commands import base
import os,imp

class Wrapper(base.Command):
    header = "wrapper"
    requiredArgs = ['_cmdName']
    def start(self):
	pathname = [self.builder.basedir,"..","ext","_cache"]
	pathname += self.args["_cmdName"].split(".")
	pathname +=["__init__.py"]
	pathname = os.path.join(*pathname)
	
	module = imp.load_source("command",pathname)
	
        Command = module.commandFactory()
        c=Command(self.builder,self.stepId,self.args)
        return c.doStart()
