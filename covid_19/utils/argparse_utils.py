import argparse

def strictly_positive_int(n):
	n = int(n)
	if n < 1:
		msg = "%r is not a strictly positive int" % n
		raise argparse.ArgumentTypeError(msg)
	return n
