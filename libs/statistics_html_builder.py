import os
import os.path

def buildHtmlStatistics(authorStatDict):
  if not os.path.exists('./statistics'):
    os.makedirs('./statistics')

  indexFile = open('./statistics/index.html', 'w+')
  indexFile.write('<!doctype html>' + '\n')
  indexFile.write('<html>' + '\n')
  indexFile.write('  <head>' + '\n')
  indexFile.write('    <title>Developers statistics</title>' + '\n')
  indexFile.write('  </head>' + '\n')
  indexFile.write('  <body>' + '\n')
  indexFile.write('    <center>' + '\n')
  indexFile.write('      <table Align="center" Border="2" width="300">' + '\n')
  indexFile.write('        <tr align="center">' + '\n')
  indexFile.write('          <td><b>Developer Nickname</b></td>' + '\n')
  indexFile.write('        </tr>' + '\n')
  for author in authorStatDict:
    #add developer to the index page
    indexFile.write('        <tr align="center">' + '\n')
    indexFile.write('          <td><a href="{0}.html"><i>{0}</i></a></td>'.format(author) + '\n')
    indexFile.write('        </tr>' + '\n')

    #add personal developer statistics
    outputResults = open('./statistics/{0}.html'.format(author), 'w+')
    outputResults.write('<!doctype html>' + '\n')
    outputResults.write('<html>' + '\n')
    outputResults.write('  <head>' + '\n')
    outputResults.write('    <title>{0} statistics</title>'.format(author) + '\n')
    outputResults.write('  </head>' + '\n')
    outputResults.write('  <body>' + '\n')
    outputResults.write('    <center>' + '\n')
    outputResults.write('      <table Align="center" Border="2" width="600">' + '\n')
    outputResults.write('        <tr align="center">' + '\n')
    outputResults.write('          <td><b>Revision</b></td><td><b>Added</b></td><td><b>Removed</b></td><td><b>Xml Lines Added</b></td><td><b>.sat, .osm, .dwg, etc.</b></td>' + '\n')
    outputResults.write('        </tr>' + '\n')
    totalAdded = 0
    totalRemoved = 0
    totalXmlAdded = 0
    totalOtherFilesNum = 0
    for item in authorStatDict[author]:
      totalAdded += item[1]
      totalRemoved += item[2]
      totalXmlAdded += item[3]
      totalOtherFilesNum += item[4]
      outputResults.write('        <tr align="center">' + '\n')
      outputResults.write('          <td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td>'.format(item[0], item[1], item[2], item[3], item[4]) + '\n')
      outputResults.write('        </tr>' + '\n')

    outputResults.write('        <tr align="center">' + '\n')
    outputResults.write('          <td>Total:</td><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>'.format(totalAdded, totalRemoved, totalXmlAdded, totalOtherFilesNum) + '\n')
    outputResults.write('        </tr>' + '\n')
    outputResults.write('        <tr align="center">' + '\n')
    outputResults.write('          <td><a href="index.html"><i>Developers List</i></td>' + '\n')
    outputResults.write('        </tr>' + '\n')
    outputResults.write('      </table>' + '\n')
    outputResults.write('    </center>' + '\n')
    outputResults.write('  </body>' + '\n')
    outputResults.write('</html>' + '\n')

  indexFile.write('      </table>' + '\n')
  indexFile.write('    </center>' + '\n')
  indexFile.write('  </body>' + '\n')
  indexFile.write('</html>' + '\n')
