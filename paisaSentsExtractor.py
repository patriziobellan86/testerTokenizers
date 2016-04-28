# -*- coding: utf-8 -*-
"""
@author: Patrizio
"""

from __future__ import unicode_literals

import codecs
import os
from Tools import Tools


class PaisaSentsExtractor (Tools):
    """ 
        questa classe si occupa di estrarre i dati dal file paisa e di salvarli 
        in files separati. uno per ogni frase
    """
 
    def VERSION (self):
        return "1.0.a-Lite"
     
     
    def __init__(self, nwords = -1,
                 folderdst = "corpusRaw" + os.path.sep, folderList = {-1: "corpus raw" + os.path.sep}):
        r"""
            direttamente durante la creazione dell'oggetto parte l'elaborazione dei dati
            
            :param str paisa: path al file
            :param int nwords: numero di parole totali che si vuole estrarre
            :param str folderdst: folder di destrinazione delle frasi estratte
            :param dict folderList: dizionario formato da:
                                key -> da quale numero di parole iniziare a salvare 
                                value->la folder dove salvare
                                
            :return: None
            
            esempio:
            
            >>>  PaisaSentsExtractor (nwords = 15000, paisa = paisaFilename, folderdst = "a" + os.path.sep, folderList = {5000 : 'b' + os.path.sep, 10000 : 'c' + os.path.sep})
            estrarrà:
            15000 parole, dal file paisaFilename
            salvandole per prima nella folder a
            giunto a 5000 le salva nella folder b
            giunto a 10000 le salva nella folder c
        """             
   
        super (PaisaSentsExtractor, self).__init__ (0)

        self.folderList = folderList

        self.folderdst = folderdst
  
        self.extfile = ".conll.txt"
      
        self.paisa_corpus = self.CaricaParametro(parametro = 'paisa')
        
        self.nwords = nwords

        self.__Elabora()


    def __Elabora(self):
        period = []
        nfile = float (0) #n di files scritti
        nwords = float (0) #n parole scritte
        
        fpaisa = codecs.open(self.paisa_corpus, mode='r', encoding='utf-8')
        while True:
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
                                    print "saving file: ", filename, "nword %d / %d" % (nwords, self.nwords)   
                                    
                                    with codecs.open(filename, mode = 'a', encoding = 'utf-8') as out:
                                        out.writelines (frase)
    
                                    nfile += 1
    
                                    #controllo se ho salvato il numero di parole desiderate
                                    if nwords >= self.nwords:
                                        return
                                        
                                    #controllo se devo cambiare folders
                                    if len(self.folderList.keys ()) > 0 and nwords >= min(self.folderList.keys ()) and self.folderList.keys() != [-1]:
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
    print "test mode non funzionante"
#    
#    print "Estrazione di 15000 Parole in 3 cartelle differenti (a, b, c)"
#   
#    PaisaSentsExtractor (nwords = 15000, folderdst = "corpusRaw" + os.path.sep)   #, folderList = {10000 : 'corpus training' + os.path.sep})
#   
#    #PaisaSentsExtractor (nwords = 15000, paisa = paisaFilename, folderdst = "a" + os.path.sep, folderList = {5000 : 'b' + os.path.sep, 10000 : 'c' + os.path.sep})
#    
#    print 'Processo terminato correttamente'
    
