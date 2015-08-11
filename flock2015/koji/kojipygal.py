# BackStory
# October 9th, 2012 is when Datagrepper came online
# 2012-2013 is missing 2 months worth of Karma Messages

import pygal

# Charts
# Total Builds (3 years)
# Secondar (2 years)
# Primary (2 years)
# COPR Builds (1 years)

kojichart = pygal.Bar(fill=True, title='Koji Builds, YoY on August')
kojichart.add('2012-2013', [66684])
kojichart.add('2013-2014', [233559])
kojichart.add('2014-2015', [470024.5])

# 66684
# 233559
# 470024.5

primarychart = pygal.Bar(fill=True, title='Koji Primary Arch Builds, YoY on August')
primarychart.add('2013-2014', [60505])
primarychart.add('2014-2015', [148415])

# 60505
# 148415


secondarychart = pygal.Bar(fill=True, title='Koji Secondary Arch Builds, YoY on August')
secondarychart.add('2013-2014', [6179])
secondarychart.add('2014-2015', [85144])

# 6179
# 85144


coprchart = pygal.Bar(fill=True, title='COPR Builds, YoY on August')
coprchart.add('2013-2014', [64285])
coprchart.add('2014-2015', [193176])

# 64285
# 193176

kojivcoprchart = pygal.Bar(fill=True, title='Koji v COPR Builds, YoY on August')
kojivcoprchart.add('Koji', [60505, 148415])
kojivcoprchart.add('COPR', [64285, 193176])


kojichart.render_to_file('kojitotal.svg')
primarychart.render_to_file('kojiprimary.svg')
secondarychart.render_to_file('kojisecondary.svg')
coprchart.render_to_file('copr.svg')
kojivcoprchart.render_to_file('kojivcopr.svg')

# anonchart.render_to_png('anonkarmabodhi.png')
# chart.render_to_png('karmabodhi.png')
