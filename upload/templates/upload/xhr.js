{% load thumbnail upload_tags %}{% thumbnail path 180x180 crop=crop as t %}{'id':{{ id }},'url':'{{ t.url|fixurl }}'}
