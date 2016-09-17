# -*- coding: utf-8 -*-
import nltk
import requests
import dbAccess

apiString = "&apikey=ca5515a3e14ca1f16d19c54f9a98c5a7"
url = 'http://api.musixmatch.com/ws/1.1/'
mGraphApi = 'http://api.musicgraph.com/api/v2/'
mGraphString = 'e6a54a7a422f513be9590d65b7c0c618'

def getAllArtistTracks(name):
	name = '%20'.join(name.split())
	query = mGraphApi + 'artist/suggest?api_key=' + mGraphString + '&prefix=' + name + '&limit=1'

	res = requests.get(query)
	data = res.json()
	aid = data['data'][0]['id']

	query2 = mGraphApi + 'artist/' + aid + '/tracks' + '?api_key=' + mGraphString
	res = requests.get(query2)
	trackdata = res.json()['data']

	title_arr = []
	for track in trackdata:
		title_arr.append(str(track['title']))

	return title_arr


def getArtistId(name):
	name = '%20'.join(name.split())
	query = url + 'artist.search?q_artist=' + name + '&page_size=5' + apiString
	res = requests.get(query)
	data = res.json()
	print(data)

def getTrackId(artist, track):
	artist = '%20'.join(artist.split())
	track = '%20'.join(track.split())
	query = url + 'track.search?q_track=' + track + '&q_artist=' + artist + '&page_size=5&f_has_lyrics=1' + apiString
	res = requests.get(query)
	data = res.json()
	try:
		tid = data['message']['body']['track_list'][0]['track']['track_id']
		return tid
	except IndexError:
		return None

def getTrackLyrics(tid):
	if tid is None:
		return ''
	query = url + 'track.lyrics.get?track_id=' + str(tid) + apiString
	res = requests.get(query)
	data = res.json()
	lyrics = data['message']['body']['lyrics']['lyrics_body']
	return lyrics

def cleanLyrics(raw):
	end = raw.find('***')
	raw = raw[:end].replace('...', ' ').replace('\n\n', '\n').strip()
	return raw

def getLongestWord(line):
	if line is None:
		return None
	else:
		return max(line.split(), key=len)


def count_syl(word):
	if word is None:
		return None
	# Count the syllables in the word.
	syllables = 0
	for i in range(len(word)) :

		# If the first letter in the word is a vowel then it is a syllable.
		if i == 0 and word[i] in "aeiouy" :
			syllables = syllables + 1

		# Else if the previous letter is not a vowel.
		elif word[i - 1] not in "aeiouy" :

		  # If it is no the last letter in the word and it is a vowel.
			if i < len(word) - 1 and word[i] in "aeiouy":
				syllables = syllables + 1

		  # Else if it is the last letter and it is a vowel that is not e.
			elif i == len(word) - 1 and word[i] in "aiouy":
				syllables = syllables + 1

	# Adjust syllables from 0 to 1.
	if len(word) > 0 and syllables == 0 :
		syllables == 0
		syllables = 1

	return syllables


def lyricsToData(lyrics):
	lyricsArr = []
	lyrics = cleanLyrics(lyrics)
	arr = lyrics.split('\n')
	for idx, line in enumerate(arr):
		nextLine = None
		if idx < len(arr)-1:
			nextLine = arr[idx+1]
		linesplit = line.split(' ')
		for widx, word in enumerate(linesplit):
			prevWord = None
			if widx > 0:
				prevWord = linesplit[widx-1].lower().replace("'", "")

			word = word.lower().replace("'", "")
			longestNext = getLongestWord(nextLine)
			syllables = count_syl(word)
			nextSyl = count_syl(longestNext)
			pos_tag = nltk.pos_tag([word])[0][1][0:2]
			next_pos_tag = None
			if longestNext is not None:
				longestNext = longestNext.lower().replace("'", "")
				next_pos_tag = nltk.pos_tag([longestNext])[0][1][0:2]
			wDict = {}
			wDict['word'] = word
			wDict['syllables'] = syllables
			wDict['longNext'] = longestNext
			wDict['longNextSyl'] = nextSyl
			wDict['prevWord'] = prevWord
			wDict['pos_tag'] = pos_tag
			wDict['next_pos_tag'] = next_pos_tag
			lyricsArr.append(wDict)

	return lyricsArr

def lyricsToLineData(lyrics):
	lyricsArr = []
	lyrics = cleanLyrics(lyrics)
	arr = lyrics.split('\n')
	for idx, line in enumerate(arr):
		tags = nltk.pos_tag(line.split())
		lyricsArr.append(tags)

	tagArr = []
	for arr in lyricsArr:
		arr = [x[1][0:2] for x in arr]
		arr = ' '.join(arr)
		tagArr.append(arr)

	return tagArr


def pushWordsToDb (arr):
	for wDict in arr:
		print(wDict)
		dbAccess.addToWords(wDict['word'], wDict['syllables'],wDict['longNext'],
			wDict['longNextSyl'], wDict['prevWord'], wDict['pos_tag'], 
			wDict['next_pos_tag'])

def pushLineStructToDb(arr):
	dbAccess.addToLineStructs(arr)


# Push all lyrics data to database
def pushLyricsToDb(lyrics):
	wArr = lyricsToData(lyrics)
	structArr = lyricsToLineData(lyrics)
	pushWordsToDb(wArr)
	pushLineStructToDb(structArr)





# getTrackLyrics(getTrackId('kanye west', 'amazing'))

sample_lyrics = "Everybody fired up this evening\nI'm exhausted barely breathing\nHolding on to what I believe in\nNo matter what you'll never take that from me\n\nMy reign is as far as your eyes can see... its amazing\nSo amazing, so amazing\nSo amazing, it's amazing\nSo amazing, so amazing\nSo amazing, it's amazing\nI'm a monster I'm a killer\n\nI know I'm wrong\nI'm a problem\nThat will never ever be solved\nNo matter what you'll never take that from me\n\nMy reign is as far as your eyes can see... it's amazing\nSo amazing, so amazing\nSo amazing, it's amazing\n...\n\n******* This Lyrics is NOT for Commercial use *******"
sample_lyrics = "Everybody fired up this evening\nI'm exhausted barely breathing"
pushLyricsToDb(sample_lyrics)

# kanyelist = getAllArtistTracks('kanye west')
# for song in kanyelist:
# 	print cleanLyrics(getTrackLyrics(getTrackId('kanye west', song)))