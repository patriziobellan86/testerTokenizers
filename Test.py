# -*- coding: utf-8 -*-
"""
questo file avvia tutti i test, con differenti dimensioni di corpus e combinazioni
di tokenizer ed in fine analizza tutti i dati
"""

from Analizzatore import Analizzatore
from TestTokenizer import TestTokenizer
from DimSamplesPunkt import DimSamplesPunkt

import sys

class Test ():
    r"""
        Questa classe avvia tutti i tests
    """
    
    def VERSION():
        return u"vers.0.3.5.b"
    

    def __init__ (self, dimCorpus, dimTrainingMyPunktTok):
        """
            dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di sents da usare
            
        """
        self.folderDati = u"dati\\"
        self.folderGrafici = self.folderDati + u"grafici\\"
        self.folderPdfs = self.folderDati + u"pdfs\\"
        self.folderPunkt = u"punkt\\"
        self.folderTestFiles = u"test files\\"
        
        self.dimCorpus = dimCorpus
        # dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di sents da usare
        self.dimMyPunktTok = [DimSamplesPunkt().nSents (dim) for dim in dimTrainingMyPunktTok]

        self.AvviaTests ()

        
    def AvviaTests (self):
        #CANCELLO I DATI DEI TEST PRECEDENTI
        self._DellAllFiles ()   
    
        #avvio tutti i test con i parametri impostati
        print "sistemare bene params in ingresso!!!!"
        TestTokenizer(fileRisultati = "Risultati", save = True, 
            dimTests = self.dimCorpus, aggiornaDatiTest = False, 
            dimsTrainTok = self.dimMyPunktTok)
        
        print "Test creati con successo\navvio analisi dei dati"
        Analizzatore ()

    def _DellAllFiles (self):
        #self.tools.DelAllFiles (self.folderPunkt)
        self.tools.DelAllFiles (self.folderTestFiles)
        self.tools.DelAllFiles (self.folderGrafici)
        self.tools.DelAllFiles (self.folderPdfs)
  
    ########################################################################
        
###########################################################################    
        
if __name__ == '__main__':
    print "test Mode"
    print
    print "imposta i parametri che vuoi!!!!!"
    
    dimCorpus = [1000, 2000]
    dimTrainingMyPunktTok = [100000, 500000]
    Tests (dimCorpus, dimTrainingMyPunktTok)
        