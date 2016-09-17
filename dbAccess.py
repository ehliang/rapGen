# -*- coding: utf-8 -*-
import pymssql

conn = pymssql.connect(tds_version='8.0', server='rapgen2.database.windows.net', user='ankai@rapgen2', password='Hackathon123!', database='rapgen2') 
cursor = conn.cursor()

def addWord(word, syllables, postag, iterFreq=1):
	iterFreq = str(iterFreq)
	wordq = '\'' + word + '\''
	postagq = '\'' + postag + '\''
	cursor.execute('SELECT * from RapData.Words where word=' + wordq);
	row = cursor.fetchone()
	if row is None:
		cursor.execute('Insert into RapData.Words values (' + wordq + ',' + str(syllables) + ', ' + iterFreq + ', ' + postagq + ')')
	else:
		cursor.execute('UPDATE Rapdata.Words SET frequency = frequency + ' + iterFreq + ' WHERE word = ' + wordq)
	conn.commit()

def addNextLongestMap(rootWord, targWord):
	cursor.execute('SELECT id from RapData.Words where word=\'' + rootWord + '\'');
	rootId = str(cursor.fetchone()[0])
	cursor.execute('SELECT id from RapData.Words where word=\'' + targWord + '\'');
	targId = str(cursor.fetchone()[0])

	cursor.execute('SELECT edge_id from RapData.WordsNextLineLongest where root_id=' + rootId + ' and target_id= ' + targId);
	edge = cursor.fetchone()

	if edge is None:
		cursor.execute('Insert into RapData.WordsNextLineLongest values (' + rootId + ', ' + targId + ', 1 )')
	else:
		edge_id = str(edge[0])
		cursor.execute('UPDATE Rapdata.WordsNextLineLongest SET frequency = frequency + 1 WHERE edge_id = ' + edge_id)
	conn.commit()

def addToPrevMap(word, prevWord):
	cursor.execute('SELECT id from RapData.Words where word=\'' + word + '\'');
	wordId = str(cursor.fetchone()[0])
	cursor.execute('SELECT id from RapData.Words where word=\'' + prevWord + '\'');
	prevId = str(cursor.fetchone()[0])

	cursor.execute('SELECT edge_id from RapData.WordsPrevMap where word_id=' + wordId + ' and prev_id= ' + prevId);
	edge = cursor.fetchone()
	if edge is None:
		cursor.execute('Insert into RapData.WordsPrevMap values (' + wordId + ', ' + prevId + ', 1 )')
	else:
		edge_id = str(edge[0])
		cursor.execute('UPDATE Rapdata.WordsPrevMap SET frequency = frequency + 1 WHERE edge_id = ' + edge_id)
	conn.commit()

def addToWords(word, syllables, longestNext, nextSyl, prevWord, postag, nextPostag):
	addWord(word, syllables, postag)
	if longestNext is not None:
		addWord(longestNext, nextSyl, nextPostag, iterFreq=0)
		addNextLongestMap(word, longestNext)

	if prevWord is not None:
		addToPrevMap(word, prevWord)
	conn.commit()

def addToLineStructs(structArr):
	for struct in structArr:
		struct = '\'' + struct + '\''

		cursor.execute('SELECT id from RapData.Structures where structure=' + struct);
		sid = cursor.fetchone()
		if sid is None:
			cursor.execute('Insert into RapData.Structures values (' + struct + ', 1 )')
		else:
			sid = str(sid[0])
			cursor.execute('UPDATE Rapdata.Structures SET frequency = frequency + 1 WHERE id = ' + sid)

	conn.commit()


def getPrevFromWord(word):
	wordq = '\'' + word + '\''
	# cursor.execute('select word_id, w.word, prev_id, prev_word, prev_syllables, \
	# prev_postag, prevmap.frequency from rapdata.words w \
	# left join \
	# 	(select map.word_id, map.prev_id, word.word as prev_word,\
	# 	word.syllables as prev_syllables, word.postag as prev_postag, map.frequency from rapdata.wordsprevmap map \
	# 	left join rapdata.words word on map.prev_id = word.id) prevmap\
	# on w.id = prevmap.word_id where w.word =' + wordq);

	cursor.execute('SELECT id from RapData.words where word=' + wordq)
	wordid = cursor.fetchone()
	if word:
		wordid = str(wordid[0])
	else:
		return None

	cursor.execute('select id, word, syllables, postag, map.frequency from rapdata.wordsprevmap map \
	 left join rapdata.words word on map.prev_id = word.id \
	 where map.word_id=' + wordid)

	prev_arr=[]
	row = cursor.fetchone()
	while row:
		prev_arr.append({
			'id': row[0],
			'word': str(row[1]),
			'syllables': row[2],
			'postag': str(row[3]),
			'frequency': row[4]
			})
		row = cursor.fetchone()

	return prev_arr

def getLongsFromWord(word):
	wordq = '\'' + word + '\''

	cursor.execute('SELECT id from RapData.words where word=' + wordq)
	wordid = cursor.fetchone()
	if word:
		wordid = str(wordid[0])
	else:
		return None

	cursor.execute('select id, word, syllables, postag, map.frequency from rapdata.WordsNextLineLongest map \
	 left join rapdata.words word on map.target_id = word.id \
	 where map.root_id=' + wordid)

	prev_arr=[]
	row = cursor.fetchone()
	while row:
		prev_arr.append({
			'id': row[0],
			'word': str(row[1]),
			'syllables': row[2],
			'postag': str(row[3]),
			'frequency': row[4]
			})
		row = cursor.fetchone()

	return prev_arr

def getWordAttributes(word):
	wordq = '\'' + word + '\''
	cursor.execute('SELECT id, word, syllables, postag, frequency from RapData.words where word=' + wordq)
	row = cursor.fetchone()
	if row:
		return {
			'id': row[0],
			'word': str(row[1]),
			'syllables': row[2],
			'postag': str(row[3]),
			'frequency': row[4]
		}
	else:
		return None

def getWordsWithTag(tag):
	tagq = '\'' + tag + '\''
	cursor.execute('SELECT id, word, syllables, postag, frequency from RapData.words where postag=' + tagq)
	row = cursor.fetchone()
	wordarr = []
	while row:
		wordarr.append({
			'id': row[0],
			'word': str(row[1]),
			'syllables': row[2],
			'postag': str(row[3]),
			'frequency': row[4]
			})
		row = cursor.fetchone()
	return wordarr

def getTopTagSequences(limit):
	cursor.execute('SELECT top ' + str(limit) + ' structure, frequency from RapData.structures order by frequency desc')
	res = cursor.fetchall()
	return [{'postag': str(x[0]), 'frequency': x[1]} for x in res]

print(getPrevFromWord('fired'))
print(getLongsFromWord('fired'))
print(getWordAttributes('fired'))
print(getWordsWithTag('NN'))
print(getTopTagSequences(1))

# addWord('Previous', 3, 'VV')
# addToWords('Test', 1, 'Next', 1, 'Previous', 'NN', 'NN')
#addToLineStructs(['VV NN PV', 'VV NN PV', 'NN NN NN'])

