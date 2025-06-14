# Proxmox ntfy
### Monitor your proxmox datacenter with phone notifications
<img src="docs/IMG_20250609_174259.jpg" width="500"/>

# Prerequisites
* Proxmox (extensive use of the `Proxmoxer` API)
* Terminal multiplexer (such as `tmux`) [Optional]
* python3
* python3-requests (It's possible to use `curl` instead with Python `subprocess`) [*Optional]

# Deploying
This example will utilize `tmux`:

1. Create a new named session, "ntfy" will be used as an example:
```
tmux [new|new-session] -s ntfy
```
2. Enter the new session:
```
tmux attach -t ntfy
```
3. Download and start the script:
```
git clone --depth=1 https://github.com/unixtensor/proxmox-ntfy
python3 ./proxmox-ntfy/src/main.py http://your.domain.com/
```

Detatch from the current tmux session with `<Ctrl b><d>`, the script should now be deployed and running in the background.