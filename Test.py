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

from Tools import Tools


import glob
import os


class Test (Tools):
    r"""
        Questa classe avvia tutti i tests
    """
    def VERSION (self):
        return "1.0.a-Lite"
        
    def __init__ (self): #, dimCorpus, nt):
        """
            #dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di sents da usare
            
        """
        
        super (Test, self).__init__(0)
        
        self.nc = int (self.CaricaParametro(parametro = 'wordsTest')) #max(dimCorpus)
        self.nt = int (self.CaricaParametro(parametro = 'wordsTraining'))        
        
        #controllo se il numero massimo di parole da usare come corpus è già stato estratto
        if self.NumSents (self.nc) <= 0:
            import paisaSentsExtractor

            print "eliminazione corpus precedente..."
            
            self.DelAllFiles (self.folderCorpus)
            self.DelAllFiles (self.folderCorpusTraining)

            print "caricamento nuovo corpus"
            #carico il nuovo corpus
            
            #per evitare errori sovrastimo i valori di nc e nt del 10%
            ntot= (self.nc + self.nt)*1.1
            paisaSentsExtractor.PaisaSentsExtractor (nwords = ntot, folderdst = self.folderCorpus + os.path.sep, folderList = {(self.nc*1.1) : self.folderCorpusTraining + os.path.sep})
        
        #converto il corpus da num di parole a num di frasi
        self.dimCorpus = [self.NumSents (dim) for dim in (self.nc, int(self.nc / 2), int(self.nc / 4))]
        
        self.AvviaTests ()

        
    def AvviaTests (self):
       
#        #CANCELLO I DATI DEI TEST PRECEDENTI
        self._DellAllFiles ()   
    
        #avvio tutti i test con i parametri impostati
        TestTokenizer(fileRisultati = "Risultati", save = True, dimTests = self.dimCorpus, aggiornaDatiTest = False)
       
       
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

                
if __name__ == '__main__':
    
    print "Avvio Programma di Test..."
    Test ()    
    
    