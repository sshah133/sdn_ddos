import pandas as pd
import matplotlib.pyplot as plt

cutoff = pd.to_datetime("2025-04-01 00:00:00")

bw_df = pd.read_csv('bandwidth.txt', header=None)

#create s1-eth1 interface bandwidth dataframe
eth1s1 = bw_df.loc[bw_df[1] == 's1-eth1'][[0,4]]
eth1s1 = eth1s1.rename(columns={0:'epochtime', 4:'bandwidth'})
eth1s1['time'] = pd.to_datetime(bw_df.loc[bw_df[1] == 's1-eth1'][0], unit='s')
eth1s1 = eth1s1.drop(['epochtime'], axis=1).set_index('time')

#create s1-eth1 interface bandwidth graph
eth1s1.index = pd.to_datetime(eth1s1.index)
eth1s1 = eth1s1[eth1s1.index >= cutoff]
eth1s1.plot(y='bandwidth', legend=False)
plt.xlabel('Time')
plt.ylabel('Bandwidth (bytes/sec)')
plt.title('s1-eth1 Bandwidth Over Time')
plt.grid(True)
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
eth2s1 = eth2s1[eth2s1.index >= cutoff]
eth2s1.plot(y='bandwidth', legend=False)
plt.xlabel('Time')
plt.ylabel('Bandwidth (bytes/sec)')
plt.title('s1-eth2 Bandwidth Over Time')
plt.grid(True)
plt.tight_layout()

plt.savefig('s1-eth2_bw_plot.png')
plt.close()

