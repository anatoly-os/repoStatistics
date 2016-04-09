import sys
import os
import os.path
import re

#revisions - list of strings with revision numbers
def analyze_diffs(revisions, revsDiffMap):
  repoPath = os.getenv('RSSTAT_REPO_PATH')
  diffsPath = './diffs/'
  folderName = os.path.basename(repoPath)
  charsToRemoveToIdentifyNonEmptyString = ['{', '}', '/', '*', '(', ')', '[', ']', ';','\n','\r', '+', '-']
  rx = '[' + re.escape(''.join(charsToRemoveToIdentifyNonEmptyString)) + ']'
  for revision in revisions:
    file = open(diffsPath + '{0}_{1}.log'.format(folderName, revision))
    addedLines = 0
    removedLines = 0
    for line in file:
      if len(line) < 1:
        continue

      firstChar = line[0]
      #svn diff uses '+' as a first char for added lines and '-' for removed ones
      if not firstChar == '+' and not firstChar == '-':
        continue

      #service lines like "+++ path/to/src/file.cpp (revision xxx)" in diff files
      #service lines like "--- path/to/src/file.cpp (revision xxx)" in diff files
      if (len(line) > 2) and line[1] == line[2] == firstChar:
        continue

      remainingLine = re.sub(rx, '', line)
      if (len(remainingLine) > 0):
        if firstChar == '+':
          addedLines += 1
        elif firstChar == '-':
          removedLines += 1

    revsDiffMap[int(revision)] = [addedLines, removedLines]