from textblob import TextBlob, Word

def getIfMeaning(input_string):
    s = input_string
    if s.find('meaning of')>=0:
        s = s.replace('meaning of ', '')
        return str(s), True
    else:
        return '', False

def getMeaning(phrase):
    def_list = {}
    for word in TextBlob(phrase).words:
        def_list[str(word)] = Word(word).definitions
    meaning_string = ''
    for word in def_list:
        meaning_string = meaning_string+str(word).upper()+":-\n"
        for defn in def_list[word]:
            meaning_string = meaning_string+">"+str(defn)+"\n"

    return meaning_string


