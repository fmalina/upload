{% load thumbnail %}{% thumbnail path 'medium' crop=crop as thumb %}{'id':{{ id }},'url':'{{ thumb }}'}
