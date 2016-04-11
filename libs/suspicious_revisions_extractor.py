import xml.etree.ElementTree as ET
import sys

def extractSuspiciousRevision(logFile, authorDataDict):
  tree = ET.parse(logFile)
  logRoot = tree.getroot()

  suspiciousRevisions = {}
  for logentry in logRoot.findall('logentry'):
    '''
     logentry[0] - author
     logentry[1] - date, time
     logentry[2] - paths, files
     logentry[3] - message
    '''
    revisionNumber = int(logentry.get('revision'))
    if (len(logentry) < 4):
      continue

    authorName = logentry[0].text
    message = logentry[3].text
    if 'revert' in message:
      suspiciousRevisions[revisionNumber] = 'Reverted'
      logRoot.remove(logentry)
      continue

    if 'rename' in message:
      suspiciousRevisions[revisionNumber] = 'Renamed'
      logRoot.remove(logentry)
      continue

  from diff_analyzer import suspiciousRevisionsFile
  suspeciousFiles = open(suspiciousRevisionsFile, 'w+')

  suspeciousFiles.write('------------- "Reverted", "Renamed" revisions -------------' + '\n')

  suspiciousRevs = sorted(suspiciousRevisions)
  counter = 0
  for rev in suspiciousRevs:
    counter += 1
    suspeciousFiles.write('{0: >3}) Revision: {1: >5}   '.format(counter, rev) + '{0: >10}'.format(suspiciousRevisions[rev]) + '\n')

  suspeciousFiles.write('------------- >1000 lines revisions -------------' + '\n')
  for author in authorDataDict:
    for item in authorDataDict[author]:
      totalStringsChanged = item[1] + item[2]
      if totalStringsChanged > 1000:
        suspeciousFiles.write('Revision: {0: <5}   Strings Changed: {1: <5}'.format(item[0], totalStringsChanged) + '\n')