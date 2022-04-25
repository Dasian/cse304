#!/bin/bash

f="tests/testing.decaf"
echo "$f";
cat "$f";
python3 decaf_checker.py "$f";
