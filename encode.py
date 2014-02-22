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

def main():
	print "Crossword"

if __name__ == '__main__':
	main()