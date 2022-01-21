from collections import Counter
from winner import get_winners

class Wordle(object):
    def __init__(self, words, set_guesses=[], winner=None, day=None):
        self.words = words
        self.guessed_letters = set()
        self.set_guesses = {i:g for i,g in enumerate(set_guesses)}
        self.winner = winner
        self.guess_log = []
        self.day = day
        self.debug_level = 0

    def log(self, s, debug_level=1):
        if self.debug_level >= debug_level:
            print(s)
    
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
        self.log(scores, 2)
        recommendation = scores[0][0]
        final_rec = self.set_guesses.get(len(self.guess_log),recommendation)
        self.log(f"Recommended: {final_rec}")
        return final_rec

    def evaluate_guess(self, guess):
        if not self.winner:
            result = input()
        else:
            result = ""
            for i,c in enumerate(guess):
                if c == self.winner[i]:
                    result += c.upper()
                elif c in self.winner:
                    result += c
                else:
                    result += "_"
            self.log(f"Result of guess: {result}")
        self.guess_log.append(result)
        return result
    
    def print_result(self):
        if self.day is not None:
            print(f"Wordle {self.day} {len(self.guess_log)}/6")
        
        for guess in self.guess_log:
            for c in guess:
                if c in "_ ":
                    print("⬛", end="")
                elif c.upper() == c:
                    print("🟩", end="")
                else:
                    print("🟨", end="")
            print("")

    def solve(self):
        while True:
            rec = wordle.recommend()
            
            result = self.evaluate_guess(rec)
            if result.upper() == result and set("_ ").isdisjoint(result):
                self.log("You won!")
                # self.print_result()
                return len(self.guess_log)
            wordle.refine(rec, result)

def load_dict(filename):
    return [w.strip() for w in open(filename) if len(w.strip()) == 5]

if __name__ == "__main__":
    word_dictionary = load_dict("words_en.txt")
    w = get_winners()[600]
    print(w)
    wordle = Wordle(word_dictionary, [], w, 600)
    wordle.debug_level=2
    wordle.log(f"Attempting to solve #{600}")
    print(w)


    score = wordle.solve()
    scores = []
    fixed_guesses = ["arose","until"]
    for i, winner in enumerate(get_winners()):
        wordle = Wordle(word_dictionary, fixed_guesses, winner, i)
        wordle.log(f"Attempting to solve #{i}")
        score = wordle.solve()

        scores.append(score)
        stats = Counter(s < 6 for s in scores)
        result = 'lost' if score > 6 else 'won'

        print("num: {:>4}  result: {:>4}  score: {:>2}  -  min: {}  max: {:>2}  avg: {:>5}  won: {:<4}  lost: {:<4}  rate: {:.2f}%".format(
            i, result, score, min(scores), max(scores), round(sum(scores)/len(scores), 2), stats[True], stats[False], stats[True]/len(scores)*100
        ))

# Wordle dict:
#   no guesses:
#     num: 2314  result: lost  score:  7  -  min: 2  max: 13  avg:  4.52  won: 1907  lost: 408   rate: 82.38%
#   arose, until:
#     num: 2314  result: lost  score:  7  -  min: 1  max: 12  avg:  4.45  won: 1971  lost: 344   rate: 85.14%
# words_en:
#   arose, until:
#     
