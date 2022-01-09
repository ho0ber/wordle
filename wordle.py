from collections import Counter

class Wordle(object):
    def __init__(self, wordlist_filename):
        self.words = self.load(wordlist_filename)
        self.guessed_letters = set()

    def load(self, filename):
        return [w.strip() for w in open(filename) if len(w.strip()) == 5]
    
    def refine(self, guess, match="_____"):
        self.guessed_letters.update(c for c in guess)
        non = [c for c in guess if c not in match.lower()]
        self.words = [w for w in self.words if self.word_matches(w, match, non)]

    def word_matches(self, word, match, non):
        for i in range(5):
            if match[i] in "_ ":
                continue
            if match[i].lower()==match[i]:
                if match[i] == word[i] or match[i] not in word:
                    return False
            else:
                if match[i].lower() != word[i]:
                    return False
        for c in word:
            if c in non:
                return False
        return True
    
    def display(self):
        counts = Counter(c for w in self.words for c in w if c not in self.guessed_letters)
        if counts:
            print("Common new letters: "+" ".join([f"{l}({c})" for l,c in counts.most_common()]))
        commons = [(word, sum(counts[c] for c in list(set(word)))) for word in self.words]
        commons.sort(key=lambda x: x[1], reverse=True)
        for word,score in commons:
            print(f"{word} ({score})")

if __name__ == "__main__":
    wordle = Wordle("words_en.txt")
    wordle.refine("arose", "_ro_E")
    wordle.refine("until")
    wordle.refine("forge", "_ORGE")
    wordle.display()
