#!/usr/bin/env python
#####
##	Author: Joshua Holzworth
#####

import os
import subprocess
import sys
import getopt
import notifier_singleton


def usage():
	print 'update_batch.py -c <configFileName> -s <stepName>'

defaultCFG = 'config.cfg'
def updateBatchID(stepName):
	updateBatchID(defaultCFG,stepName)
	
def updateBatchID(configFileName, stepName):
	notifier_singleton.readConfig(configFileName)
	notifier_singleton.incrBatchID(stepName)
	notifier_singleton.writeConfig(configFileName)

