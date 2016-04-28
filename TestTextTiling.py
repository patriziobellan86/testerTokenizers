# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:43:31 2016

@author: Patrizio


"""


from __future__ import unicode_literals, division

from Tools import Tools

import glob
import nltk


class TextTiling (Tools):
    r""" Questa classe testa tutte le possibili combinazioni di opzioni di TextTiling """
    
    def __init__(self):   
        super (TextTiling, self).__init__ ()
       
        #BLOCK_COMPARISON, VOCABULARY_INTRODUCTION = 0, 1
        self.similarityMethod={'BLOCK_COMPARISON':0,'VOCABULARY_INTRODUCTION':1}       
        
        self.wParam=[20]    #Pseudosentence size
        self.kParam=[10]     #Size (in sentences) of the block used in the block comparison method 
    
        self.smoothingMethod=[[0]]   #DEFAULT_SMOOTHING = [0]  
        self.smoothingWidth=[2]   
        self.smoothingRounds=[1, 3, 5, 10]
    
        self.cutoffPolicy={'LC':0, 'HC':1}
        
        self.stopWords = glob.glob (self.folderDati + '*' + self.fileExtStopW)
        
        if not self.stopWords:
            import ItalianStopWords
            ItalianStopWords.ItalianStopWords().StopWords ()
            self.stopWords = glob.glob (self.folderDati + '*' + self.fileExtStopW)            
       
        self.D_w = 20 
        self.D_k = 10
        self.D_similarityMethod = self.similarityMethod['BLOCK_COMPARISON']
        self.D_stopWords = self.stopWords[0]
        self.D_smoothingMethod = [0]
        self.D_smoothingWidth = 2 
        self.D_smoothingRounds = 1
        self.D_cutoffPolicy = self.cutoffPolicy['HC']

        ########################################################################

    def GetStandardParams (self):
        r"""
            Questo metodo restituisce un'array contenente tutti i parametri di default
        """
        return [ self.D_w, self.D_k, self.D_similarityMethod, self.D_stopWords,
                 self.D_smoothingMethod, self.D_smoothingWidth, 
                 self.D_smoothingRounds, self.D_cutoffPolicy]            
    
    
    def GetAllParams (self):
        r"""
            Questo metodo restituisce un'array contenente tutti i parametri con tutte le varianti
        """
        return [{e:e for e in self.wParam},
                {e:e for e in self.kParam},
                self.similarityMethod,
                {e:e for e in self.stopWords},
                {e:e for e in self.smoothingWidth},
                {e:e for e in self.smoothingRounds},
                self.D_cutoffPolicy]

    ########################################################################
            
    def CreaTextTilingTokenizer (self, w, k, similarityMethod, stopWords,
        smoothingMethod, smoothingWidth, smoothingRounds, cutoffPolicy):
            
        stopWords = self.tools.LoadByte (stopWords)
        
        return nltk.tokenize.TextTilingTokenizer (w = w, k = k, 
            similarity_method = similarityMethod, stopwords = stopWords,
            smoothing_method = smoothingMethod, smoothing_width = smoothingWidth,
            smoothing_rounds = smoothingRounds, cutoff_policy = cutoffPolicy)
        
    ########################################################################
 
                         
if __name__=='__main__':
    print "Test Mode non eseguibile"

    
    
