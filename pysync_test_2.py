from pysyncobj import SyncObj, replicated

class kvStore(SyncObj):
    def __init__(self):
        super(kvStore, self).__init__('10.10.1.5:9000', ['10.10.1.4:9000'])
        self.mac_to_port = {}
    
    @replicated
    def setDefault(self, dpid):
        self.mac_to_port.setdefault(dpid, {})
    
    @replicated
    def write(self, dpid, src, in_port):
        self.mac_to_port[dpid][src] = in_port
    
    def read(self, dpid, dst):
        return self.mac_to_port[dpid][dst]
    
    def isIn(self, dpid, dst):
        return dst in self.mac_to_port[dpid]

    def printAll(self):
        print("in print all")
        print(self.mac_to_port)

class caller:
    def __init__(self):
        self.kvStore = kvStore()
    
    def add(self, dpid, src, in_port):
        self.kvStore.setDefault(dpid)
        self.kvStore.write(dpid, src, in_port)

    def print(self):
        self.kvStore.printAll()


myCaller = caller()
myCaller.add(2, 1, 1)
myCaller.add(2, 2, 2)
myCaller.print()
    
    