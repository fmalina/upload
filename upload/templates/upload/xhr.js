{% load thumbnail %}{% thumbnail path 180x180 crop=crop as t %}{'id':{{ id }},'url':'{{ t.absolute_url }}'}
