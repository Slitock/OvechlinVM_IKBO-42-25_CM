#!/usr/bin/env bash
echo "Runing unit test \n -------"
python3 -m unittest discover -s tests -v
echo "-------"
