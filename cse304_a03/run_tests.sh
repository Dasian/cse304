#!/bin/bash
for f in tests/*; do
	echo "********************************************";
	echo "$f";
	cat "$f";
	python3 decaf_checker.py "$f";
	echo "";
done
