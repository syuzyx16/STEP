with open ("words.txt", "r",) as f:
    dictionary = [ word.strip() for word in f if word.strip()]

new_dictionary = {}

for word in dictionary:
    key = ''.join(sorted(word))
    if key not in new_dictionary:
        new_dictionary[key] = []
    new_dictionary[key].append(word)


def find_anagram(word):
    target = ''.join(sorted(word))
    if target not in new_dictionary: return "No match"
    anagrams =  [anagram for anagram in new_dictionary[target] if anagram != word]
    if anagrams: return anagrams
    else : return "No match"

print(find_anagram("listen") )
print(find_anagram("eeee"))
print(find_anagram("  !"))