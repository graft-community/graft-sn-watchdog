
#!/bin/bash

while true; do
        if [ ! `pgrep supernode` ]; then
                ~/Supernode/supernode &
                for ((i=0; i<600; i+=5)); do
                        sleep 5
                        if [ ! `pgrep supernode` ]; then
                                break
                        fi
                done
                #killall -9 supernode > /dev/null 2>&1 # Warning this will kill graft_server inside each hour
        fi
        sleep 5
done

