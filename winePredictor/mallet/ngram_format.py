import sys
import json
import re
import nltk
from nltk.util import ngrams
from nltk.stem.lancaster import LancasterStemmer

# Helper function to split words and build a count-mapping
def clean_text(text_to_clean):
	# text_to_clean = text_to_clean.encode('utf8')
	# words = [word.lower() for word in re.findall("([A-Za-z]\w+)", text_to_clean)]

	words_raw = [word.lower() for word in re.findall(r'\w+(?:-\w+)?', text_to_clean)]
	words = [k for k in words_raw if not k.split('-')[0].isdigit()]
	words = [k for k in words if not k in stop_words.keys()]
	words = [lancaster.stem(k) for k in words]
	words = [k for k in words if k in top_words.keys()]

	return words

	# words2 = []
	# for w in words:
	# 	if not stop_words.has_key(w):

	# 		words2.append(w)

	# return words2


	# for word in words:
	# 	if word in words_count:
	# 		words_count[word] += 1
	# 	else:
	# 		words_count[word] = 1
	# return words_count

# Helper function to print words and count in VW-friendly format
def print_features(frequency_map):
	return_string = ""
	for feature, count in frequency_map.iteritems():
		return_string += " " + feature + ":" + str(count)

	# if return_string == "":
	# 	return_string = " no_value:1"
	return return_string

# Data headers:
# varietal	name	country	sub_region	appelation	alcohol	review_1	review_2	review_3	review_4	review_5	link
# Reviews are columns 6-10 (0-indexed)
review_start = 6
review_end = 10


# Build varietal matchup from the file
# categories = {} # 34 categories total
# # category_filter = ["Zinfandel", "Chardonnay", "Sauvignon Blanc", "Pinot Noir", "Riesling", "Shiraz/Syrah"]
# varietal_map_file = open('vowpal_wabbit/category_map.txt', 'r')
# for f in varietal_map_file:
# 	lines = f.split('\r') # excel is awful, so readline breaks :(
# for line in lines:
#     data = (line.strip()).split('\t')
#     categories[data[0]] = {"id":data[1], "color":data[2]}
# varietal_map_file.close
stop_words = {}
top_words = {}
stop_words_file = open('./mallet/data/stop_words_wine_specific.txt', 'r')
for line in stop_words_file:
    data = (line.strip())
    stop_words[data] = 1
stop_words_file.close

stop_words_file = open('./mallet/data/stop_words.txt', 'r')
for line in stop_words_file:
    data = (line.strip())
    stop_words[data] = 1
stop_words_file.close

top_words_file = open('./mallet/data/top_words_stemmed.txt', 'r')
top_words_max = 5000
for line in top_words_file:
	if (len(top_words) > top_words_max):
		break
	else:
	    data = (line.strip())
	    top_words[data] = 1
top_words_file.close

lancaster = LancasterStemmer()

def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])

# Reformat each line in Vowpal Wabbit-friendly form
for line in sys.stdin:
# 	lines = f.split('\r') # excel is awful, so readline breaks :(

# for line in lines[1:len(lines)]:
	#data = line.strip().split('\t')

	# print review

	# Parse varietal and keywords from each line
	review = line
	keywords = []
	keywords = clean_text(review)

	# ngrams_out = nltk.bigrams(" ".join(keywords))
	ngrams_out = find_ngrams(keywords, 1)

	ngrams_out_str = ""
	for gram in ngrams_out:
		ngrams_out_str += "_".join(gram) + " " 

	# print ngrams_out_str
	print data[0] + " " + data[1] + " " + ngrams_out_str



