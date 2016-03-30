# -*- coding: utf-8 -*-
"""
questo file avvia tutti i test, con differenti dimensioni di corpus e combinazioni
di tokenizer ed in fine analizza tutti i dati
"""

from __future__ import division

from Analizzatore import Analizzatore
from TestTokenizer import TestTokenizer
from DimSamplesPunkt import DimSamplesPunkt
from Tools import Tools

import sys
import glob

class Test ():
    r"""
        Questa classe avvia tutti i tests
    """
    
    def VERSION():
        return u"vers.0.3.5.b"
    

    def __init__ (self, dimCorpus):
        """
            dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di sents da usare
            
        """
        
        self.folderDati = u"dati\\"
        self.folderGrafici = self.folderDati + u"grafici\\"
        self.folderPdfs = self.folderDati + u"pdfs\\"
        self.folderPunkt = u"punkt\\"
        self.folderTestFiles = u"test files\\"
        self.tools = Tools (0)
        self.dimCorpus = [DimSamplesPunkt().nSents (dim) for dim in dimCorpus]
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
        Analizzatore ()


    def _DellAllFiles (self):
        #self.tools.DelAllFiles (self.folderPunkt)
        print "Eliminazione test files precendenti"
        self.tools.DelAllFiles (self.folderTestFiles)
        print "Elilminazione grafici precedenti"
        self.tools.DelAllFiles (self.folderGrafici)
        print "Eliminazione pdfs precedenti"
        self.tools.DelAllFiles (self.folderPdfs)
        print "Eliminazione file abbreviazioni precedenti"
        for file in glob.glob (self.folderDati + '*.abl'):
            self.tools.DelFile (file)
        print "Eliminazione file stopwords precedenti"
        for file in glob.glob (self.folderDati + '*.stopWords'):
            self.tools.DelFile (file)
            
    ########################################################################
        
###########################################################################    

def AvvioConEstrazioneDaPaisa ():
    import paisaSentsExtractor

    print "eliminazione corpus precedente"    
    #per prima cosa cancello i corpus precedenti
    a=Tools(0)
    
    a.DelAllFiles ("corpus\\")
    a.DelAllFiles ('corpus training\\')
    
    print "caricamento nuovo corpus"
    #carico il nuovo corpus
    nc = 200000
    nt = 150000
    
    paisaSentsExtractor.PaisaSentsExtractor (nwords = (nc + nt), folderdst = "corpus\\", folderList = {nc : 'corpus training\\'})
   
    print "Avvio programma di TEST"
    #avvio i tests  
    #effettuo i test con dimensione nc, nc/2 e nc/4 che sono pari a:
    # nc = 2000000
    # nc/2 = 1000000
    # nc/4 = 500000
    Test (dimCorpus = [nc / 2, nc / 4, nc])
    
    
def AvvioSenzaEstrazioneDaPaisa ():
    #carico il nuovo corpus
    nc = 20000
    
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