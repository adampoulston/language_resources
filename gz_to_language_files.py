# -*- coding: UTF-8 -*-
'''
	Quick and dirty script to convert a list of gzipped tweet files
	into another list of cut down tweet files separated by language and geolocation info
'''
import json
import os
import gzip
from datetime import datetime
import shapefile as sfl
from shapely.geometry import Polygon, box, Point, LineString, LinearRing
###CODE to lookup country the coordinate falls in
#file source: http://thematicmapping.org/downloads/world_borders.php
sf_path = "TM_WORLD_BORDERS-03/TM_WORLD_BORDERS-03"
r = sfl.Reader(sf_path)
shapes = r.shapes()
records = r.records()
shapely_shapes = []
shapely_records = []
for idx, shape in enumerate(shapes):
	if len(shape.parts) == 1:
		shapely_shapes.append(Polygon(shape.points))
		shapely_records.append(records[idx])
	else:
		for p_idx in range(len(shape.parts)-1):
			shapely_shapes.append(Polygon(shape.points[shape.parts[p_idx]:shape.parts[p_idx+1]]))
			shapely_records.append(records[idx])
		shapely_shapes.append(Polygon(shape.points[len(shape.parts):]))
		shapely_records.append(records[idx])

def which_area(x, y):
    idx = 0
    p = Point(x, y)
    for s in shapely_shapes:
        if s.contains(p):
            return idx
        idx += 1
    return None

def which_iso(x,y):
	a = which_area(x,y)
	if a:
		return shapely_records[a][1].lower()
	else:
		return a
### END of country lookup code
#directory to stored processed gzipped tweets in
t_dir = ""

#Twitter supported languages
#TODO: infer this automatically from API
langs = [{u'status': u'production', u'code': u'fr', u'name': u'French'}, {u'status': u'production', u'code': u'en', u'name': u'English'}, {u'status': u'production', u'code': u'ar', u'name': u'Arabic'}, {u'status': u'production', u'code': u'ja', u'name': u'Japanese'}, {u'status': u'production', u'code': u'es', u'name': u'Spanish'}, {u'status': u'production', u'code': u'de', u'name': u'German'}, {u'status': u'production', u'code': u'it', u'name': u'Italian'}, {u'status': u'production', u'code': u'id', u'name': u'Indonesian'}, {u'status': u'production', u'code': u'pt', u'name': u'Portuguese'}, {u'status': u'production', u'code': u'ko', u'name': u'Korean'}, {u'status': u'production', u'code': u'tr', u'name': u'Turkish'}, {u'status': u'production', u'code': u'ru', u'name': u'Russian'}, {u'status': u'production', u'code': u'nl', u'name': u'Dutch'}, {u'status': u'production', u'code': u'fil', u'name': u'Filipino'}, {u'status': u'production', u'code': u'msa', u'name': u'Malay'}, {u'status': u'production', u'code': u'zh-tw', u'name': u'Traditional Chinese'}, {u'status': u'production', u'code': u'zh-cn', u'name': u'Simplified Chinese'}, {u'status': u'production', u'code': u'hi', u'name': u'Hindi'}, {u'status': u'production', u'code': u'no', u'name': u'Norwegian'}, {u'status': u'production', u'code': u'sv', u'name': u'Swedish'}, {u'status': u'production', u'code': u'fi', u'name': u'Finnish'}, {u'status': u'production', u'code': u'da', u'name': u'Danish'}, {u'status': u'production', u'code': u'pl', u'name': u'Polish'}, {u'status': u'production', u'code': u'hu', u'name': u'Hungarian'}, {u'status': u'production', u'code': u'fa', u'name': u'Persian'}, {u'status': u'production', u'code': u'he', u'name': u'Hebrew'}, {u'status': u'production', u'code': u'th', u'name': u'Thai'}, {u'status': u'production', u'code': u'uk', u'name': u'Ukrainian'}, {u'status': u'production', u'code': u'cs', u'name': u'Czech'}, {u'status': u'production', u'code': u'ro', u'name': u'Romanian'}, {u'status': u'production', u'code': u'en-gb', u'name': u'British English'}, {u'status': u'production', u'code': u'vi', u'name': u'Vietnamese'}, {u'status': u'production', u'code': u'bn', u'name': u'Bengali'}]
#create a directory to store the processed tweets for each language in
for l in langs:
	try:
		os.makedirs(t_dir+l['code'])
	except Exception, e:
		#TODO: improve this handler
		print "Folder already exists(",str(e),")"

#load a list of files to process
gzipped_tweets_file = ""
gz_tweets = ["./2015_gh/"+fn.strip() for fn in open(gzipped_tweets_file)]

#open two file handles for each language, one where the tweets are geolocated and one not
lang_handles = {}
for l in langs:
	lang_handles[l['code']] = gzip.open(t_dir+l['code']+"/"+l['code'],"a+")
	lang_handles[l['code']+"_geo"] = gzip.open(t_dir+l['code']+"/"+l['code']+"_geo","a+")


try:
	i = 1
	for fn in gz_tweets:
		print "Processing:",fn,"at",
		print datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
		print "(",i,"/",len(gz_tweets),")"
		i+=1
		#open the unprocessed file
		with gzip.open(fn,"rb") as f:
			for line in f:
				try:
					tweet = json.loads(line)
					#extract the useful parts of the file
					if tweet['lang'] in lang_handles:
						out_tweet = {
							'id': 			tweet['id'],
							'u_id':			tweet['user']['id'],
							'text':			tweet['text'].replace("\n"," <newline> "),
							'lang':			tweet['lang'],
							'is_rt':		'retweeted_status' in tweet,
							'coordinates':	None,
							'coord_iso2':	None,
							'place_iso2':	None,
							'u_location':	None
						}
						#convert any tweet coordinates to a country code
						if tweet['coordinates']:
							out_tweet['coordinates'] = tweet['coordinates']['coordinates']
							out_tweet['coord_iso2'] = which_iso(*out_tweet['coordinates'])
						#extract the country code from the place object
						if tweet['place']:
							out_tweet['place_iso2'] = tweet['place']['country_code'].lower()
						#store the user's location'
						u_loc = tweet['user']['location'].strip()
						if u_loc:
							out_tweet['u_location']  = u_loc
						#write to one file if there is geo info otherwise write to other
						if out_tweet['coord_iso2'] or out_tweet['place_iso2']:
							lang_handles[out_tweet['lang']+"_geo"].write(json.dumps(out_tweet)+"\n")
						else:
							lang_handles[out_tweet['lang']].write(json.dumps(out_tweet)+"\n")
				except Exception,e:
					print "Error:",str(e)
except Exception, e:
	#TODO: improve this handler
	print "Error in main loop:",str(e)
finally:
	#close all file handles
	for gfh in lang_handles.values():
		gfh.close()




