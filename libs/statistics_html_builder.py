import os
import os.path

def buildHtmlStatistics(authorStatDict):
  if not os.path.exists('./statistics'):
    os.makedirs('./statistics')
  for author in authorStatDict:
    outputResults = open('./statistics/{0}.html'.format(author), 'w+')
    outputResults.write('<!doctype html>' + '\n')
    outputResults.write('<html>' + '\n')
    outputResults.write('  <head>' + '\n')
    outputResults.write('    <title>{0} statistics</title>'.format(author) + '\n')
    outputResults.write('  </head>' + '\n')
    outputResults.write('  <body>' + '\n')
    outputResults.write('    <center>' + '\n')
    outputResults.write('      <table Align="center" Border="2" width="300">' + '\n')
    outputResults.write('        <tr>' + '\n')
    outputResults.write('          <td><b>Revision</b></td><td><b>Added</b></td><td><b>Removed</b></td>' + '\n')
    outputResults.write('        </tr>' + '\n')
    totalAdded = 0
    totalRemoved = 0
    for item in authorStatDict[author]:
      totalAdded += item[1]
      totalRemoved += item[2]
      outputResults.write('        <tr>' + '\n')
      outputResults.write('          <td>{0}</td><td>{1}</td><td>{2}</td>'.format(item[0], item[1], item[2]) + '\n')
      outputResults.write('        </tr>' + '\n')
      outputResults.write('\n')

    outputResults.write('        <tr>' + '\n')
    outputResults.write('          <td>Total:</td><td>{0}</td><td>{1}</td>'.format(totalAdded, totalRemoved) + '\n')
    outputResults.write('        </tr>' + '\n')
    outputResults.write('      </table>' + '\n')
    outputResults.write('    </center>' + '\n')
    outputResults.write('  </body>' + '\n')
    outputResults.write('</html>' + '\n')
    outputResults.write('\n')