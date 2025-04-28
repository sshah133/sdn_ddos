# sdn_ddos

## Start Controller

The Pox controllers are in the `pox_controllers` repository. There are two controllers to choose from: `flood_cont.py` and `rate_limit.py`. The `flood_cont.py` is the controller for the regular Pox controller without rate limiting. In this controller, the controller tells each switch to just flood each packet. The `rate_limit.py` is the controller for the Rate Limit implementing Pox Controller. This controller will also flood the packet but will install a rule on the switch to block packets for 5 seconds if the source IP of the packets is sending packets at a rate greater than 50 packets per second.

To run the controller, copy the controller file you wish to run into your `pox/` folder and run:
```
./pox.py log.level --DEBUG {controller name (rate_limit) or (flood_cont)}
```

## Start Network Attack

The `net.py` file is the main file for this project that runs all the code and will call the other files `cpu_track.py` and `create_graphs.py`. This file cleans the network environments, starts recording metrics before the experiment and stops recording metrics after the experiment, starts up and stops the network, starts up and stops the DDoS attack, and creates graphs for the metrics.

Run the `net.py` file by first ensuring a remote controller is running on `localhost:6633` and then running:
```
sudo python3 net.py
```
