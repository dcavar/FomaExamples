#!/usr/bin/env python3
#
# (C) 2017 by Damir Cavar <dcavar@iu.edu>
#
# Testing Foma in Python 3.x with NLTK pre-processing
#
# Make sure that the script is either executable or that you can run it with your Python 3.x interpreter.
#
# I recommend that you use Anaconda, because it has all modules preinstalled, except of the foma module.
#
# Place the foma.py module somewhere in your path or module location. This is not the same as the one on the public
# GitHub, it is patched to work with Python 3.x
#
# This is an example of a multi-word morphological analuzer using a Foma morphology. In this distribution you should
# find eng.fst, a basic English morphology (with a lot of words and rules missing).


import foma, sys, glob
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk import pos_tag


def main(fname, fsm, n=5):
    try:
        ifp = open(fname, mode='r', encoding='utf-8')
        text = ifp.read()
        ifp.close()
    except IOError:
        print("Cannot read", fname)

    sentences = sent_tokenize(text)

    for s in sentences:
        print(str.strip(s), '\n')
        tokens = word_tokenize(s)
        tagged = pos_tag(tokens)
        if tagged[0][1] != 'NNP' and str.isupper(tokens[0][0]) and str.islower(tokens[0][1:]):
            # print(tokens)
            tokens[0] = tokens[0].lower()

        for i in range(1, n + 1):
            for j in range(len(tokens)-i+1):
                toks = " ".join(tokens[j:i+j])
                result = list(fsm.apply_up(str.encode(toks)))
                if len(result) == 0:
                    if i == 1:
                        print( "\t".join( (str(j), str(j+i), toks) ), end="\t")
                        if toks == tagged[j][1]:
                            print(toks + "+Punct")
                        elif tagged[j][1] == 'JJ':
                            print(toks.lower() + "+Adj")
                        elif tagged[j][1] == 'NNP':
                            print(toks + "+N")
                        elif tagged[j][1] == 'CC':
                            print(toks + "+Conj")
                        else:
                            print(tagged[j][1])
                else:
                    print( "\t".join( (str(j), str(j + i), toks, ", ".join([ i.decode('utf-8') for i in result ])) ) )
        print('-' * 30)


if __name__=="__main__":
    fsm = foma.FST.load(b'eng.fst')
    n = 6
    #print("loaded FST")

    for x in sys.argv[1:]:
        for fname in glob.glob(x):
            main(fname, fsm, n)


