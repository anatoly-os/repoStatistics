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


sys.path.insert(0, './libs/')
from diff_analyzer import repoPath
from diff_analyzer import diffsPath
repoPathLetter = repoPath[0:2]
repoFolderName = os.path.basename(repoPath)
file.write('@echo off' + '\n')
file.write('\n')
file.write('SET stat_path=%~dp0' + '\n')
file.write('\n')
file.write('if not exist "%stat_path%/{0}" mkdir "%stat_path%/{0}"'.format(diffsPath[1:-1]) + '\n')
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

  from diff_analyzer import bannedDiffsPath
  if not (os.path.isfile('{0}/{1}_{2}.log'.format(diffsPath, repoFolderName, revisionStr)) or
          os.path.isfile('{0}/{1}_{2}.log'.format(bannedDiffsPath, repoFolderName, revisionStr)) ):
    file.write('echo {0} revision diff in progress...'.format(revisionStr) + '\n')
    file.write('set outputDiff=%stat_path%{0}/{1}_{2}.log'.format(diffsPath[1:-1], repoFolderName, revisionStr) + '\n')
    file.write('svn diff -c {0} > %outputDiff%'.format(revisionStr) + '\n' + '\n')

file.write('SET statPathVal=%stat_path%' + '\n')
file.write('cd /d %stat_path:~0,3%' + '\n')
file.write('cd "%stat_path%"')
file.close()

runDiffConstructor = True
if (len(sys.argv) > 2):
  runDiffConstructor = False

import subprocess
if runDiffConstructor:
  callArgs = [diffBuilderFile]
  print('{0} has been started'.format(diffBuilderFile))
  subprocess.call(callArgs)
  print('{0} has been finished'.format(diffBuilderFile))

authorDataDict = {}
from diff_analyzer import analyze_diffs
print('analyzing has been started')
analyze_diffs(revisions, authorDataDict)
print('analyzing has been finished')

from suspicious_revisions_extractor import extractSuspiciousRevision
print('extracting suspicious revisions...')
extractSuspiciousRevision(logPath, authorDataDict)

from statistics_html_builder import buildHtmlStatistics
buildHtmlStatistics(authorDataDict)
