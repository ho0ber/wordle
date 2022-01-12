from collections import Counter

class Wordle(object):
    def __init__(self, wordlist_filename, set_guesses=[]):
        self.words = self.load(wordlist_filename)
        self.guessed_letters = set()
        self.set_guesses = {i:g for i,g in enumerate(set_guesses)}

    def load(self, filename):
        return [w.strip() for w in open(filename) if len(w.strip()) == 5]
    
    def refine(self, guess, match="_____"):
        self.guessed_letters.update(c for c in guess)
        non = set(c for c in guess if c not in match.lower())
        self.words = [w for w in self.words if self.word_matches(w, match, non)]

    def word_matches(self, word, match, non):
        for i in range(5):
            if not match[i] in "_ ":
                if match[i].lower() == match[i]:
                    if match[i] == word[i] or match[i] not in word:
                        return False
                elif match[i].lower() != word[i]:
                    return False

        return non.isdisjoint(word)

    def recommend(self):
        counts = Counter(c for w in self.words for c in w if c not in self.guessed_letters)
        scores = [(word, sum(counts[c] for c in list(set(word)))) for word in self.words]
        scores.sort(key=lambda x: x[1], reverse=True)
        recommendation = scores[0][0]
        return recommendation

    def interactive_solve(self):
        for i in range(6):
            rec = self.set_guesses.get(i,wordle.recommend())
            print(f"Recommended: {rec}")
            result = input()
            if result.upper() == result and set("_ ").isdisjoint(result):
                print("You won!")
                break
            wordle.refine(rec, result)

if __name__ == "__main__":
    wordle = Wordle("words_en.txt", ["arose","until"])
    wordle.interactive_solve()
