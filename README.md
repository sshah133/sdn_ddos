# sdn_ddos

## Downloads

Ensure you have `Mininet` and `pox` set up in your environment.

Additionally, some other packages will be needed:

We use `bwm-ng` to monitor the network. Install in Linux using:
```
sudo apt-get -y install bwm-ng
```

## Start Controller

The `rate_limit.py` file is the controller file. Copy this file into your `pox/` folder and run:
```
./pox.py log.level --DEBUG rate_limit
```

## Start Network Attack

Run the `net.py` file by:
```
sudo python3 net.py
```
