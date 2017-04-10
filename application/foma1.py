#!/usr/bin/env python
#
# (C) 2017 by Damir Cavar <dcavar@iu.edu>
#
#
# Example of how to use Foma and generate a rewrite rule from the output of
# the morphology.

import foma

token = "calls"

fsm = foma.FST.load(b'eng.fst')

result = list(fsm.apply_up(str.encode(token)))

for x in result:
    x = x.decode('utf-8')
    morphtokens = x.split('+')
    print(morphtokens[1], "-->", morphtokens[0])



