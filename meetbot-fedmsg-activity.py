#!/usr/bin/env python
""" Make an index page where you can find datagrepper stuff. """

import jinja2


topics = [
  'org.fedoraproject.prod.meetbot.meeting.item.agreed',
  'org.fedoraproject.prod.meetbot.meeting.item.accepted',
  'org.fedoraproject.prod.meetbot.meeting.item.rejected',
  'org.fedoraproject.prod.meetbot.meeting.item.action',
  'org.fedoraproject.prod.meetbot.meeting.item.info',
  'org.fedoraproject.prod.meetbot.meeting.item.idea',
  'org.fedoraproject.prod.meetbot.meeting.item.help',
  'org.fedoraproject.prod.meetbot.meeting.item.link',
]
keyword_sets = [
  ('blocker',),
  ('design',),
  ('documentation', 'docs',),
  ('security', 'infosec',),
  ('epel',),
  ('infra',),
  ('i18n',),
  ('g18n',),
  ('marketing',),
  ('mktg',),
  ('magazine',),
  ('qa', 'quality',),
  ('ask',),
  ('commops',),
  ('fesco',),
  ('council',),
  ('ambassadors', 'fasmco', 'fasmna'),
]


keywords = dict([
    (kws[0], '&contains='.join(kws),)
    for kws in keyword_sets
])

baseurl = 'https://apps.fedoraproject.org/datagrepper/raw'

template = jinja2.Template("""
<html> <body>

<table>
    {% for topic in topics %}
        <tr>
        <td>{{topic.split('.')[-1]}}</td>
        {% for name, contains in keywords.items() %}
            <td>
            <a href="{{baseurl}}?contains={{contains}}&topic={{topic}}">{{name}}</a>
            </td>
        {% endfor %}
        </tr>
    {% endfor %}
</table>

</body> </html>
""")

print template.render(topics=topics, keywords=keywords, baseurl=baseurl)
