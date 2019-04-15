# Graft-Alpha-Watchdog
Graft SN Watchdog/Reset

cd ~

git clone https://github.com/graft-community/graft-sn-watchdog

cd graft-sn-watchdog

sudo chmod +x gn.sh once in folder

sudo chmod +x gs.sh once in folder

./gn.sh to launch graftnode reset script once in folder

./gs.sh to launch graft_server reset script once in folder

These can be run inside seperate TMUX sessions or panes although graftnoded is set for
	--detach so there will be no screen response.

Then run python3 snwatchdog.py inside the folder, once both above .sh scripts are loaded.

Currently the snwatchdog script now looks for less than 5 SN's in the sn list and resets both graft instances 
	if this occurs.
	
*** Please note: Reset is currently disabled by default and version and status checking is assumed you have Deb Community Build or bash command will error out, without correct path set. ***
