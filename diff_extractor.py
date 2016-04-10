import xml.etree.ElementTree as ET
import sys
import os

logPath = ''
if (len(sys.argv) > 1):
  logPath = sys.argv[1]
else:
  print('Specify path to the log file as the 1st argument')
  sys.exit()

tree = ET.parse(logPath)
logRoot = tree.getroot()

diffBuilderFile = 'svn_diff_builder.bat'
file = open(diffBuilderFile, 'w+')

repoPath = os.getenv('RSSTAT_REPO_PATH')
repoPathLetter = repoPath[0:2]
repoFolderName = os.path.basename(repoPath)
file.write('@echo off' + '\n')
file.write('\n')
file.write('SET stat_path=%~dp0' + '\n')
file.write('\n')
file.write('if not exist "%stat_path%/diffs" mkdir "%stat_path%/diffs"' + '\n')
file.write('cd /d {0}'.format(repoPathLetter) + '\n')
file.write('cd {0}'.format(repoPath) + '\n')
file.write('\n')

revisions = {}
for logentry in logRoot.findall('logentry'):
  """
   logentry[0] - author
   logentry[1] - date, time
   logentry[2] - paths, files
   logentry[3] - message
  """
  revisionStr = logentry.get('revision')
  revisions[int(revisionStr)] = logentry[0].text

  if not os.path.isfile('./diffs/{0}_{1}.log'.format(repoFolderName, revisionStr)):
    file.write('set outputDiff=%stat_path%/diffs/{0}_{1}.log'.format(repoFolderName, revisionStr) + '\n')
    file.write('svn diff -c {0} > %outputDiff%'.format(revisionStr) + '\n' + '\n')

file.write('SET statPathVal=%stat_path%' + '\n')
file.write('cd /d %stat_path:~0,3%' + '\n')
file.write('cd "%stat_path%"')
file.close()

import subprocess
callArgs = [diffBuilderFile]
print('{0} has been started'.format(diffBuilderFile))
subprocess.call(callArgs)
print('{0} has been finished'.format(diffBuilderFile))

revisionsNumSorted = sorted(revisions)
revsDiffMap = {}
from diffs_analyzer import analyze_diffs
print('analyzing has been started')
analyze_diffs(revisionsNumSorted, revsDiffMap)
print('analyzing has been finished')

authorDataDict = {}
for revision in revisionsNumSorted:
  authorName = revisions[revision]
  addedStringsNum = revsDiffMap[revision][0]
  removedStringsNum = revsDiffMap[revision][1]
  if not authorName in authorDataDict:
    authorDataDict[authorName] = []

  authorDataDict[authorName].append([revision, addedStringsNum, removedStringsNum])

from statistics_html_builder import buildHtmlStatistics
buildHtmlStatistics(authorDataDict)
