# -*- coding: utf-8 -*-
"""
@author: Patrizio
"""

from __future__ import unicode_literals

import codecs


class PaisaSentsExtractor ():
    """ 
        questa classe si occupa di estrarre i dati dal file paisa e di salvarli 
        in files separati. uno per ogni frase
    """
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.4.1.b"
     
    def __init__(self, paisa = "paisa.annotated.CoNLL.utf8", nwords = -1,
                 folderdst = "corpus raw\\", folderList = {-1: "corpus raw\\"}):
        #per i conteggi uso i float per evitare overflow
        self.folderList = folderList
        self.folderdst = folderdst
        self.extfile = ".conll.txt"
        self.paisa_corpus = paisa
        self.nwords = nwords
        self.__Elabora()


    def __Elabora(self):
        
      #  with codecs.open(self.paisa_corpus, mode='r', encoding='utf-8') as f:   
        period = []
        nfile = float (0) #n di files scritti
        nwords = float (0) #n parole scritte
        
        fpaisa = codecs.open(self.paisa_corpus, mode='r', encoding='utf-8')
        while True:
#            try:
            line = fpaisa.read (1)
            if line[0] == u"<":
                if period[0] != u'#' and period[0] != u"" and len(period) > 1:
                    frase = []
                    period = u"".join (period)
                    if len(period.strip ()) > 1:
                        try:
                            #uso il costrutto try per evitare errori quando la substring manca
                            period = period[period.index (u">")+1:]
                            
                            for s in period.split (u"\n"):
                                if s != u'\n' and s != u"":
                                    if  len(s.split(u"\t")) == 8:
                                        s = s + u"\t_\t_\n"                                    
                                        frase.append (s)        
                                        nwords += 1
                                        
                                elif frase != []:                                
                                    filename = self.folderdst + str(nfile) + self.extfile                                
                                    print "saving file: ", filename                                
                                    with codecs.open(filename, mode = 'a', encoding = 'utf-8') as out:
                                        out.writelines (frase)
    
                                    nfile += 1
    
                                    #controllo se ho salvato il numero di parole desiderate
                                    if nwords >= self.nwords:
                                        return
                                        
                                    #controllo se devo cambiare folders
                                    if len(self.folderList.keys ()) > 0 and nwords >= min(self.folderList.keys ()):
                                        self.folderdst = self.folderList [min(self.folderList.keys())]
                                        del self.folderList[min(self.folderList.keys())]
                                    
                                    frase = []
                        except ValueError:
                            period = []
                    else:
                        period = []
                period = []
            period.append (line)

        fpaisa.close ()
if __name__=='__main__':
    print "Test Mode"
    print
    print "Estrazione di 15000 Parole in 3 cartelle differenti (a, b, c)"
    #PaisaSentsExtractor (nwords = 15000, folderdst = "corpus raw\\")#, folderList = {10000 : 'corpus training\\'})
    
    PaisaSentsExtractor (nwords = 15000, folderdst = "a\\", folderList = {5000 : 'b\\', 10000 : 'c\\'})
    
    print 'Processo terminato correttamente'
    