# -*- coding: utf-8 -*-
"""
questo file avvia tutti i test, con differenti dimensioni di corpus e combinazioni
di tokenizer ed in fine analizza tutti i dati


            usato ereditarietà di:
            tools
                    
"""

from __future__ import division

#from Analizzatore import Analizzatore
from TestTokenizer import TestTokenizer
from DimSamplesPunkt import DimSamplesPunkt
from Tools import Tools

import sys
import glob
import os

class Test (Tools):
    r"""
        Questa classe avvia tutti i tests
    """
    
    def VERSION():
        return u"vers.0.3.5.b"
    

    def __init__ (self, dimCorpus):
        """
            dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di sents da usare
            
        """
        #self.folder = '//mnt//8tera//shareclic//lucaNgrams//Patrizio//'
#eredita qui
        #self = Tools (0)
        Tools.__init__ (self, 0)
        
        self.folderDati = self.folder + u"dati" + os.path.sep
        self.folderGrafici = self.folderDati + u"grafici" + os.path.sep
        self.folderPdfs = self.folderDati + u"pdfs" + os.path.sep
        self.folderPunkt = self.folder + u"punkt" + os.path.sep
        self.folderTestFiles = self.folder + u"testFiles" + os.path.sep

        print "Dim corpus:", dimCorpus
        
        self.dimCorpus = [DimSamplesPunkt().NumSents (dim) for dim in dimCorpus]
        
        # dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di sents da usare
        #self.dimMyPunktTok = [DimSamplesPunkt().nSents (dim) for dim in dimTrainingMyPunktTok]

        self.AvviaTests ()

        
    def AvviaTests (self):
        #CANCELLO I DATI DEI TEST PRECEDENTI
        self._DellAllFiles ()   
    
        #avvio tutti i test con i parametri impostati
        TestTokenizer(fileRisultati = "Risultati", save = True, 
            dimTests = self.dimCorpus, aggiornaDatiTest = False)
        
        print "Test creati con successo\navvio analisi dei dati"
        
        #decido di separare i processi di test e di analisi
        #Analizzatore ()


    def _DellAllFiles (self):
        #self.DelAllFiles (self.folderPunkt)
        print "Eliminazione test files precendenti"
        self.DelAllFiles (self.folderTestFiles)
        print "Elilminazione grafici precedenti"
        self.DelAllFiles (self.folderGrafici)
        print "Eliminazione pdfs precedenti"
        self.DelAllFiles (self.folderPdfs)
        print "Eliminazione file abbreviazioni precedenti"
        for file in glob.glob (self.folderDati + '*.abl'):
            self.DelFile (file)
        print "Eliminazione file stopwords precedenti"
        for file in glob.glob (self.folderDati + '*.stopWords'):
            self.DelFile (file)
            
    ########################################################################
        
###########################################################################    

def AvvioConEstrazioneDaPaisa ():
    import paisaSentsExtractor

    print "eliminazione corpus precedente"    
    #per prima cosa cancello i corpus precedenti
    a=Tools(0)
    folder = '//mnt//8tera//shareclic//lucaNgrams//Patrizio//'    
    a.DelAllFiles (folder + "corpus" + os.path.sep)
    a.DelAllFiles (folder + "corpusTraining" + os.path.sep)
    
    print "caricamento nuovo corpus"
    #carico il nuovo corpus
    nc = 5000000
    nt = 2500000
    #my pc
    nc = 50000
    nt = 25000
    
    paisaSentsExtractor.PaisaSentsExtractor (nwords = (nc + nt), folderdst = "corpus" + os.path.sep, folderList = {nc : "corpusTraining" + os.path.sep})
   
    print "Avvio programma di TEST"
    #avvio i tests  
    #effettuo i test con dimensione nc, nc/2 e nc/4 che sono pari a:
    # nc = 2000000
    # nc/2 = 1000000
    # nc/4 = 500000
    Test (dimCorpus = [int(nc / 2), int(nc / 4), nc])
    
    
def AvvioSenzaEstrazioneDaPaisa ():
    #carico il nuovo corpus
    nc = 50000
    
    print "Avvio programma di TEST"
    #avvio i tests  
    #effettuo i test con dimensione nc, nc/2 e nc/4 che sono pari a:
    # nc = 2000000
    # nc/2 = 1000000
    # nc/4 = 500000
    Test (dimCorpus = [nc / 2, nc / 4, nc])


def TestMode ():
    print "test Mode"
    print
    print "dimensione dei test espressa in numero di parole. il numero differirà leggermente poichè approssimato alla fine della frase"
    
    dimCorpus = [1000, 2000]
    
    Test (dimCorpus)
                
if __name__ == '__main__':
    #AvvioConEstrazioneDaPaisa ()
    AvvioSenzaEstrazioneDaPaisa ()
