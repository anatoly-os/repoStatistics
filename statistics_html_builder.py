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
    for item in authorStatDict[author]:
      outputResults.write('        <tr>' + '\n')
      outputResults.write('          <td>')
      outputResults.write(str(item))
      outputResults.write('          </td>' + '\n')
      outputResults.write('        </tr>' + '\n')
      outputResults.write('\n')

    outputResults.write('      </table>' + '\n')
    outputResults.write('    </center>' + '\n')
    outputResults.write('  </body>' + '\n')
    outputResults.write('</html>' + '\n')
    outputResults.write('\n')