#!/bin/bash
DELAY=$1
shift
for i in mn-unicorn-1 mn-unicorn-2 mn-sense-1 ride jemison lovelace mn-amp-1 mn-amp-2 mn-satellite mn-node-3 ; do 
	ssh -A medianet@$i "sleep $(($RANDOM % $DELAY)) ; $@ &" &
done
