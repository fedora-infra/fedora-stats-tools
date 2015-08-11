# BackStory
# October 9th, 2012 is when Datagrepper came online
# 2012-2013 is missing 2 months worth of Karma Messages

import pygal

chart = pygal.Bar(fill=True, title='Bodhi Karma, YoY on August', x_title='*2012 missing 2 months of fedmsg data (Datagrepper not deployed until October 9th)')
chart.add('2012-2013', [{'value': 7140, 'style': 'stroke:red; stroke-width: 10'}])
chart.add('2013-2014', [16807])
chart.add('2014-2015', [19102])

# 2012-2013   7140
# 2013-2014   16807
# 2014-2015   19102

anonchart = pygal.Bar(fill=True, title='Bodhi Anonymous Karma, YoY on August', x_title='*2012 missing 2 months of fedmsg data (Datagrepper not deployed until October 9th)')
anonchart.add('2012-2013', [{'value': 230, 'style': 'stroke:red; stroke-width: 10'}])
anonchart.add('2013-2014', [462])
anonchart.add('2014-2015', [370])

# 2012-2013     230
# 2013-2014     462
# 2014-2015     370


chart.render_to_file('karmabodhi.svg')
anonchart.render_to_file('anonkarmabodhi.svg')

# anonchart.render_to_png('anonkarmabodhi.png')
# chart.render_to_png('karmabodhi.png')
