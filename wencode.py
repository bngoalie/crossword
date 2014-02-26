#!/usr/bin/python
"""
Crossword SAT Weighted Encoder
@AUTHORS: Jeremy Dolinko & Ben Glickman
@DESCRIPTION: Takes a .puzzle file describing a Crossword
              and returns the MAXSAT CNF encoding that can be used by
              zchaff.
"""
import sys
from sets import Set

class Glob:
	cross = [] #stores crossword elements at [r][c]
	hashmtrx = [] # stores list of possible values at [r][c]
	trie_dict = {"#":Set(["#"])} # dictionary
	m_row = 0 # grid row size
	m_col = 0 # grid col size

def print_set_variables():
	for r in range(Glob.m_row):
		for c in range(Glob.m_col):
			if Glob.cross[(r * Glob.m_row) + c] != ".":
				if (r == Glob.m_row -1 and c == Glob.m_row -1):
					print(Glob.cross[(r * Glob.m_row) + c] + "_" + str(r) + "_" + str(c)),
				else:
					print(Glob.cross[(r * Glob.m_row) + c] + "_" + str(r) + "_" + str(c) + " &\n"),


# helper for outer loops
def inner_loop(key, row, col, direction):
	if (direction == "H" and col < Glob.m_col - 1) or (direction == "V" and row < Glob.m_row - 1):
		lst = Glob.trie_dict.get(key)
		for i in range(len(key)):
			if i == (len(key) - 1):
				if direction == "H":
					print("~" + key[i] + "_" + str(row) + "_" + str(col - len(key) + i + 1)),
				else:
					print("~" + key[i] + "_" + str(row - len(key) + i + 1) + "_" + str(col)),
			else:
				if direction == "H":
					print("~" + key[i] + "_" + str(row) + "_" + str(col - len(key) + i + 1) + " v "),
				else:
					print("~" + key[i] + "_" + str(row - len(key) + i + 1) + "_" + str(col) + " v "),
		for letter in lst:
			if direction == "H":
				print(" v " + letter + "_" + str(row) + "_" + str(col + 1)),
			else:
				print(" v " + letter + "_" + str(row + 1) + "_" + str(col)),
		print(" &\n"),
		for letter in lst:
			prefix = ""
			if letter == "#":
				prefix = "#"
			else:
				prefix = key + letter
			if direction == "H":
				inner_loop(prefix, row, col + 1, direction)
			else:
				inner_loop(prefix, row + 1, col, direction)
		if key != "":
			if not (key[-1] in Glob.hashmtrx[(row * Glob.m_row) + col]):
				Glob.hashmtrx[(row * Glob.m_row) + col].append(key[-1])

def horiz_outer_loop():
	for r in range(1, Glob.m_row - 1):
		inner_loop("#", r, 0, "H")

def vert_outer_loop():
	for c in range(1, Glob.m_col - 1):
		inner_loop("#", 0, c, "V")

def one_per_block():
	for r in range(Glob.m_row):
		for c in range (Glob.m_col):
			for i in range( len(Glob.hashmtrx[(r * Glob.m_row) + c]) - 1 ):
				for j in range (i + 1, len(Glob.hashmtrx[(r * Glob.m_row) + c])):
					print("~" + Glob.hashmtrx[(r * Glob.m_row) + c][i] + "_" + str(r) + "_" + str(c) + " v ~" + Glob.hashmtrx[(r * Glob.m_row) + c][j] + "_" + str(r) + "_" + str(c) + " &\n"),
			for item in Glob.hashmtrx[(r * Glob.m_row) + c]:
				if item == Glob.hashmtrx[(r * Glob.m_row) + c][len(Glob.hashmtrx[(r * Glob.m_row) + c]) -1]:
					print(item + "_" + str(r) + "_" + str(c) + " &\n"),
				else:
					print(item + "_" + str(r) + "_" + str(c) + " v "),

# helper method for making our "trie"
def tries(prefix, rest):
	# if the key is in the dict, union the first letter of the rest in
	if prefix in Glob.trie_dict:
		Glob.trie_dict[prefix] = Glob.trie_dict[prefix] | Set([rest[0]])
	# if there's still stuff left and is not already in, put it in
	elif len(rest) > 0:
		Glob.trie_dict[prefix] = Set([rest[0]])
	# if it's done, put in the empty set
	else:
		Glob.trie_dict[prefix] = Set(["#"])
	# if the rest isn't empty try it with the next letter
	if rest != "#":
		tries(prefix + rest[0], rest[1:])

def make_trie(wordlist):
	f = open(wordlist)
	for word in f:
		word = word.strip()
		tries("#", word + "#")
	f.close()

def make_crossmtrx(puzzle):
	f = open(puzzle)
	items = f.readline().split()
	Glob.m_row = int(items[0])
	Glob.m_col = int(items[1])
	for line in f:
		line = line.strip()
		for char in line:
			Glob.cross.append(char)
	Glob.hashmtrx = [ [] for i in range(Glob.m_row * Glob.m_col)]

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

	horiz_outer_loop()
	vert_outer_loop()
	one_per_block()
	print_set_variables()


if __name__ == '__main__':
	main()
