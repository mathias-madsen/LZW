import random

from LZW import sample_text
from LZW_data import ENGLISH, holmes


print("""This script learns a phrasebook from reading a short snippet of text,
then goes on to sample from the posterior state of the LZW process.
(The method does not take into account the minor issues about leftover
characters at the end of a text.)\n\n""")

for hintsize in [10, 100, 1000]:
    print("With a condition of size %s:\n" % hintsize)
    print(sample_text(holmes[:hintsize], ENGLISH))
    print("\n")

print("""You should be able to detect that the posterior process contains more English
and English-looking phrases when the size of the training material is larger.""")

