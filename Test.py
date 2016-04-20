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
    

    def __init__ (self, dimCorpus, nt):
        """
            dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di sents da usare
            
        """
        #self.folder = '//mnt//8tera//shareclic//lucaNgrams//Patrizio//'
#eredita qui
        #self = Tools (0)
        Tools.__init__ (self, 0)
        
        self.nc = max(dimCorpus)
        self.nt = nt        
        
        self.folderDati = self.folder + u"dati" + os.path.sep
        self.folderGrafici = self.folderDati + u"grafici" + os.path.sep
        self.folderPdfs = self.folderDati + u"pdfs" + os.path.sep
        self.folderPunkt = self.folder + u"punkt" + os.path.sep
        self.folderTestFiles = self.folder + u"testFiles" + os.path.sep

        print "Dim corpus:", dimCorpus
        
        self.dimCorpus = [DimSamplesPunkt().NumSents (dim) for dim in dimCorpus]
        
        if len(glob.glob (self.folderCorpus + '*')) == 0 or max (self.dimCorpus) == 0 \
                        or max (dimCorpus) != len(glob.glob (self.folderCorpus + '*')):

            import paisaSentsExtractor

            print "eliminazione corpus precedente..."
            
            self.DelAllFiles (self.folderCorpus)
            self.DelAllFiles (self.folderCorpusTraining)

            print "caricamento nuovo corpus"
            #carico il nuovo corpus
            paisaSentsExtractor.PaisaSentsExtractor (nwords = (self.nc + self.nt), folderdst = "corpus" + os.path.sep, folderList = {self.nc : "corpusTraining" + os.path.sep})
                       
        # dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di sents da usare
        #self.dimMyPunktTok = [DimSamplesPunkt().nSents (dim) for dim in dimTrainingMyPunktTok]

        self.AvviaTests ()

        
    def AvviaTests (self):
        #CANCELLO I DATI DEI TEST PRECEDENTI
        self._DellAllFiles ()   
    
        #controllo se i corpus sono già stati costruiti o sono da costruire
        self.CorpusDaCreare ()
#        if self.CorpusDaCreare ():   
#            import paisaSentsExtractor
#
#            print "eliminazione corpus precedente"    
#            #per prima cosa cancello i corpus precedenti
#            print "caricamento nuovo corpus"
#            #carico il nuovo corpus
#            paisaSentsExtractor.PaisaSentsExtractor (nwords = (self.nc + self.nt), folderdst = "corpus" + os.path.sep, folderList = {self.nc : "corpusTraining" + os.path.sep})
#                       
#            #creazione dei corpus
#            self.CreaCorpusOrigin ()    
            
        #avvio tutti i test con i parametri impostati
        TestTokenizer(fileRisultati = "Risultati", save = True, dimTests = self.dimCorpus, aggiornaDatiTest = False)
        
        #decido di separare i processi di test e di analisi
        #Analizzatore ()

    
#    def CreaCorpusOrigin (self):
#        #elimino i corpus precedenti
#        self.DelAllFiles (self.folderTestFiles)
#        #creo quelli nuovi
#        print "creazione dei corpus per i test in corso..."
#        for dim in self.dimTests:        
#            for paramS in self.TAGS.keys():
#                    for paramW in self.TAGW:
#                        self.n = dim
#                        self.CaricaCorpus ()
#                        self.CreaPlainText2 (paramS, paramW)
#                        
#                        print "Corpus %s %s %s creato correttamente" % (dim, paramS, paramW)
#                   
                   
    def CorpusDaCreare (self):
        r"""
            Questo metodo crea i corpus da utilizzare per i test       
        """
        
        for dim in self.dimTests:        
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
                        self.n = dim
                        self.CaricaCorpus ()
                        self.CreaPlainText2 (paramS, paramW)
                        print "Corpus %s %s %s creato correttamente" % (dim, paramS, paramW)

    
    def _DellAllFiles (self):
        #self.DelAllFiles (self.folderPunkt)
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

#def AvvioConEstrazioneDaPaisa ():
#    import paisaSentsExtractor
#
#    print "eliminazione corpus precedente"    
#    #per prima cosa cancello i corpus precedenti
#    a=Tools(0)
#    folder = '//mnt//8tera//shareclic//lucaNgrams//Patrizio//'    
#    a.DelAllFiles (folder + "corpus" + os.path.sep)
#    a.DelAllFiles (folder + "corpusTraining" + os.path.sep)
#    
#    print "caricamento nuovo corpus"
#    #carico il nuovo corpus
#    nc = 5000000
#    nt = 2500000
#    #my pc
##    nc = 50000
##    nt = 25000
##    
#    paisaSentsExtractor.PaisaSentsExtractor (nwords = (nc + nt), folderdst = "corpus" + os.path.sep, folderList = {nc : "corpusTraining" + os.path.sep})
#   
#    print "Avvio programma di TEST"
#    #avvio i tests  
#    #effettuo i test con dimensione nc, nc/2 e nc/4 che sono pari a:
#    # nc = 2000000
#    # nc/2 = 1000000
#    # nc/4 = 500000
#    Test (dimCorpus = [int(nc / 2), int(nc / 4), nc], nt)
#    
#    
#def AvvioSenzaEstrazioneDaPaisa ():
#    #carico il nuovo corpus
#    nc = 50000
#    
#    print "Avvio programma di TEST"
#    #avvio i tests  
#    #effettuo i test con dimensione nc, nc/2 e nc/4 che sono pari a:
#    # nc = 2000000
#    # nc/2 = 1000000
#    # nc/4 = 500000
#    Test (dimCorpus = [nc / 2, nc / 4, nc])
#
#
#def TestMode ():
#    print "test Mode"
#    print
#    print "dimensione dei test espressa in numero di parole. il numero differirà leggermente poichè approssimato alla fine della frase"
#    
#    dimCorpus = [1000, 2000]
#    
#    Test (dimCorpus)
                
if __name__ == '__main__':
    #AvvioConEstrazioneDaPaisa ()
    #AvvioSenzaEstrazioneDaPaisa ()
  
    #imposto le dimensioni e avvio i test
    nc = 5000000
    nt = 2500000     
    print "Avvio programma di test dei tokenizers"
    print 
    print "Numero parole nel corpus di test: %f" % nc
    print "Numero parole nel corpus di training: %f" % nt
    
    Test (dimCorpus = [int(nc / 2), int(nc / 4), nc], nt = nt)
    
    
    