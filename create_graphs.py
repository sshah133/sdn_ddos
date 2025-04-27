import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

if os.path.exists("cont_cpu_plot.png"):
    os.remove("cont_cpu_plot.png")
if os.path.exists("cont_mem_plot.png"):
    os.remove("cont_mem_plot.png")
if os.path.exists("s1-eth1_bw_plot.png"):
    os.remove("s1-eth1_bw_plot.png")
if os.path.exists("s1-eth2_bw_plot.png"):
    os.remove("s1-eth2_bw_plot.png")

with open('timestamps.txt', 'r') as file:
    timestamps = [float(line.strip()) for line in file]
timestamps = pd.to_datetime(timestamps, unit='s')

start = timestamps[0]
ddos_start = timestamps[1]
ddos_end = timestamps[2]
end = timestamps[3]

bw_df = pd.read_csv('bandwidth.txt', header=None)

#create s1-eth1 interface bandwidth dataframe
eth1s1 = bw_df.loc[bw_df[1] == 's1-eth1'][[0,4]]
eth1s1 = eth1s1.rename(columns={0:'epochtime', 4:'bandwidth'})
eth1s1['time'] = pd.to_datetime(bw_df.loc[bw_df[1] == 's1-eth1'][0], unit='s')
eth1s1 = eth1s1.drop(['epochtime'], axis=1).set_index('time')

#create s1-eth1 interface bandwidth graph
eth1s1.index = pd.to_datetime(eth1s1.index)
eth1s1 = eth1s1[eth1s1.index >= start]
eth1s1 = eth1s1[eth1s1.index <= end]
eth1s1['bandwidth'] = eth1s1['bandwidth'].rolling(window=3, min_periods=1).mean()
eth1s1.plot(y='bandwidth', legend=False)
plt.xlabel('Time')
plt.ylabel('Bandwidth (bytes/sec)')
plt.title('s1-eth1 Bandwidth Over Time')
plt.grid(True)
plt.axvline(x=ddos_start, color='red', linestyle='--', label='DDoS Start')
plt.axvline(x=ddos_end, color='orange', linestyle='--', label='DDoS End')
plt.legend()
plt.tight_layout()

plt.savefig('s1-eth1_bw_plot.png')
plt.close()

#create s1-eth2 interface bandwidth dataframe
eth2s1 = bw_df.loc[bw_df[1] == 's1-eth2'][[0,4]]
eth2s1 = eth2s1.rename(columns={0:'epochtime', 4:'bandwidth'})
eth2s1['time'] = pd.to_datetime(bw_df.loc[bw_df[1] == 's1-eth2'][0], unit='s')
eth2s1 = eth2s1.drop(['epochtime'], axis=1).set_index('time')

#create s1-eth2 interface bandwidth graph
eth2s1.index = pd.to_datetime(eth2s1.index)
eth2s1 = eth2s1[eth2s1.index >= start]
eth2s1 = eth2s1[eth2s1.index <= end]
eth2s1['bandwidth'] = eth2s1['bandwidth'].rolling(window=3, min_periods=1).mean()
eth2s1.plot(y='bandwidth', legend=False)
plt.xlabel('Time')
plt.ylabel('Bandwidth (bytes/sec)')
plt.title('s1-eth2 Bandwidth Over Time')
plt.grid(True)
plt.axvline(x=ddos_start, color='red', linestyle='--', label='DDoS Start')
plt.axvline(x=ddos_end, color='orange', linestyle='--', label='DDoS End')
plt.legend()
plt.tight_layout()

plt.savefig('s1-eth2_bw_plot.png')
plt.close()

#create the controller usage dataframe
data = []
with open("controller_usage.txt", "r") as f:
    for line in f:
        parts = line.strip().split(", ")
        timestamp_str = parts[0]
        cpu_str = parts[1].replace("CPU: ", "").replace("%", "")
        mem_str = parts[2].replace("MEM: ", "").replace("%", "")        
        data.append({
            "time": pd.to_datetime(timestamp_str),
            "cpu": float(cpu_str),
            "mem": float(mem_str)
        })

con_df = pd.DataFrame(data)
con_df.set_index("time", inplace=True)

#create controller cpu graph
con_cpu_df = con_df[['cpu']]
con_cpu_df.index = pd.to_datetime(con_cpu_df.index)
con_cpu_df = con_cpu_df[con_cpu_df.index >= start]
con_cpu_df = con_cpu_df[con_cpu_df.index <= end]
con_cpu_df['cpu'] = con_cpu_df['cpu'].rolling(window=3, min_periods=1).mean()
con_cpu_df.plot(y='cpu', legend=False)
plt.xlabel('Time')
plt.ylabel('CPU (percentage)')
plt.title('Controller CPU Utilization Over Time')
plt.grid(True)
plt.axvline(x=ddos_start, color='red', linestyle='--', label='DDoS Start')
plt.axvline(x=ddos_end, color='orange', linestyle='--', label='DDoS End')
plt.legend()
plt.tight_layout()

plt.savefig('cont_cpu_plot.png')
plt.close()

#create controller mem graph
con_mem_df = con_df[['mem']]
con_mem_df.index = pd.to_datetime(con_mem_df.index)
con_mem_df = con_mem_df[con_mem_df.index >= start]
con_mem_df = con_mem_df[con_mem_df.index <= end]
con_mem_df['mem'] = con_mem_df['mem'].rolling(window=3, min_periods=1).mean()
con_mem_df.plot(y='mem', legend=False)
plt.xlabel('Time')
plt.ylabel('Mem (percentage)')
plt.title('Controller Mem Utilization Over Time')
plt.grid(True)
plt.axvline(x=ddos_start, color='red', linestyle='--', label='DDoS Start')
plt.axvline(x=ddos_end, color='orange', linestyle='--', label='DDoS End')
plt.legend()
plt.tight_layout()

plt.savefig('cont_mem_plot.png')
plt.close()

