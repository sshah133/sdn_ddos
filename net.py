from subprocess import Popen
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.util import dumpNodeConnections

class SimpleTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        self.addLink(h1, s1)
        self.addLink(h2, s1)

class MyNetwork:

    def clean_env(self):
        print(f"* Cleaning mininet environ")
        cmd = "sudo mn -c"
        print(f"** Running: {cmd}")
        Popen(cmd, shell=True).wait()
        #cmd = "sudo fuser -k 6633/tcp"
        #print(f"** Running: {cmd}")
        #Popen(cmd, shell=True).wait()
        print(f"* Done cleaning mininet environ")
    
    def start_net(self, controller_ip='127.0.0.1', controller_port=6633):
        """Build the topology and initialize the network with a remote controller"""
        controller = RemoteController('c0', ip=controller_ip, port=controller_port)
        self.net = Mininet(topo=SimpleTopo(), controller=controller)
        self.net.start()

        print("Dumping host connections")
        dumpNodeConnections(self.net.hosts)

        print("Testing network connectivity")
        self.net.pingAll()

    def stop_net(self):
        """Stop Mininet with current network"""
        self.net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    net = MyNetwork()
    net.clean_env()
    net.start_net(controller_ip='127.0.0.1')  
    CLI(net.net)  # Optional interactive CLI
    net.stop_net()
    net.clean_env()

