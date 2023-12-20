#!/bin/bash
for i in ride jemison lovelace mn-amp-1 mn-amp-2 mn-sense-1 mn-unicorn-1 mn-satellite mn-node-3; do 
	ssh -A medianet@$i "\
		killall -KILL mpv ;\
		killall -KILL python3.11 ;\
		bin/display.sh python3.11 no-mans-sky/gol-pygame.py &" \
	&
done
