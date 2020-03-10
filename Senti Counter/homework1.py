"""
 Vino vvimalan@stevens.edu
 (C) Stevens.edu
"""

#function that loads negative word list file
def loadLexicon(fname):
    newLexList = set()
    lexConn = open(fname)
    for line in lexConn:
        newLexList.add(line.strip()) 
    lexConn.close()
    return newLexList #return end of  loadLexicon Function
 
#the function will return a dictionary that contains frequency of negative words occured between the and phone
def run(path):
    negFreq = {} #dictionary to score negative words frequency
    negLex = loadLexicon('negative-words.txt') #load the negative lexicons
    inputFile = open(path) #load the reviews file
    
    for line in inputFile:
        negWords = set() #set to contain all unique negative words in a line
        line = line.lower().strip() #converting line to lower case and removing extra spaces
        for word in line.split(' '): #for every word in the review file
            if word in negLex: #if the word is in the negative lexicon
                negWords.add(word) #adding unique word in the negative words set
        for negword in negWords:  #iterate the set thru line look for the \w phone
            if negword in negFreq:
                negFreq[negword] += line.count("the "+negword+" phone")
            else:
                negFreq[negword] = line.count("the "+negword+" phone")
            
            
    inputFile.close() #closing connection with file
    return negFreq

# main function
if __name__ == "__main__": 
    dictionary = run('homeworkinput') #get dictionary as return value
    print(dictionary) #printing dictionary
