########
##	Author: Joshua Holzworth
########

import os
import subprocess

HDFS_CMD = "hdfs dfs"

#Obtain files on hdfs and place them on local
#  hdfsDir - can also be referenced as src dir where files are located
#  localDir - can also be refenced as dest dir where files will be pulled to
def getFiles(hdfsDir, localDir):
	if not os.path.exists(localDir):
		print('FAILURE')
	pullCmd = HDFS_CMD+" -get "+hdfsDir+"/* "+localDir+"/."
	print("Pulling hdfs files into: "+localDir)
	pullProc = subprocess.Popen(pullCmd,shell=True)
	pullProc.communicate()


#Pushes all files locate din localDir into hdfsDir
def putFiles(localDir,hdfsDir):
	if not os.path.exists(localDir):
		print('FAILURE')
	pushCmd = HDFS_CMD+' -put '+localDir+'/* '+hdfsDir+'/.'
	pushProc = subprocess.Popen(pushCmd,shell=True)
	pushProc.communicate()
