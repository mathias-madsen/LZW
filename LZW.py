import random


###################### ENCODING AND DECODING ###################### 


def text_to_integers(text, alphabet):
    " LZW-encode a text as a sequence of integers "

    phrasebook = alphabet[:] 
    register, tape = "", text

    while tape:

        # while nothing new happens, move forward:
        while tape and (register + tape[0] in phrasebook):
            register, tape = register + tape[0], tape[1:]

        # encode what's in the buffer:
        yield phrasebook.index(register)

        # learn a new word: the buffer + the lookahead:
        if tape:
            phrasebook.append(register + tape[0])

        # flush the buffer:
        register = ""


def integers_to_text(encoded, alphabet):
    " LZW-decode a sequence of integers as a text "

    # initialize:
    phrasebook = alphabet[:]
    code = encoded[:]

    n = code.pop(0)
    next_word = phrasebook[n]

    phrasebook.append(next_word)                # still awaiting completion
    yield next_word

    while code:
        n = code.pop(0)

        if n < len(phrasebook) - 1:             # known and complete entry
            next_word = phrasebook[n]           # retreive the decoded phrase
            phrasebook[-1] += next_word[0]      # complete the previous entry

        else:                                   # Unknown and incomplete entry
            phrasebook[n] += phrasebook[n][0]   # circularly complete yourself
            next_word = phrasebook[n]           # after self-completion: known

        phrasebook.append(next_word)            # still awaiting completion
        yield next_word


###################### PREDICTION AND SIMULATION ###################### 


def sample_text(text, alphabet, additional_phrases=200):
    " Encode the whole text, then use the learned phrasebook to continue "

    code = list(text_to_integers(text, alphabet))
    roof = len(alphabet) + len(code)

    for i in range(additional_phrases):
        code.append(random.randint(0, roof - 1))
        roof += 1

    return "".join(integers_to_text(code, alphabet))


def compute_parser_state(text, alphabet):
    " (phrasebook, leftover characters) posterior to scanning the text "

    phrasebook = alphabet[:] 
    register, tape = "", text

    while tape:

        # while nothing new happens, move forward:
        while tape and (register + tape[0] in phrasebook):
            register, tape = register + tape[0], tape[1:]

        # learn a new word: the buffer + the lookahead:
        if tape:
            phrasebook.append(register + tape[0])

        # flush the buffer:
        if tape:
            register = ""
        else:
            return phrasebook, register


def match(phrase, segment):
    " True iff the phrase is consistent with the remaining segment "

    return phrase.startswith(segment) or segment.startswith(phrase)


def sample_continuation(phrasebook, segment=""):
    " Sample a letter from the posterior distribution at the given slot "

    # the script does so by sampling from the LZW process given the current
    # phrasebook until a letter has been written in the relevant p

    tail, phrase = segment, ""
    parsing = []

    while len(tail) >= len(phrase):

        matches = [phrase for phrase in phrasebook if match(phrase, tail)]
        phrase = random.choice(matches)

        parsing.append(phrase)

        while tail and phrase:
            tail, phrase = tail[1:], phrase[1:]

    return parsing, tail

