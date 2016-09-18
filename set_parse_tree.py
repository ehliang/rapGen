import nltk
import re
import random
import pronouncing
from nltk.corpus import words
import azure_query as aq
import dbAccess as db

PARSE_TREE = [['NN', 'VB', 'JJ', 'NN', 'CC', 'VB', 'NN'],
			  ['NN', 'CC', 'VB', 'NN']]

def weighted_choice(word_dict):
	choices = word_dict.items()
	total = sum(w for c, w in choices)
	r = random.uniform(0, total)
	upto = 0
	for c, w in choices:
	   if upto + w >= r:
		  return c
	   upto += w
	assert False

class MarkovModel():
	tag = lambda self, x: nltk.pos_tag([x])[0][1][0:2]
	def __init__(self):
		tag_list = nltk.data.load('help/tagsets/upenn_tagset.pickle').keys()
		tag_set = set([tag[0:2] for tag in tag_list])
		#self.lib = dict(zip(tag_set, [{} for x in range(len(tag_set))]))
		#self.master = {}
		#self.add_to_lib('allLyrics.txt')
		self.aq = aq.Requests()

	# this function was used for testing before db came along
	'''
	def add_to_lib(self, fileName):
		file = open(fileName, 'r')
		words = re.sub("-"," ", re.sub("[\.!@#\$,)(?/]", "", file.read())).split('\n')
		for i, line in enumerate(words):
			#print words[i]
			if len(line) == 0: continue
			#print len(line)
			k = line.split(' ')
			if k[-1] == '': k.pop()
			words[i] = nltk.pos_tag(k)
			cur = len(words[i]) - 1
			line = words[i]
			while cur > 0:
			#looping through reverse 
				cur_word = line[cur][0]
				prev_word = line[cur - 1][0]
				if cur_word in ['', ' ', '\n']:
					cur -= 1
					continue
				cur_word_tag = line[cur][1][0:2]
				# if the word is in the lib
				#print cur_word, prev_word, len(cur_word)
				if cur_word in self.lib[cur_word_tag].keys():
					if prev_word in self.lib[cur_word_tag][cur_word].keys():
						#if we've seen the sequence currWord -> nextWord before
						self.lib[cur_word_tag][cur_word][prev_word] += 1
					else:
						#haven't seen sequence currWord -> nextWord before
						self.lib[cur_word_tag][cur_word][prev_word] = 1
				else:
					# we start a dictionary if we have not seen this word.
					self.lib[cur_word_tag][cur_word] = {prev_word: 1}
				cur -= 1

				if cur_word not in self.master.keys():
					self.master[cur_word] = 1
				else:
					self.master[cur_word] += 1
	'''
	def markov_prev(self, cur_word, cur_word_tag, prev_word_tag):
		cur_word_dict = db.getWordAttributes(cur_word)
		if cur_word_dict == None: return random.choice([x['word'] for x in db.getWordsWithTag(cur_word_tag)])
		prev_word_options = db.getPrevFromWord(cur_word)
		valid_words = filter(lambda word: prev_word_tag == nltk.pos_tag([word['postag'], cur_word])[0][1][0:2],
							prev_word_options)
		if len(valid_words) == 0:
			return random.choice([x['word'] for x in db.getWordsWithTag(prev_word_tag)])
		else: 
			return random.choice([x['word'] for x in valid_words])

	def line_gen2(self, end_word, line_length):
		line, wc = '', 0
		i = 0
		for seq in ['NN', 'VB']:
			possible_words = db.getWordsWithTag(seq)
			rand_num = random.randint(0, len(possible_words) - 1)
			line = possible_words[rand_num]['word'] + ' ' + line[:-1]
		if self.aq.validate(line) > -10:
			while True:
				word_list = []
				try:
					line = self.aq.next_word(line)
				except:
					word_list = []
					for k in range(100):
						word_list.append(db.getWordsWithTag('JJ'))
					line = self.aq.next_prob(line, word_list) 
				if (i > line_length and nltk.pos_tag(line.split(" "))[-1][1][0:2] in ['NN', 'VB']) or i > line_length + 3:
					break
				i += 1
		else:
			self.line_gen2(end_word,line_length)
		v = self.aq.validate(line)
		if  v > -11:
			return line
		return ''

	def line_gen(self, end_word):
		wc = 0
		cur = end_word
		line = end_word
		reverse = random.choice(PARSE_TREE)[::-1]
		for i, seq in enumerate(reverse[:-1]):
			cur = self.markov_prev(cur, seq, reverse[i + 1])
			line = cur + ' ' + line
			if cur == False: return line
		return line

	def generate_rhymes(self, n, sameword = True):
		rap = ''
		rhymes = []
		last_word = 'now'
		k = None
		while(True):
			k = self.line_gen2(last_word, 3)
			if (k == ''): continue
			last_word = k.split()[-1]
			list_of_rhymes = pronouncing.rhymes(last_word)
			if (len(list_of_rhymes) != 0): break
		rhymes.append(k)
		for i in range(n - 1):
			if sameword == False:
				last_word = random.choice(list_of_rhymes).replace("'", "")
			print "happens"
			rhymes.append(self.line_gen(last_word))
		print n
		return rhymes

if __name__ == "__main__":
	d = MarkovModel()
	for i in range(2):
		print 1, i
		print d.generate_rhymes(2, True)
		print 2, i
		print d.generate_rhymes(3, False)
		print 3, i
		print d.generate_rhymes(2, False)
