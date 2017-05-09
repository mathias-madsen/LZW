from LZW import sample_continuation, compute_parser_state
from LZW_data import holmes, ENGLISH

snippet = holmes[:900]

print("""We wish to predict the next character in the following text:\n""")
print(snippet + "_", "\n\n")

phrasebook, leftovers = compute_parser_state(snippet, ENGLISH)
lookahead = len(leftovers)

N = 1000

samples = [sample_continuation(phrasebook, leftovers) for i in range(N)]
chars = [''.join(sample)[lookahead] for sample, leftovers in samples]
charlist = sorted(set(chars), key=lambda x: -chars.count(x))

print("""The corresponding distribution is as follows:\n""")

for character in charlist:
    
    occurrences = chars.count(character)
    prob = float(occurrences) / N
    
    print(character, '\t', '%.3f' % prob)
