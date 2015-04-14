from buildslave.commands import base
import os,imp
import tempfile,tarfile
from twisted.internet.defer import inlineCallbacks

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

