import xml.etree.ElementTree as ET
import sys

logPath = ''
if (len(sys.argv) > 1):
  logPath = sys.argv[1]
else:
  print('Specify path to the log file as the 1st argument')
  sys.exit()

suppressDiffBuilderCall = False
if (len(sys.argv) > 2):
  suppressDiffBuilderCall = True

tree = ET.parse(logPath)
logRoot = tree.getroot()

diffBuilderFile = 'svn_diff_builder.bat'
file = open(diffBuilderFile, 'w+')
file.write('@echo off' + '\n')
file.write('\n')
file.write('SET repo_path="%RSSTAT_REPO_PATH%"' + '\n')
file.write('IF "%repo_path%" == "" (echo "repo is undefined"' + '\n')
file.write('EXIT)' + '\n')
file.write('SET stat_path=%~dp0' + '\n')
file.write('\n')
file.write('if not exist "%stat_path%/diffs" mkdir "%stat_path%/diffs"' + '\n')
file.write('SET repoTemp=%repo_path%' + '\n')
file.write('cd /d %repoTemp:~1,3%' + '\n')
file.write('cd %repo_path%' + '\n')
file.write('SET repoFolderSearcher=%repo_path%' + '\n')
file.write('for %%f in (%repoFolderSearcher%) do SET repoFolderName=%%~nxf' + '\n')
file.write('\n')

revisions = []
for logentry in logRoot.findall('logentry'):
  """
   logentry[0] - author
   logentry[1] - date, time
   logentry[2] - paths, files
   logentry[3] - message
  """
  revisionStr = logentry.get('revision')
  revisions.append(revisionStr)
  file.write('set outputDiff=%stat_path%/diffs/%repoFolderName%_{0}.log'.format(revisionStr) + '\n')
  file.write('svn diff -c {0} > %outputDiff%'.format(revisionStr) + '\n' + '\n')

file.write('SET statPathVal=%stat_path%' + '\n')
file.write('cd /d %stat_path:~0,3%' + '\n')
file.write('cd "%stat_path%"')
file.close()

import subprocess
callArgs = [diffBuilderFile]
if not suppressDiffBuilderCall:
  print('svn_diff_extractor.bat has been started')
  subprocess.call(callArgs)
  print('svn_diff_extractor.bat has been finished')

revisions = sorted(revisions)
revsDiffMap = {}
from diffs_analyzer import analyze_diffs
analyze_diffs(revisions, revsDiffMap)

outputResults = open('a.log', 'w+')
for revision in revisions:
  outputResults.write('Revision: {0: <5}   Added: {1: <5}   Removed: {2: <5}'.format(revision, revsDiffMap[int(revision)][0], revsDiffMap[int(revision)][1]))
  outputResults.write('\n')















