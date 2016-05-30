#!/bin/bash
./analysis.py |& grep -E '\+|\|' |& grep -vE 'INFO\s|WARN'
