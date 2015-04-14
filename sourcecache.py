from buildslave.commands import base
import os,imp
import tempfile,tarfile
from twisted.internet.defer import inlineCallbacks
import shelve

class SourceCacheIndex:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
    def load(self,where):
        if "backend" not in dir(self):
            self.backend = shelve.open(where)
    def checksum(self,package):
        return self.backend.get(package,None)
    def setChecksum(self,package,sum):
        self.backend[package] = sum

class UpdateCache(base.Command):
    header = "updateCache"
    requiredArgs = ['_package']
    @inlineCallbacks
    def start(self):
        pkg = self.args["_package"]
        pkg.callRemote("openFile","_cache",True)
        # todo: checsum check
	# download data
	tmp = tempfile.TemporaryFile()
	buff = " "
	while (len(buff) > 0):
	    buff = yield pkg.callRemote("read")
	    tmp.write(buff)
	tmp.seek(0)
	tar = tarfile.TarFile(fileobj=tmp,mode="r")
	tar.extractall(os.path.join(self.builder.basedir,"..","ext"))
	tar.close()
	tmp.close()
        self.sendStatus({'rc': 0})

class Wrapper(base.Command):
    header = "wrapper"
    requiredArgs = ['_package']
    @inlineCallbacks
    def start(self):
        pkg = self.args["_package"]
        pkgName = yield pkg.callRemote("packageName")
        self.basedir = os.path.join(self.builder.basedir,"..","ext")
        index = SourceCacheIndex()
        index.load(os.path.join(self.basedir,"index"))   
        # todo: checsum check
        current = yield pkg.callRemote("checksum")
        if ( current != index.checksum("packageName")):
            #download update
            pkg.callRemote("openFile","_cache",True)
	    tmp = tempfile.TemporaryFile()
	    buff = " "
	    while (len(buff) > 0):
	        buff = yield pkg.callRemote("read")
	        tmp.write(buff)
	    tmp.seek(0)
	    tar = tarfile.TarFile(fileobj=tmp,mode="r")
	    tar.extractall(os.path.join(self.builder.basedir,"..","ext"))
	    tar.close()
	    tmp.close()
	#execute updated command
        pathname = [self.builder.basedir,"..","ext","_cache"]
        pathname += pkgName.split(".")
        pathname +=["__init__.py"]
        pathname = os.path.join(*pathname)

        module = imp.load_source("command",pathname)

        Command = module.commandFactory()
        c=Command(self.builder,self.stepId,self.args)
        yield c.doStart()
