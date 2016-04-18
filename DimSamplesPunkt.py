# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 11:39:01 2016

@author: Patrizio
"""
import glob

from Tools import Tools
import os


class DimSamplesPunkt (Tools):
    def __init__ (self, folderCorpus = u"corpus" + os.path.sep):
        
#        self.folder = os.path.sep + 'mnt' + os.path.sep + '8tera' + os.path.sep + 'shareclic' + os.path.sep + 'lucaNgrams' + os.path.sep + 'Patrizio' + os.path.sep + 'testerTokenizers' + os.path.sep
        Tools.__init__(0)
        
        self.folderCorpus =  self.folder + folderCorpus + os.path.sep

    def nSents (self, nWord):
        r"""            
            dato un numero di parole richiesto, restituisce il numero di frasi 
            si calcolano le frasi ordinate secondo l'ordine di lettura di glob
        """
        nsent = 0
        nw = 0
	print self.folderCorpus
        l = glob.glob(self.folderCorpus+'*')
        for f in l:
            nw = nw + len (Tools(0).LoadFile (f))
            nsent += 1
            if nw >= nWord:
                return nsent
        print "fine files"
        return nsent

            
if __name__ == '__main__':
    a=DimSamplesPunkt ()
    b = a.nSents (1000)
    print b
    c = a.nSents (10000)
    print c   
