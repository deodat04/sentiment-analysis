from nltk.corpus import wordnet

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    
    return list(set(synonyms))

positive_word = "good"
negative_word = "bad"

synonymes = get_synonyms(positive_word)
print(f"Synonymes de '{positive_word}': {synonymes}")
synonymess = get_synonyms(negative_word)
print(f"Synonymes de '{negative_word}': {synonymess}")