SCORE = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

def cal_score(word):
    score = 0
    for letter in word:
        if 'a' <= letter <= 'z':
            score += SCORE[ord(letter) - ord('a')]
    return score

def count(word):
    count = {}
    for letter in word:
      if letter not in count:
        count[letter] = 0
      count[letter] += 1
    return count

def subset_or_not (word_in_dict, input):
    word_count = count(word_in_dict)
    input_count = count(input)
    for letter in word_in_dict:
        if letter not in input or word_count[letter] > input_count[letter]:return False
    return True


with open( "words.txt", "r") as f:
    dictionary = [ word.strip() for word in f if word.strip() ]
with open( "large.txt", "r") as f:
    inputs = [ input.strip() for input in f if word.strip() ]

scored_dictionary = sorted(dictionary, key=cal_score, reverse=True)

answers= []

for input in inputs:
    for word in scored_dictionary:
        answer = "No match"
        if subset_or_not(word,input): 
            answer = word
            break
    answers.append(answer)

with open("large_answer.txt", "w") as f:
    for word in answers: f.write(word + "\n")
    
    
# medium for 29s 
# large for 34s

#You answer is correct! Your score is 193.
#You answer is correct! Your score is 18911.
#You answer is correct! Your score is 244642.
