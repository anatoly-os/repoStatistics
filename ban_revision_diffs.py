import xml.etree.ElementTree as ET
import sys
import os

bannedRevsList = ''
if (len(sys.argv) > 1):
  bannedRevsList = sys.argv[1]
else:
  print('Specify path to the list of banned revisions as the 1st argument')
  sys.exit()

bannedRevsFile = open(bannedRevsList, 'r')
diffFilesToBan = []

sys.path.insert(0, './libs/')
from diff_analyzer import repoPath
from diff_analyzer import diffsPath
from diff_analyzer import bannedDiffsPath
folderName = os.path.basename(repoPath)

if not os.path.exists(bannedDiffsPath):
  os.makedirs(bannedDiffsPath)

from diff_analyzer import diffLogMask
for line in bannedRevsFile:
  revision = line.split(' ')[0] #revision number only
  logName = diffLogMask.format(folderName, revision)
  if os.path.exists(diffsPath + logName):
    os.rename(diffsPath + logName, bannedDiffsPath + logName)


