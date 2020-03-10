#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 15:51:37 2020

@author: rswithinzadok
"""

import nltk, re
from nltk.tokenize import sent_tokenize
from nltk import load

#to return the positive and negative words as a set
def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())#  strip to remove the lin-change character
    lex_conn.close()

    return newLex

def processSentence(sentence,posLex,negLex,tagger):
    
    terms = nltk.word_tokenize(sentence.lower())
    tagged_terms=tagger.tag(terms)#do POS tagging on the tokenized sentence
    #print('tagged terms', tagged_terms)
    word_comb = []
    for i in range(len(tagged_terms)-3):
        term1=tagged_terms[i] #current term
        term2=tagged_terms[i+1] #next term
        term3=tagged_terms[i+2] #third term
        term4=tagged_terms[i+3] #fourth term
        
        if term1[0]=='not':
            if term3[0] in posLex.union(negLex):
                if re.match('NN',term4[1]):
                    word_comb.append((term1[0], term2[0], term3[0], term4[0]))
            
    return word_comb        
    
    
if __name__=='__main__':
    _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
    tagger = load(_POS_TAGGER)
    posLex = loadLexicon('positive-words.txt')
    #print(posLex)
    negLex = loadLexicon('negative-words.txt')
    sentence = 'not a bad movie. not the best restaurent'
    print (processSentence(sentence,posLex,negLex,tagger))   
