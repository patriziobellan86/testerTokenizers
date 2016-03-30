# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 15:57:18 2016

@author: Patrizio
"""

from __future__ import division

import nltk
from nltk.probability import FreqDist
from nltk import *
import glob
from Tools import Tools
from math import sqrt
import Queue
import threading
import multiprocessing

class LogLikelihood ():
    r"""
        Questa classe si occupa di effettuare la stima del parametro  
        log-likelihood inerente alle collocations 
        da utilizzare come parametro per la creazione dei MyPunkt Tokenizers
    """
    
    def VERSION (self):
        return "vers.0.1.a"
        
        
    def __init__ (self, n = -1):
        r"""
            il parametro n indica la quantità di frasi da utilizzare come
            campione su cui effettuare il test
            il parametro folder indica la cartella da cui caricare le frasi
        """
        self.folderDati = "dati\\"
        self.loglFilename = self.folderDati + "loglikelihood.pickle"
        self.__tools = Tools (n) #default -1, cioè tutto il campione
        self.__col_logl = list ()
        self.queue = Queue.Queue ()
        
        self.__tools.CaricaCorpus ()



    def __FreqFromCorpus (self):
        bi = FreqDist(bigrams(self.__tools.words))
        wfr = FreqDist(self.__tools.words)
        
        #popolo la coda        
        for eles in bi.keys():
            a = wfr[eles[0]]
            b = wfr[eles[1]]
            ab = bi[eles]
            N = wfr.N()
            
            self.queue.put(tuple([a, b, ab, N]))
        
    
    def __CalcolaLogL (self):
        while True:
            a, b, ab, N = self.queue.get ()
            
            self.__col_logl.append (nltk.tokenize.punkt.PunktTrainer()._col_log_likelihood  (a, b, ab, N))

            self.queue.task_done()
    
    
    #lancio tutti i threads
    def __MThreard (self):
        #numero di threads
        nThread = multiprocessing.cpu_count()  
        
        while not self.queue.empty ():
            #avvio tanti threads quanti sono il numero di processori logici
            #disponibili
            for  i in xrange (nThread):
                t = threading.Thread(target = self.__CalcolaLogL)
                t.daemon = True
                t.start ()
                       
                       
    def LogLikelihood (self):
        r"""
            Questa funzione calcola la media dei logl.
            
            essendo k > 30 / 50 la distribuzione Gamma si approssima alla normale
            quindi sfrutto le proprietà della normale e stabilisco che una
            collocations è tale se rappresenta almeno circa il 30% del campione
        """
        self.__FreqFromCorpus ()
        self.__MThreard ()
        
        
        mean = float( sum(self.__col_logl) / len(self.__col_logl))
        
        var = sum ([abs(x - mean) for x in self.__col_logl]) / len (self.__col_logl)
        
        logl = mean - sqrt(var) * 1
        
        print "mean:", mean
        print "var:%f   sigm:%f" %(var, sqrt(var))
        print "logl:", logl
        
        #salvo il logl trovato
        self.__tools.SaveByte ([logl], self.loglFilename) 
        
        return [logl]
        
    def LogLikelihoods (self):
        r"""
            Questo metodo calcola 3 loglikel. in base alle 3 dimensioni disponibili
            3* - tutto il campione
            2* - 2/3 del campione
            1* - 1/3 del campione
        """
        ress = []
        dimcorp = len(glob.glob (self.__tools.folderCorpus + '*.*'))
        #suddivido gli step
        for i in range(1,4):
            #calcolo il logl
            dim = int (i / 3 * dimcorp )
            self.__tools.n = dim
            self.__tools.CaricaCorpus ()
            ress.append (self.LogLikelihood ()[0])
        #registro i dati
        self.__tools.DelFile (self.loglFilename)
        self.__tools.SaveByte (ress, self.loglFilename) 
        
        return ress
    
############################################################################

class TestLogLikelihood ():
    r"""
        Questa classe modella la batteria di test da effettuare
    """
    def __init__ (self, batterie = [-1], filename = "TestLogLikelihood_newTests.csv"):
        r"""
            Il parametro batterie è una lista contenente i valori di numerosità
            del campione su cui andare ad effettuare i tests
        """
        self.folderDati = "dati\\"
        self.testFilename = self.folderDati + filename 
                       
        self.tools = Tools(1)
        
        self.AvviaTests (batterie)

    
    def AvviaTests (self, batterie):
        
        for dim in batterie:
            print "Avvio Test su %d campioni" % dim
            #Effettuo il test
            test = LogLikelihood (n = dim)
            #registro i dati
            filename = self.testFilename
            result = test.LogLikelihood ()
            
            print "LogLikelihood pari a %f" % result
            #salvo i log trovati    
            self.tools.SaveTestCsv (filename = filename,testName = "Loglikelihood",
                                    nSamples = dim, result = result)
            
            self.tools.SaveByte (result, self.loglFilename)                        
        print "Tests Eseguiti correttamente"
        
 
def TestClasseDiCalcolo ():
    a = LogLikelihood (n = 1000)
    print "la sogla logLikelihood sul campione è:", a.LogLikelihood ()


def BatterieDiTest ():
    batterieTests = [5000, 10000, 15000, 20000, 25000, 50000, 100000]
    TestLogLikelihood (batterie = batterieTests)

if __name__ == '__main__':
#    BatterieDiTest ()
#    TestClasseDiCalcolo ()
    LogLikelihood (-1).LogLikelihood ()