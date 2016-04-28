# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 15:57:18 2016

@author: Patrizio


            usato ereditarietà di:
            tools
                    
"""

from __future__ import division
from __future__ import unicode_literals

import nltk
from nltk.probability import FreqDist
from nltk import *
import glob
from Tools import Tools
from math import sqrt
import Queue
import threading
import multiprocessing
import os


class LogLikelihood (Tools):
    r"""
        Questa classe si occupa di effettuare la stima del parametro  
        log-likelihood inerente alle collocations 
        da utilizzare come parametro per la creazione dei MyPunkt Tokenizers
    """
    
    def VERSION (self):
        return "vers.3.8.b"
        
        
    def __init__ (self, n = -1):
        r"""
           
            :param int n: la dimensione su cui effettuare il calcolo del logl.
              
        """

        super (LogLikelihood, self).__init__ (n)

        self.__col_logl = list ()
        self.queue = Queue.Queue ()
        
        
    def __FreqFromCorpus (self):
        r"""
            Questo metodo estrae le frequenze dal corpus
        """
        print "Calcolo bigrams..."
        bi = FreqDist(bigrams(self.words))
        print "Calcolo FreqDist..."
        wfr = FreqDist(self.words)
        
        print "Coda di elaborazione..."
        print 
              
        tot = len(bi.keys())
        i = 0
        for eles in bi.keys():
            a = wfr[eles[0]]
            b = wfr[eles[1]]
            ab = bi[eles]
            N = wfr.N()
            try:
                self.__col_logl.append (nltk.tokenize.punkt.PunktTrainer()._col_log_likelihood  (a, b, ab, N))
                print "elemento %d / %d \t -> \tloglikelihood di %s %s \t\t ->  %f" % (i, tot,eles[0], eles[1], self.__col_logl[-1])
            except UnicodeEncodeError:
                #catturo eventuali errori di codifica
                pass
            i += 1
            
                       
    def LogLikelihood (self):
        r"""
            Questa funzione calcola la media dei logl.
            
            essendo k > 30 / 50 la distribuzione Gamma si approssima alla normale
            quindi sfrutto le proprietà della normale e stabilisco che una
            collocations è tale se rappresenta almeno circa il 30% del campione
              
            
            :return: i valori di logll.
            :rtype: list
        """
        self.__FreqFromCorpus ()
        #self.__MThreard ()
        
        
        mean = float( sum(self.__col_logl) / len(self.__col_logl))
        
        var = sum ([abs(x - mean) for x in self.__col_logl]) / len (self.__col_logl)
        
        logl = mean - sqrt(var) * 1
        
        print "mean:", mean
        print "var:%f   sigm:%f" %(var, sqrt(var))
        print "logl:", logl
        
        #salvo il logl trovato
        self.SaveByte ([logl], self.loglFilename) 
        
        return [logl]
        
    def LogLikelihoods (self):
        r"""
            Questo metodo calcola 3 loglikel. in base alle 3 dimensioni disponibili
            3* - tutto il campione
            2* - 2/3 del campione
            1* - 1/3 del campione
            
            :return: i valori di logll.
            :rtype: list
        """
        ress = []
        dimcorp = len(glob.glob (self.folderCorpus + '*.*'))
        #suddivido gli step
        for i in range(1,4):
            #calcolo il logl
            dim = int (i / 3 * dimcorp )
            print "Calcolo dimensione %d" % (dim)
            self.n = dim
            self.CaricaCorpus ()
            print "Corpus dati caricato, inizio calcolo log..."
            ress.append (self.LogLikelihood ()[0])
        #registro i dati
        self.DelFile (self.loglFilename)
        self.SaveByte (ress, self.loglFilename) 
        
        return ress
    
############################################################################

if __name__ == '__main__':
    LogLikelihood (-1).LogLikelihoods ()
