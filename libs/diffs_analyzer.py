import sys
import os
import os.path
import re

def linesCounter(linesByFiles):
  charsToRemoveToIdentifyNonEmptyString = ['{', '}', '/', '*', '(', ')', '[', ']', ';','\n','\r', '+', '-']
  rx = '[' + re.escape(''.join(charsToRemoveToIdentifyNonEmptyString)) + ']'
  addedLines = 0
  removedLines = 0
  for codeFileLines in linesByFiles:
    for line in codeFileLines:
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

  return addedLines, removedLines

def analyze_diffs(revisionAuthorDict, authorDataDict):
  repoPath = os.getenv('RSSTAT_REPO_PATH')
  diffsPath = './diffs/'
  folderName = os.path.basename(repoPath)
  revisionsNumSorted = sorted(revisionAuthorDict)
  for revision in revisionsNumSorted:
    file = open(diffsPath + '{0}_{1}.log'.format(folderName, str(revision)))
    filesSeparator = '==================================================================='
    from collections import defaultdict
    revisionDiffByFiles = defaultdict(list)
    filesCounter = 0
    for line in file:
      line = line.replace('\n', '')
      if line == filesSeparator:
        #print(line)
        filesCounter += 1
        revisionDiffByFiles[filesCounter] = [filesSeparator]
        continue

      #print(line)
      revisionDiffByFiles[filesCounter].append(line)

    #print(revisionDiffByFiles)
    linesFromCodeFiles = []
    linesFromXmlFiles = []
    numberOfRemainingFiles = 0
    for fileNum in revisionDiffByFiles:
      if (len(revisionDiffByFiles[fileNum]) < 3):
        continue

      fileDefinition = revisionDiffByFiles[fileNum][1]
      if not fileDefinition[0:3] == '---':
        continue

      fileName = os.path.basename(fileDefinition.split(' ')[1].split('\t')[0])
      codeFile = fileName.endswith('.cpp') or fileName.endswith('.h') or fileName.endswith('.txt') or fileName.endswith('.lsp')
      if codeFile:
        linesFromCodeFiles.append(revisionDiffByFiles[fileNum])
      elif fileName.endswith('.xml'):
        linesFromXmlFiles.append(revisionDiffByFiles[fileNum])
      else:
        numberOfRemainingFiles += 1

    addedLines, removedLines = linesCounter(linesFromCodeFiles)
    xmlLinesAdded, xmlLinesRemoved = linesCounter(linesFromXmlFiles)

    authorName = revisionAuthorDict[revision]
    if not authorName in authorDataDict:
      authorDataDict[authorName] = []

    authorDataDict[authorName].append([revision, addedLines, removedLines, xmlLinesAdded, numberOfRemainingFiles])
