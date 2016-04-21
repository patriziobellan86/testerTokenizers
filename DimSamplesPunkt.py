# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 11:39:01 2016

@author: Patrizio
"""

import glob

from Tools import Tools
import os


class DimSamplesPunkt (Tools):
    r"""
        Questa classe si occupa del calcolo del numero di frasi dati il numero di parole
    """
    def __init__ (self, folderCorpus = u"corpus" + os.path.sep):
        
#        self.folder = os.path.sep + 'mnt' + os.path.sep + '8tera' + os.path.sep + 'shareclic' + os.path.sep + 'lucaNgrams' + os.path.sep + 'Patrizio' + os.path.sep + 'testerTokenizers' + os.path.sep
        #Tools.__init__(self, 0)
        #inizializzazione ereditarietà
        super (DimSamplesPunkt, self).__init__ (0)
        
        #parametro di classe
        self.folderCorpus =  self.folder + folderCorpus + os.path.sep
        #print "dimSamplePnktFolder", self.folderCorpus
        
        
    def NumSents (self, nWord):
        r"""            
            dato un numero di parole richiesto, restituisce il numero di frasi 
            si calcolano le frasi ordinate secondo l'ordine di lettura di glob, ordinate
            
            questo metodo restituisce un valore negativo quando si raggiunge la fine dei files
            senza aver estratto il numero desiderato di parole
            
            :param int nWord: numero di parole da estrarre
            
            :return: numero di frasi 
            :rtype: int
        """
        
        nsent = 0
        nw = 0
        nf = 1 #num file
        
        #lista files
        l = glob.glob(self.folderCorpus+'*.*')
        l.sort ()
        
        #ciclo di estrazione
        for f in l:
#new
            print "load file ", f, nf, "/", len(l)
            nf+=1
            nw = nw + len (self.LoadFile (f))
#old
            #nw = nw + len (Tools(0).LoadFile (f))
            nsent += 1
            print "nWord", nw, "/", nWord
            
            #controllo di essere arrivato al punto desiderato
            if nw >= nWord:
                return nsent
        #se non sono ancora uscito è perchè ho raggiunto la fine dei file
        print "fine files"
        return -nsent

            
if __name__ == '__main__':
    a=DimSamplesPunkt ()
    b = a.nSents (1000)
    print b
    c = a.nSents (10000)
    print c   
