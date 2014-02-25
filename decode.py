"""
Crossword SAT Decoder
@AUTHORS: Jeremy Dolinko & Ben Glickman
@DESCRIPTION: Takes in the output from the .ans file and
              prints out the item
"""
import sys

class Globs:
	cross = []
	m_row = 0
	m_col = 0

def workout_encoding(answerfile):
	Globs.cross = [[] for i in range(Globs.m_row * Globs.m_col)]
	f = open(answerfile)
	for word in f:
		if not ("~" in word):
			#words in x_num_num -> [x,num,num]
			lst = word.split("_")
			row = int(lst[1])
			col = int(lst[2])
			if Globs.cross[(row * Globs.m_row) + col][0] != "":
				print "TWO ITEMS IN SAME SPOT?"
			Globs.cross[(Globs.m_row * row) + col].append(lst[0])
	f.close()
	for i in range (Globs.m_row * Globs.m_col)
			if (i % Globs.m_col == 0):
				print(Globs.cross[i][0] + "\n"),
			else:
				print(Globs.cross[i][0]),

def get_args():
	if len(sys.argv) != 3:
		sys.stderr.write("Incorrect number of args")
		sys.exit(1)
	else:
		puzzle = str(sys.argv[1])
		answer = str(sys.argv[2])
		return [puzzle, answer]

def main():
	my_args = get_args()
	
	p = open(my_args[0])
	firstline = p.readline().split()
	Globs.m_row = firstline[0]
	Globs.m_col = firstline[1]
	p.close()

	workout_encoding(my_args[1])

if __name__ == '__main__':
	main()