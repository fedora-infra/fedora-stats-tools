import requests

seconds = 365 * 24 * 60 * 60

categories = ['anitya', 'ansible', 'askbot', 'bodhi', 'bugzilla', 'buildsys',
              'compose', 'copr', 'datnommer', 'faf', 'fas', 'fedbadges',
              'fedimg', 'fedocal', 'fedora_elections', 'fedoratagger', 'fmn',
              'git', 'github', 'hotness', 'irc', 'jenkins', 'kerneltest',
              'koschei', 'mailman', 'meetbot', 'mirrormanager', 'nuancier',
              'pagure', 'pkgdb', 'planet', 'summershum', 'trac', 'wiki',
              'zanata']

print seconds
response = requests.get('https://apps.fedoraproject.org/datagrepper/raw?delta=%i' % seconds)
print response.json().keys()

# [u'count', u'raw_messages', u'total', u'arguments', u'pages']

print response.json()['total']
# 23291693


