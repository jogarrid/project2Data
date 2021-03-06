   

import pandas as pd
import numpy as np
import scipy
import re
import gensim

from sklearn.feature_extraction.text import TfidfVectorizer

"""
Functions to obtain the 4 different text representations with which we do classification.
This functions are later called from within LoadData.py
"""

def get_mean_w2v_embeddings(titles,word2vec_model):
    """ 
    Using the model WORD2VEC_MODEL which has been pretrained (it is google's pretrained model in 
    our case), and that associates words to vectors, go from a sentence (TITLE) to a vector by summing the vectorial representation of all the words in a title
    """
    embs = []
    for title in titles:
        title_emb = np.zeros(300)
        words = title.split(' ')
        for w in words:
            if w in word2vec_model:
                scalar = 1.
#               scalar = 1. / len(words)  
                vector = word2vec_model[w]   
                title_emb += scalar * vector
        embs.append(title_emb)
    return embs

def get_tfidf_w2v_embeddings(titles, word2vec_model):
    """ 
    Using the model WORD2VEC_MODEL which has been pretrained (it is google's pretrained model in 
    our case), and that associates words to vectors, go from a sentence (TITLE) to a vector by summing the vectorial representation of all the words in TITLE
    multiplying the vector of every word by the tf-idf measure of its relative importance in the text.
    """
    tfidf_vect = TfidfVectorizer()
    titles_tfidf_matrix = tfidf_vect.fit_transform(titles)
    # have matrix, where rows are titles and cols are words from vocabulary
    tfidf_words_indices = {word : index for (word, index) in tfidf_vect.vocabulary_.items()}
    embs = []
    for i in range(len(titles)):
        title = titles.iloc[i]
        words = title.split(' ')
        
        # make sparse matrix row a dict:
        matrix_row = titles_tfidf_matrix[i]
        matrix_row_dict = {}
        indices = matrix_row.indices
        data    = matrix_row.data
        for i in range(len(data)):
            matrix_row_dict[indices[i]] = data[i]
        
        title_emb = np.zeros(300)
        for w in words:
            if w in word2vec_model:
                vector = word2vec_model[w]
                
                if w in tfidf_words_indices:
                    word_index = tfidf_words_indices[w]
                    scalar = matrix_row_dict.get(word_index, 0)
                else:
                    scalar = 1. / len(words) # take scalar as in mean
#                   scalar = 1.
                
                title_emb += scalar * vector
                
        embs.append(title_emb)
    return embs

def get_sent2vec_embeddings(titles, sent2vec_model):
    """
    Find vectorial representation of the sentence TITLE using the sent2vec model
    """
    lists = sent2vec_model.embed_sentences(titles.values)
    return [np.asarray(lists[i]) for i in range(len(lists))]

    return sent2vec_model.embed_sentences(titles.values)

