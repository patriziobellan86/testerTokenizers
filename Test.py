# -*- coding: utf-8 -*-
"""
questo file avvia tutti i test, con differenti dimensioni di corpus e combinazioni
di tokenizer ed in fine analizza tutti i dati
"""

from Tools import Tools
from TestTokenizer import TestTokenizer
from CreatorePunktTokenize import MyPunktTokenize

class Test ():
    r"""
        Questa classe avvia tutti i tests
    """
    
    def VERSION():
        return u"vers.0.3.5.b"
    

    def __init__ (self, dimCorpus, dimMyPunktTok):
        self.folderDati = u"dati\\"
        self.folderPunkt = u"punkt\\"
        self.folderTestFiles = u"test files\\"
        
        self.dimCorpus = dimCorpus
        self.dimMyPunktTok = dimMyPunktTok
        
        self.tools = Tools ()
        self.paramCorpusCreationW = self.tools.TAGW
        self.paramCorpusCreationS = self.tools.TAGS.keys()
      
        self.test = TestTokenizer (fileRisultati = "Risultati", n = 10, save = True)
        self.AvviaTests ()

        
    def CreaMyPukntTok (self):
        for dim in self.dimMyPunktTok:
            print "Creazione MypunktTok su %s campioni" % (dim)
            MyPunktTokenize(dim)
        
        
    def AvviaTests (self):
        #CANCELLO I DATI DEI TEST PRECEDENTI
        self._DellAllFiles ()        
        #self.CreaMyPukntTok ()
    
    
    
        #PARTO DAL TEST DEL SIMPLE SPACE TOKENIZER
        for dim in self.dimCorpus:
            print "Avvio su un campione di ", dim, "elementi"
            filenameRes = u"Risultati " + unicode(dim)
        
            TestTokenizer(fileRisultati = filenameRes, n = dim, save = True).AvviaTests ()       
        



    def AllTestsSimpleSpaceTokenizerWord (self):
        #per prima cosa avvio il test nella condizione più semplice
        paramS = u'SPACE'
        paramW = u'PARAG_2'
        #creo il corpus da utilizzare per i tests
        self.tools.CreaPlainText (tagS = paramS, tagW = paramW)
        
        score = self.test.TestSimpleSpaceTokenizerWord (self.tools.corpusTxt, paramS, paramW)
        
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            if self.EuristicaNoZeroAll :
                if self.EuristicaPrestazioniMedie (soglia = 0.75):
                    print "Test Passato \n dati da registrare"



        
    def _DellAllFiles (self):
        #self.tools.DelAllFiles (self.folderPunkt)
        self.tools.DelAllFiles (self.folderTestFiles)
    
    ########################################################################
    #######################  EURISTICHE  ###################################
    ########################################################################
    def EuristicaNoZero (self, testResult):
        r"""
            Questa euristica rappresenta la condizione minima per proseguire
            con i tests
            il risultato del test non deve essere zero
        """
        print "TODO"
        if testResult:
            return True
        else:
            return False


    def EuristicaNoZeroAll (self, test):
        r""" 
            Questa euristica rappresenta la condizione minima per proseguire 
            con i tests
            il test deve ottenere risultati diversi da zero in ogni condizione
        """
        print "TODO"
        for t in test:
            risultatiTest = t
            self.EuristicaNoZero (risultatiTest)


    def EuristicaPrestazioniMedie (self, testResults, soglia):
        r"""
            
            il test deve ottenere delle prestazioni medie sopra il valore soglia
        """
        print "TODO"
        
        
    def EuristicaDelMiglioramento (self, testResults):
        r"""
            
            il test deve ottenere prestazioni in rapporto diretto con le 
            dimensioni del campione di test. 
            se i risultati non migliorano con il crescere del numero di campioni
            il test è scartato
        """
        print "TODO"
    ########################################################################
        
        
###########################################################################       
       
def Tests():
    #dimensione del corpus da testare in numero di frasi
    ncorpus=[50,100,250]#,500,1000,5000,15000,30000]
    #dimensione del corpus con cui addestrare i tokenizer
    nTok = [1000, 15000]
    #Avvio i Tests
    Test(dimCorpus = ncorpus, dimMyPunktTok = nTok)


if __name__ == '__main__':
    Tests ()
        