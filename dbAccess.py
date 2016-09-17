# -*- coding: utf-8 -*-
import pymssql

conn = pymssql.connect(tds_version='8.0', server='rapgen2.database.windows.net', user='ankai@rapgen2', password='Hackathon123!', database='rapgen2')  
cursor = conn.cursor()

def addWord(word, syllables, iterFreq=1):
	iterFreq = str(iterFreq)
	wordq = '\'' + word + '\''
	cursor.execute('SELECT * from RapData.Words where word=\'' + word + '\'');
	row = cursor.fetchone()
	if row is None:
		cursor.execute('Insert into RapData.Words values (' + wordq + ',' + str(syllables) + ', ' + iterFreq + ')')
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

def addToWords(word, syllables, longestNext, nextSyl, prevWord):
	addWord(word, syllables)
	if longestNext is not None:
		addWord(longestNext, nextSyl, iterFreq=0)
		addNextLongestMap(word, longestNext)

	if prevWord is not None:
		addToPrevMap(word, prevWord)
	conn.commit()








# cursor.execute('SELECT c.CustomerID, c.CompanyName,COUNT(soh.SalesOrderID) AS OrderCount FROM SalesLT.Customer AS c LEFT OUTER JOIN SalesLT.SalesOrderHeader AS soh ON c.CustomerID = soh.CustomerID GROUP BY c.CustomerID, c.CompanyName ORDER BY OrderCount DESC;')  
# row = cursor.fetchone()  
# while row:  
#     print row
#     row = cursor.fetchone()
addToWords('Test', 1, 'Next', 1, 'Previous')

