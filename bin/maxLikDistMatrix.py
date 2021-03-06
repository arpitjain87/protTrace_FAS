### Script to generate maximum likelihood distances file
### INPUT -> outfile (from TREEPUZZLE)
### OUTPUT -> maxLikDist.txt

import os, sys

def main(infile, prot_id):
	outfile = open('maxLikDist_%s.txt' %prot_id, 'w')

	for j in range(1, len(infile) - 1):
		if infile[j] != "":
			if not infile[j].split()[0][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
				outfile.write('\n' + infile[j].split()[0])
				for k in range(1, len(infile[j].split())):
					if infile[j].split()[k] != "":
						outfile.write('\t' + infile[j].split()[k])
			else:
				for k in range(len(infile[j].split())):
					if infile[j].split()[k] != "":
						outfile.write('\t' + infile[j].split()[k])
		else:
			break
	outfile.close()

	f = open('maxLikDist_%s.txt' %prot_id).read().split('\n')
	fnew = open('maxLikDist_%s.txt' %prot_id, 'w')
	for i in range(1, len(f)):
		fnew.write(f[i] + '\n')
	fnew.close()
