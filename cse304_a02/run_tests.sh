#!/bin/bash
for f in tests/*; do
	echo "$f";
	python3 decaf_checker.py "$f";
	echo "";
done
