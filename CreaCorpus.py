# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 16:48:23 2016

@author: patrizio
"""

from __future__ import division

from DimSamplesPunkt import DimSamplesPunkt
from Tools import Tools

import os

class CreaCorpus (Tools):
    def __init__ (self, dimCorpus, nt):
        """
            dimTrainingMyPunktTok è espresso in numero di parole, viene trasformato in numero di sents da usare
            
        """
     
#eredita qui
        #Tools.__init__ (self, 0)
        super (CreaCorpus, self).__init__(1)
        
        self.nc = max(dimCorpus)
        self.nt = nt        
        
        self.folderDati = self.folder + u"dati" + os.path.sep
        self.folderGrafici = self.folderDati + u"grafici" + os.path.sep
        self.folderPdfs = self.folderDati + u"pdfs" + os.path.sep
        self.folderPunkt = self.folder + u"punkt" + os.path.sep
        self.folderTestFiles = self.folder + u"testFiles" + os.path.sep

        #converto il corpus da num di parole a num di frasi
        self.dimCorpus = [DimSamplesPunkt().NumSents (dim) for dim in dimCorpus]
        
        self.CorpusDaCreare ()
            

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

    
    ########################################################################
        
###########################################################################    

                
if __name__ == '__main__':
 
    #imposto le dimensioni e avvio i test
    print "Temporaneo pretest"
    nc = 5000000
    nt = 2500000     
  
    
    CreaCorpus (dimCorpus = [nc], nt = nt)
    
    
    