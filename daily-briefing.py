#!/usr/bin/env python
""" Make an index page where you can find datagrepper stuff. """

import jinja2
import arrow

docs_links = [
    "http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/Virtualization_Deployment_and_Administration_Guide/index.html",
    "https://fedoraproject.org/wiki/Virt_Getting_Started_Planning has the current TOC",
    "https://fedoraproject.org/wiki/Category:Docs_Project_tasks?rd=Docs_Project_tasks is the guide task list",
    ]

trans_links = [
    "http://unicode.org/cldr/trac/ticket/8683",
    "https://fedorahosted.org/i18n/ticket/51",
    "https://fedoraproject.org/wiki/Changes/Unicode_8.0",
    "https://fedorahosted.org/i18n/ticket/50",
    "https://fedorahosted.org/i18n/ticket/49",
    "https://fedorahosted.org/i18n/ticket/43",
    "https://fedoraproject.org/wiki/I18N/Meetings/2015-06-24",
    ]

ambassadors_links = []
ask_links = []
blocker_links = []
commops_links = []
council_links = []
design_links = []
epel_links = []
fesco_links = []
infra_links = []
magazine_links = []
marketing_links = []
qa_links = []
security_links = []
marketing_links = []
cloudwg_links = []
serverwg_links = []
workstationwg_links = []
basewg_links = []
stacksenvwg_links = []
websites_links = []
sig_links = []


template = jinja2.Template("""
<html> <body>

<h1>Daily Briefing</h1>

{% if ambassadors_links: %}
<h2>Ambassadors</h2>
    <ul>
        {% for link in ambassadors_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if ask_links: %}
<h2>Ask</h2>
    <ul>
        {% for link in ask_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if blocker_links: %}
<h2>Blocker</h2>
    <ul>
        {% for link in blocker_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if commops_links: %}
<h2>CommOps</h2>
    <ul>
        {% for link in commops_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if council_links: %}
<h2>Council</h2>
    <ul>
        {% for link in council_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if design_links: %}
<h2>Design</h2>
    <ul>
        {% for link in design_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if docs_links: %}
<h2>Documentation:</h2>
    <ul>
        {% for link in docs_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if epel_links: %}
<h2>EPEL</h2>
    <ul>
        {% for link in docs_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if fesco_links: %}
<h2>FESCo</h2>
    <ul>
        {% for link in docs_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if infra_links: %}
<h2>Infrastructure</h2>
    <ul>
        {% for link in docs_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if magazine_links: %}
<h2>Magazine</h2>
    <ul>
        {% for link in docs_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if marketing_links: %}
<h2>Marketing</h2>
    <ul>
        {% for link in docs_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if qa_links: %}
<h2>Q&amp;A</h2>
    <ul>
        {% for link in docs_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if security_links: %}
<h2>Security</h2>
    <ul>
        {% for link in docs_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}

{% if trans_links: %}
<h2>Translation</h2>
    <ul>
        {% for link in trans_links: %}
            <li><a target="_blank" href="{{link}}">{{link}}</a></li>
        {% endfor %}
    </ul>
{% endif %}



</body> </html>
""")

output = template.render(docs_links=docs_links, trans_links=trans_links)

with open('{}-brief.html'.format(arrow.now().format()[0:10]), "wb") as f:
        f.write(output)
