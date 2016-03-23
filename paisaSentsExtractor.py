# -*- coding: utf-8 -*-
"""
@author: Patrizio
"""

from __future__ import unicode_literals

import codecs


class PaisaSentsExtractor():
    """ 
        questa classe si occupa di estrarre i dati dal file paisa e di salvarli 
        in files separati. uno per ogni frase
    """
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.3.1.a"
     
    def __init__(self, paisa = "paisa.annotated.CoNLL.utf8", nsents = -1,
                 folderdst = "corpus raw\\", folderList = {-1: "corpus raw\\"}):
        #per i conteggi uso i float per evitare overflow
        self.folderList = folderList
        self.folderdst = folderdst
        self.extfile = ".conll.txt"
        self.paisa_corpus = paisa
        self.nsents = nsents
        self.__Elabora()


    def __Elabora(self):

      #  with codecs.open(self.paisa_corpus, mode='r', encoding='utf-8') as f:   
        period = []
        nfile = float (0)
        fpaisa = codecs.open(self.paisa_corpus, mode='r', encoding='utf-8')
        while True:
            try:
                line = fpaisa.read (1)
                if line[0] == u"<":
                    if period[0] != u'#' and period[0] != u"" and len(period) > 1:
                        frase = []
                        period = u"".join (period)
                        period = period[period.index (u">")+1:]
                        
                        for s in period.split (u"\n"):
                            if s != u'\n' and s != u"":
                                s = s[:-1] + u"\t_\t_\n"
                                frase.append (s)        
                
                            elif frase != []:                                
                                filename = self.folderdst + str(nfile) + self.extfile                                
                                print "saving file: ", filename                                
                                with codecs.open(filename, mode = 'a', encoding = 'utf-8') as out:
                                    out.writelines (frase)
                                nfile += 1
                                if nfile == 16:
                                    pass
                                if self.nsents != -1 and nfile > self.nsents:
                                    return
                                    
                                
                                if nfile in self.folderList.keys ():
                                    self.folderdst = self.folderList [nfile]
                                    del self.folderList [nfile]
                                frase=[]
                      
                    period = []
                period.append (line)
            except:
                print "fine dati"
        fpaisa.close ()
if __name__=='__main__':
    print "Test Mode"
    print
    print "Estrazione di 500000 frasi"
    #PaisaSentsExtractor (nsents = 1000010, folderList = {300000 : 'corpus training', 1000001: ""})
    PaisaSentsExtractor (nsents = 1000, folderList = {30 : 'corpus training\\', 10: ""})
    print 'Processo terminato correttamente'
    