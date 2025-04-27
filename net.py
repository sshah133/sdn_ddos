from datetime import datetime
import os
import psutil
from subprocess import Popen, DEVNULL
import time
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

class LessSimpleTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

class MyNetwork:

    def __init__(self):
        if os.path.exists('timestamps.txt'):
            os.remove('timestamps.txt')
        self.ts_file = open('timestamps.txt', 'w')

    def clean_env(self):
        print(f"* Cleaning mininet environ")
        cmd = "sudo mn -c"
        print(f"** Running: {cmd}")
        Popen(cmd, shell=True).wait()
        print(f"* Done cleaning mininet environ")
    
    def start_net(self, controller_ip='127.0.0.1', controller_port=6633):
        """Build the topology and initialize the network with a remote controller"""
        controller = RemoteController('c0', ip=controller_ip, port=controller_port)
        self.net = Mininet(topo=SimpleTopo(), controller=controller)
        #self.net = Mininet(topo=LessSimpleTopo(), controller=controller)
        self.net.start()

        print("Dumping host connections")
        dumpNodeConnections(self.net.hosts)

        print("Testing network connectivity")
        self.net.pingAll()

    def stop_net(self):
        """Stop Mininet with current network"""
        self.net.stop()

    def clear_metrics(self):
        print('* Clearing metrics')
        if os.path.exists("bandwidth.txt"):
            os.remove("bandwidth.txt")
        if os.path.exists("controller_usage.txt"):
            os.remove("controller_usage.txt")

    def start_metrics(self):
        print('* Starting monitor')
        cmd = f"bwm-ng -o csv -T rate -C ',' > bandwidth.txt &"
        Popen(cmd, shell=True).wait()
        c_cmd = f"sudo python3 cpu_track.py"
        self.cont_proc = Popen(c_cmd, shell=True)
        self.ts_file.write(str(time.time())+'\n')

    def stop_metrics(self):
        print('* Stopping monitor')
        cmd = "killall bwm-ng"
        Popen(cmd, shell=True).wait()
        self.cont_proc.terminate()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and 'cpu_track.py' in ' '.join(cmdline):
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        self.ts_file.write(str(time.time())+'\n')
        self.ts_file.close()

    def start_ddos(self):
        print('* Starting DDoS Attack')
        print("** Attack started at:", datetime.now())
        self.ts_file.write(str(time.time())+'\n')
        h1 = self.net.get('h1')
        h2_ip = self.net.get('h2').IP()
        h1.cmd(f"hping3 --flood {h2_ip} &")

    def stop_ddos(self):
        print('* Stopping DDoS Attack')
        self.ts_file.write(str(time.time())+'\n')
        cmd = "killall hping3"
        Popen(cmd, shell=True).wait()
        print("** Attack stopped at:", datetime.now())
    
    def create_graphs(self):
        print('* Creating Graphs')
        cmd = f"sudo python3 create_graphs.py"
        Popen(cmd, shell=True).wait()


if __name__ == '__main__':
    setLogLevel('info')
    net = MyNetwork()
    net.clean_env()
    net.clear_metrics()
    net.start_net()
    net.start_metrics()
    time.sleep(5)
    #CLI(net.net)
    net.start_ddos()
    time.sleep(5)
    #CLI(net.net)
    net.stop_ddos()
    time.sleep(15)
    #CLI(net.net)
    net.stop_metrics()
    net.stop_net()
    net.clean_env()
    net.create_graphs()

