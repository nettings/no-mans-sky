#!/bin/bash
for i in mn-unicorn-1 mn-unicorn-2 ; do
	ssh -A medianet@$i "\
		killall -KILL python3.11 ;\
		/usr/bin/python3.11 /home/medianet/no-mans-sky/gol-unicorn.py &" \
	&
done
for i in mn-sense-1 ; do
	ssh -A medianet@$i "\
		killall -KILL python3.11 ;\
		/usr/bin/python3.11 /home/medianet/no-mans-sky/gol-sense.py &" \
	&
done
for i in ride jemison lovelace mn-amp-1 mn-amp-2 mn-sense-1 mn-unicorn-1 mn-satellite mn-node-3; do 
	ssh -A medianet@$i "\
		killall -KILL mpv ;\
		killall -KILL python3.11 ;\
		bin/display.sh python3.11 no-mans-sky/gol-pygame.py &" \
	&
done
