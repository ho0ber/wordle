# wordle
Wordle solving helper

## Interactive Solve Usage
* `python3 wordle.py`
* For each round:
  * Type the word it recommends into wordle
  * for any gray letters, input `_`
  * for any yellow letters, input the letter in lowercase
  * for any green letters, input the letter in uppercase

## Example
```
$ python3 wordle.py
Recommended: arose
ar_s_
Recommended: until
__t__
Recommended: parts
_ARTS
Recommended: carts
_ARTS
Recommended: darts
_ARTS
Recommended: farts
FARTS
You won!
```