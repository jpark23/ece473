def find_sentences(word_dict, start, length):
    nexts = word_dict.get(start, 0)
    # print(str(start)+str(" ")+str(length)+str(" ")+str(nexts))
    if not nexts or length == 1:
        return start
    sentence = list()
    for next in nexts:
        wordorwords = find_sentences(word_dict, next, length-1)
    sentence.append(wordorwords)
    # print(sentence)
    return sentence

def main_3c():
    sentence = 'the cat and the mouse'
    word_dict = {}
    words = sentence.split()
    index = 0
    while(index < len(words)-1):
        test_entry = words[index]
        if(test_entry not in word_dict):
            new_value = list()
            new_value.append(words[index + 1])
            word_dict[test_entry] = new_value
        else:
            word_dict[test_entry].append(words[index+1]) 
        index += 1
    word_dict[words[4]] = []
    keylist = word_dict.keys()
    # for key in keylist:
    #     sentence = find_sentences(word_dict, key, 5)
    sentence = find_sentences(word_dict, "and", 5)

def main():
    

main()