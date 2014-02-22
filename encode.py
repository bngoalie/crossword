"""
Crossword Encode:

First line:
	int1 == row, int2 == col

if #, then is_#
if ., set ~is_#

# starts and ends words
#jigs# #jig# #jigsaw# are all valid

Variables at End:
  LTR_XY i.e. s_13 == "s" at 1,3

Use the dictionary to create the trie...

check that prev letters are valid, then put possible
letters for next char

prefix -> ((possible letters) ^ (is it shared) ^ (end of word))
"""
import sys

# Make sure args are correct
def get_args():
	if len(sys.argv) != 3:
		sys.stderr.write("Incorrect number of args")
		sys.exit(1)
	else:

		return [str(sys.argv[1]), str(sys.argv[2])]

# Takes the wordlist, returns the trie of words
def make_trie(wordlist):
	f = open(wordlist)
	for line in f:
		# add to trie
		print line
	f.close()

# encode everything
def main():
	fromarg = get_args()
	print (fromarg[0] + " " +  fromarg[1])

if __name__ == '__main__':
	main()