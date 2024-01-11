#!/bin/bash
for i in 1 2 3 ; do
	ssh -A medianet@mn-pi5-$i "\
		sudo reboot" \
	&
done
