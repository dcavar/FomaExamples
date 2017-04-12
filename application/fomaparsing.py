import nltk, foma
from nltk.grammar import FeatureGrammar,FeatDict


def feat2LFG(f):
    result = featureMapping.get(f, "")
    return(nltk.FeatStruct("".join( ("[", result, "]") )))


def flatFStructure(f):
    res = ""
    for key in f.keys():
        val = f[key]
        if res:
            res += ', '
        if (isinstance(val, FeatDict)):
            res += key + '=' + flatFStructure(val)
        else:
            res += key + "=" + str(val)
    return('[' + res + ']')


grammarText = """
% start S
# ############################
# Grammar Rules
# ############################
S -> NP[NUM=?n, PERS=?p, CASE='nom'] VP[NUM=?n, PERS=?p]
NP[NUM=?n, PERS=?p, CASE=?c] -> N[NUM=?n, PERS=?p, CASE=?c]
NP[NUM=?n, PERS=?p, CASE=?c] -> D[NUM=?n,CASE=?c] NC[NUM=?n,PERS=?p,CASE=?c]
NP[NUM=?n, PERS=?p, CASE=?c] -> Pron[NUM=?n,PERS=?p,CASE=?c]
VP[NUM=?n, PERS=?p] -> V[NUM=?n, PERS=?p]
VP[NUM=?n, PERS=?p] -> V[NUM=?n, PERS=?p] NP[CASE='acc']
"""


featureMapping = {
    'Def'   : "DETTYPE = def",
    'Indef' : "DETTYPE = indef",
    'Sg'  : "NUM = sg",
    'Pl'  : "NUM = pl",
    '3P'  : "PERS = 3",
    'Masc': "GENDSEM = male",
    'Fem' : "GENDSEM = female",
    'Dat' : "CASE = dat",
    'Acc' : "CASE = acc",
    'Nom' : "CASE = nom",
    'NEPersonName' : """NTYPE = [NSYN = proper,
                                NSEM = [PROPER = [PROPERTYPE = name,
                                                 NAMETYPE   = first_name]]],
                        HUMAN = 1"""
}

#for x in featureMapping:
#    featureMapping[x] = nltk.FeatStruct("".join( ("[", featureMapping[x], "]") ))



fst = foma.FST.load(b'eng.fst')


def parseFoma(sentence):
    tokens = sentence.split()

    tokenAnalyses = {}
    rules = []
    count = 0
    for token in tokens:
        aVal = []
        result = list(fst.apply_up(str.encode(token)))
        for r in result:
            elements = r.decode('utf8').split('+')
            print(r.decode('utf8'))

            lemma = elements[0]
            tokFeat = nltk.FeatStruct("[PRED=" + lemma + "]")

            cat = elements[1]
            if len(elements) > 2:
                feats = tuple(elements[2:])
            else:
                feats = ()
            for x in feats:
                fRes2 = feat2LFG(x)
                fRes = tokFeat.unify(fRes2)
                if fRes:
                    tokFeat = fRes
                else:
                    print("Error unifying:", tokFeat, fRes2)
            flatFStr = flatFStructure(tokFeat)
            aVal.append(cat + flatFStr)
            rules.append(cat + flatFStr + " -> " + "'" + token + "'")
        tokenAnalyses[count] = aVal
        count += 1

    grammarText2 = grammarText + "\n" + "\n".join(rules)

    grammar = FeatureGrammar.fromstring(grammarText2)
    parser = nltk.parse.FeatureChartParser(grammar)
    result = list(parser.parse(tokens))
    if result:
        for x in result:
            print(x)
    else:
        print("*", sentence)


parseFoma("John loves her")
