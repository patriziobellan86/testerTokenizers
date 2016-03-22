# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:43:31 2016

@author: Patrizio


"""


from __future__ import unicode_literals, division
import Queue
import threading
import multiprocessing
#import subprocess

#import collections
from Tools import Tools

import glob
import nltk
import os


class TextTiling:
    r""" Questa classe testa tutte le possibili combinazioni di opzioni di TextTiling """
    
    def VERSION(self):
        return u"0.3.8.1.a"
        
        
    def __init__(self, dim, paramS, paramW, save, nThread = -1):
        self.dim = dim
        self.paramS = paramS
        self.paramW = paramW
    
        self.nt = nThread   #numero di thread da utilizzare per i compiti
        
        self.folderDati = u"dati\\"
        self.fileExtStopW = u".stopWords"
        self.tools = Tools (0)  #Strumenti vari
        self.save = save
        self.folderTestFiles = u"test files\\"
        
        #BLOCK_COMPARISON, VOCABULARY_INTRODUCTION = 0, 1
        self.similarityMethod={'BLOCK_COMPARISON':0,'VOCABULARY_INTRODUCTION':1}       
        
        self.wParam=[20]    #Pseudosentence size
        self.kParam=[10]     #Size (in sentences) of the block used in the block comparison method 
    
        self.smoothingMethod=[[0]]   #DEFAULT_SMOOTHING = [0]  
        self.smoothingWidth=[2]   
        self.smoothingRounds=[1, 3, 5, 10]
    
        self.cutoffPolicy={'LC':0, 'HC':1}
        
        self.stopWords=glob.glob(self.folderDati + self.fileExtStopW)
        if not self.stopWords:
            import ItalianStopwords
            ItalianStopwords.AvviaCalcoli ()
            self.stopWords=glob.glob(self.folderDati + self.fileExtStopW)            
       
       
        self.D_w = 20 
        self.D_k = 10
        self.D_similarityMethod = self.similarityMethod['BLOCK_COMPARISON']
        self.D_stopWords = None
        self.D_smoothingMethod = [0]
        self.D_smoothingWidth = 2 
        self.D_smoothingRounds = 1
        self.D_cutoffPolicy = self.cutoffPolicy['HC']
        
        #old
#        self.queue = Queue.Queue()  #Queue per multithreading
#
#        #Variabile che contiene i risultati dei tests        
#        self.risultatiTest = dict ()

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
                self.stopWords,
                {e:e for e in self.smoothingWidth},
                {e:e for e in self.smoothingRounds},
                self.D_cutoffPolicy]

    ########################################################################
            
    def CreaTextTilingTokenizer (self, w, k, similarityMethod, stopWords,
        smoothingMethod, smoothingWidth, smoothingRounds, cutoffPolicy):
        
        return nltk.tokenize.TextTilingTokenizer (w = w, k = k, 
            similarity_method = similarityMethod, stopwords = stopWords,
            smoothing_method = smoothingMethod, smoothing_width = smoothingWidth,
            smoothing_rounds = smoothingRounds, cutoff_policy = cutoffPolicy)
        
    ########################################################################
 
#    ############old
#    def AvviaTests (self):
#        self.CaricaTests ()                
#        self.MThreard ()
#        
#        return self.risultatiTest
#        
#        
#    def CaricaTests(self):
#        for w in self.wParam:
#            for k in self.kParam:
#                for similarityMethod in self.similarityMethod:
#                    for smoothingMethod in self.smoothingMethod:
#                        for smoothingWidth in self.smoothingWidth:
#                            for smoothingRounds in self.smoothingRounds:  
#                                for cutoffPolicy in self.cutoffPolicy:
#                                    if self.stopWords == list():
#                                        self.stopWords = [None]
#                                    for fileStopW in self.stopWords:
#                                        if fileStopW:                                        
#                                            #carico il file delle stopWords
#                                            stopWords = self.tools.LoadByte (fileStopW)
#                                        else:
#                                            stopWords=None
#                                            
#                                        tok=nltk.tokenize.TextTilingTokenizer(w=w,
#                                             k=k,
#                                             similarity_method = self.similarityMethod[similarityMethod],
#                                             stopwords = stopWords,
#                                             smoothing_method = smoothingMethod,
#                                             smoothing_width = smoothingWidth,
#                                             smoothing_rounds = smoothingRounds,
#                                             cutoff_policy = self.cutoffPolicy[cutoffPolicy])
#                                    
#                                        testName = "TEXTTILING TOKENIZER"
#                                        testName = testName + u"w_" + unicode(str(w))
#                                        testName = testName + u"k_" + unicode(str(k))
#                                        testName = testName + u"_" + unicode(str(similarityMethod))
#                                        testName = testName + u"_" + unicode(str(smoothingMethod))
#                                        testName = testName + u"_" + unicode(str(smoothingWidth))
#                                        testName = testName + u"_" + unicode(str(smoothingRounds))
#                                        testName = testName + u"_" + unicode(str(cutoffPolicy))
#                                        if fileStopW:
#                                            testName = testName+u"_"+os.path.basename(fileStopW)
#                                        else:
#                                            testName = testName+u"_NONE"
#                                    
#                                        #Creo i dati per la coda
#                                        dati = tuple ([tok, testName])
#                                        # POPOLO LA CODA PER I THREAD
#                                        self.queue.put (dati)
#                                   
#                                    
#    def TestTok (self):
#        corpusObj = Tools (self.dim)
#        corpusObj.CaricaCorpus ()    
#        
#        while True:
#            tok, testName = self.queue.get()
#            
#            #testName=u"TEXTTILING TOKENIZER"
#            s=u"\n   TEST : {}".format(testName)
#            try:
#                datiOut = tok.tokenize(self.corpus)
#                s = u"\nTEST : {}".format (testName)  
#                
#                datiOut =  tok.tokenize (corpusObj.CreaPlainText (tagS = self.paramS, tagW = self.paramW)) 
#                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst)
#                self.tools.PrintOut (r)
#                
#                s = s + r +u"\nTEST COMPLETATO CON SUCCESSO"
#                self.tools.PrintOut (s)
#                                    
#                if self.save:
#                    #Salvo il file elaborato dal tokenizzatore
#                    filename = self.folderTestFiles + u" " + self.paramS + u" "  + \
#                        self.paramW + u" " +  unicode(self.dim) + u" "  + testName + u".txt"
#                    self.tools.SaveFile (filename = filename, dati = datiOut)
#                    
#            except :    #ValueError, NotImplementedError:
#                print "test non applicabile a questo corpus"
#            #aggiorno la variabile dei risultati
#            self.risultatiTest[testName] = score
#            
#            self.queue.task_done()
#
#
#    #lancio tutti i threads
#    def MThreard (self):
#        # non ho bisogno di tener traccia dei risultati perchè
#        # vengono già memorizzati nei vari files
#
#        #numero di threads
#        if self.nt == -1 :
#            nThread = multiprocessing.cpu_count()  
#        else:
#            nThread = self.nt
#
#        #lancio l'eseguzione dei tests
#        while not self.queue.empty ():
#            #avvio tanti threads quanti sono il numero di processori logici
#            #disponibili
#            for  i in xrange (nThread):
#                t = threading.Thread(target = self.TestTok)
#                t.daemon = True
#                t.start ()
               
                         
if __name__=='__main__':
    print "Test Mode non eseguibile"
#    a=TextTiling()
    
    
    