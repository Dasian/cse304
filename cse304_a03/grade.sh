#!/bin/bash
for f in a03_test_cases/*; do
	echo "********************************************";
	echo "$f";
	cat "$f";
	python3 decaf_checker.py "$f";
	echo "";
done
