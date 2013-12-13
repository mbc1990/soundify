import fuzzy
import Levenshtein as pylev

wordlist = []

def initialize():
  global wordlist
  words = [] 
  with open('/usr/share/dict/words') as f:
    words = f.readlines()
  for w in words:
    if not w[0].isupper():
    	wordlist.append( (w, fuzzy.nysiis(w)) )

def find_similar(word):
  word_sound = fuzzy.nysiis(word)
  best = None 
  best_dist = 99999
  for w in wordlist:
    if pylev.distance(word_sound, w[1]) < best_dist and word != w[0][:-1]:
      best_dist = pylev.distance(word_sound, w[1])
      best = (w[0], best_dist)
  return best    

def soundify(word):
	table = []
	table.append( ('', 0) ) 
	word = fuzzy.nysiis(word)
	for n in range(1,len(word)):
		opt_n_score = 99999
		opt_n_obj = None
		for m in range(0, n):
			opt_m = table[m]
			remaining = find_similar(word[m:n])
			if opt_m[1] + remaining[1] < opt_n_score:
				opt_n_score = opt_m[1] + remaining[1]
				opt_n_obj = (opt_m[0]+' '+remaining[0], opt_m[1] + remaining[1])
		print n
		table.append(opt_n_obj)
	return table[-1]
			
print "initializing"
initialize()
print "done"
while True:
	inp = raw_input("String to soundify: ")
	out = soundify(inp)
	print out[0].split('\n')[:-1]
  
