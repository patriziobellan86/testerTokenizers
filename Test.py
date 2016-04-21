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
        return u"vers.0.3.8.3.a"
    

    def __init__ (self, dimCorpus, nt):
        """
            dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di frasi 
        """
     
        #eredita qui
        #Tools.__init__ (self, 0)
        super (Test, self).__init__(1)
        
        
        self.nc = max(dimCorpus) # numero max parole del corpus di test
        self.nt = nt             # numero max parole del corpus di training
        
        #parametri di classe
        self.folderDati = self.folder + u"dati" + os.path.sep
        self.folderGrafici = self.folderDati + u"grafici" + os.path.sep
        self.folderPdfs = self.folderDati + u"pdfs" + os.path.sep
        self.folderPunkt = self.folder + u"punkt" + os.path.sep
        self.folderTestFiles = self.folder + u"testFiles" + os.path.sep

#        print "Dim corpus:", dimCorpus
#        print "dim nc", self.nc
        
        #controllo se il numero massimo di parole da usare come corpus è già stato estratto
        #il metodo NumSents restituisce un numero negativo se raggiungo la fine dei files senza aver raggiunto
        #il valore desiderato
        if DimSamplesPunkt().NumSents (self.nc) < 0:
            #avvio l'estrazione dei dati da paisa            
            import paisaSentsExtractor

            print "eliminazione corpus precedente..."
        
            self.DelAllFiles (self.folderCorpus)
            self.DelAllFiles (self.folderCorpusTraining)

            print "caricamento nuovo corpus"
            
            #per evitare errori sovrastimo i valori di nc e nt del 10%
            ntot= (self.nc + self.nt)*1.1
            #avvio l'estrazione dei dati
            paisaSentsExtractor.PaisaSentsExtractor (nwords =ntot, folderdst = "corpus" + os.path.sep, folderList = {(self.nc*1.1) : "corpusTraining" + os.path.sep})
        
        #converto il corpus da num di parole a num di frasi
        self.dimCorpus = [DimSamplesPunkt().NumSents (dim) for dim in dimCorpus]
        
#        print max (dimCorpus)
#        print len(glob.glob (self.folderCorpus + '*'))
#        print self.dimCorpus

        self.AvviaTests ()

        
    def AvviaTests (self):
        #CANCELLO I DATI DEI TEST PRECEDENTI
        self._DellAllFiles ()   
    
        #controllo se i corpus sono già stati costruiti o sono da costruire
        self.CorpusDaCreare ()
            
        #avvio tutti i test con i parametri impostati
        TestTokenizer(fileRisultati = "Risultati", save = True, dimTests = self.dimCorpus, aggiornaDatiTest = False)
        
     
    def CorpusDaCreare (self):
        r"""
            Questo metodo crea i corpus da utilizzare per i test   
        """
        
        for dim in self.dimCorpus:        
            for paramS in self.TAGS.keys():
                for paramW in self.TAGW:  
                    filename = str(dim) + paramS + paramW
                    filename = self.folderTestFiles + filename + self.extCorpusData        
                    #se esiste continuo altrimenti ritorno e li costruisco
                    try:
                        with open(filename, "r"):
                            print "Corpus %s %s %s presente" % (dim, paramS, paramW)
                        continue
                    except IOError:
                        #self.n = dim
                        #self.CaricaCorpus ()
                        print "Creazione Corpus %s %s %s in corso..." % (dim, paramS, paramW)
                        self.CreaPlainText2 (paramS, paramW, dim)
                        print "Corpus %s %s %s creato correttamente" % (dim, paramS, paramW)

    
    def _DellAllFiles (self):
        r"""
            Questo metodo elimina i dati dei test precedenti   
        """
        self.DelAllFiles (self.folderPunkt)
        print "Eliminazione test files precendenti"
        self.DelAllFiles (self.folderTestFiles, escludeExt = self.extCorpusData)
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
 
    #imposto le dimensioni e avvio i test
    nc = 5000000
    nt = 2500000     
    
#    print "Temporaneo pretest"
#    nc = 5000
#    nt = 2500         
    
    print "Avvio programma di test dei tokenizers"
    print 
    print "Numero parole nel corpus di test: %f" % nc
    print "Numero parole nel corpus di training: %f" % nt
    
    Test (dimCorpus = [int(nc / 2), int(nc / 4), nc], nt = nt)
    
    
    