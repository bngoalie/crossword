"""
Crossword SAT Encoder
@AUTHORS: Jeremy Dolinko & Ben Glickman
@DESCRIPTION: Takes a .puzzle file describing a Crossword
              and returns the CNF encoding that can be used by
              zchaff.
"""

import sys
from sets import Set

# Make sure args are correct
class Glob:
	cross = [] #stores crossword elements at [r][c]
	hashmtrx = [] # stores list of possible values at [r][c]
	trie_dict = {} # dictionary
	m_row = 0 # grid row size
	m_col = 0 # grid col size

def print_set_variables():
	for r in range(m_row):
		for c in range(m_col):
			if Glob.hashmtrx[r][c] != ".":
				if (r == m_row and c == c_row):
					print Glob.hashmtrx[r][c] + r + "_" + c
				else:
					print Glob.hashmtrx[r][c] + r + "_" + c + " & "

def inner_loop(key, row, col, direction):
	if direction == "H":
		col = col + 1
	else:
		row = row + 1
	lst = Glob.trie_dict.get(key)
	if len(lst) == 0:
		print " v ~" + key[0][-1] + row + "_" + col
	else:
		for letter in lst:
			inner_loop((key[0] + letter, key[1]), row, col, direction)
			if key[0] != "":
				print " v " + key[0][-1] + row + "_" + col
	if key[0] != "":
		if not (key[0] in Glob.hashmtrx[row][col]):
			Glob.hashmtrx[row][col].append(key[0])

def horiz_outer_loop():
	for r in range(m_row):
		for c in range(m_col):
			counter = 0
			if Glob.crossmtrx[r][c] != "#":
				counter = counter + 1
			elif counter > 0:
				print " ~#" + r + "_" + (c - counter - 1)
				inner_loop(("", counter), "H", r, (c - counter))
				print " &"
			else:
				counter = 0

# helper method for making our "trie"
def tries(prefix, length, rest):
	# if the key is in the dict, union the first letter of the rest in
	if (prefix,length) in Glob.trie_dict:
		Glob.trie_dict[(prefix, length)] = Glob.trie_dict[(prefix, length)] | Set([rest[0]])
	# if there's still stuff left and is not already in, put it in
	elif len(rest) > 0:
		Glob.trie_dict[(prefix, length)] = Set([rest[0]])
	# if it's done, put in the empty set
	else:
		Glob.trie_dict[(prefix, length)] = Set([])
	# if the rest isn't empty try it with the next letter
	if rest != "":
		newprx = "" + prefix + rest[0]
		tries(prefix + rest[0], length, rest[1:])

def make_trie(wordlist):
	f = open(wordlist)
	for word in f:
		word = word.strip()
		tries("", len(word), word)
	f.close()

def make_crossmtrx(puzzle):
	f = open(puzzle)
	items = f.readline().split()
	Glob.m_row = items[0]
	Glob.m_col = items[1]
	for line in f:
		line = line.strip()
		for char in line:
			Glob.cross.append(char)

def get_args():
	# checks that arguments are correct
	if len(sys.argv) != 3:
		sys.stderr.write("Incorrect number of args")
		sys.exit(1)
	else:
		puzzle = str(sys.argv[1])
		wordlist = str(sys.argv[2])
		return [puzzle, wordlist]

def main():
	puzzlewords = get_args()
	puzzle = puzzlewords[0]
	wordlist = puzzlewords[1]
	make_trie(wordlist) # set up the dictionary list
	make_crossmtrx(puzzle)



if __name__ == '__main__':
	main()