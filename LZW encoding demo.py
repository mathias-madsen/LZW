from LZW import text_to_integers, integers_to_text
from LZW_data import holmes, ENGLISH


numberlist = list(text_to_integers(holmes, ENGLISH))
chunks = list(integers_to_text(numberlist, ENGLISH))

print("""We encode the following snippet of English text:

'%s'
""" % holmes)

print("""The encoder parses this text into the following list of largest-known phrases:

%s

(Note how the phrase length grows as the phrasebook gets longer.)
""" % " + ".join("'%s'" % chunk for chunk in chunks))

print("""These phrases are actually coded by integers:

%s
""" % numberlist)

print("""If we want to, we can once again decode the list of integers back into text:

'%s'
""" % "".join(integers_to_text(numberlist, ENGLISH)))