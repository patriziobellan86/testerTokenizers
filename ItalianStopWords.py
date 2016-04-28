# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 11:12:09 2016

@author: Patrizio


"""
from __future__ import unicode_literals
from __future__ import division

from Tools import Tools

import collections 
import re
import nltk
from math import sqrt, log
import glob
import os

def IsAlpha (string):
    #dato che lavoro con unicode non posso usare il metodo isalpha della classe str
    alls=u"qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMèéòàùì"
    for l in string:
        if not l in alls:
            return False
    return True
    
########################################################################### 
    
class IDF(Tools):
    
    def __init__(self, n = -1):
        #dichiarazione ereditarietà
        super (IDF, self).__init__(n)
        #var di classe
        self.D = 0
        self.KD = collections.defaultdict (int)
        self.idfs = dict ()
        
        self.CaricaCorpus()               
    
    
    def AvviaCalcoli (self):
        self.VocsDocs ()
        self.IDFs ()
        
        
    def VocsDocs (self):
        docs = self.CreaDocs (self.sents)
        self.D =len(docs)

        for doc in docs:
            for voc in set(doc):
                if IsAlpha (voc):
                    self.KD[voc.lower()] += 1
                
                
    def IDFs (self):
        r"""
            Questo metodo computa il valore idf per ogni termine
        """        
        for voc in self.KD.keys ():
            self.idfs[voc] = self.CalcolaIdf (self.D, self.KD[voc])
            
            
    def CalcolaIdf (self, D, kd):
        return log(D / kd)
        
      
    def CreaDocs (self, sents):
        down = float (0)   #uso float per evitare overflow
        up = float (0)
        
        PASSO = 500
        up = PASSO
        docs = list ()  #lista di documenti
        
        while up <= len (sents):
            doc = list ()
            for j in xrange(PASSO):
                doc.extend ([w.lower() for w in sents[j + down]])                
            docs.append (doc)
            down = up
            up += PASSO
        else:
            #aggiungo l'ultima frase
            doc = list ()
            for j in xrange(len (sents) - down):
                doc.extend ([w.lower() for w in sents[j + down]])              
            docs.append (doc)   
        
        return docs    


    def SelezionaStopWords (self, metodo = 1, val = 1):
        r"""
            Questo metodo calcola le stopwords
            
            sicuramente valori di log pari a 0 sono stopwords perchè presenti in
            tutti i documenti, le altre da stimare sono quelle sotto la soglia
            
        """
        def Metodo_1 (percentuale):
            """ percentuale rappresenta la porzione di testi in cui una parola
                deva comparire per essere considerata stopwords
            """
            LIMITE = log (self.D * (1 - percentuale))
            stopws = list ()
            for voc in self.idfs.keys ():
                c = self.idfs[voc]
#                print "%s : %f" % (voc, c)
                if c <= LIMITE:
                    stopws.append (voc)
        
            return stopws
        
        def Metodo_2 (nVar):
            """
                nVar rappresenta l'indice di quale limite scegliere
            """
            mean = sum([self.idfs[voc] for voc in self.idfs.keys ()]) / len(self.idfs.keys ())
            scartiQuadratici = [pow(self.idfs[voc] - mean,2) for voc in self.idfs.keys ()]
            scartoQuadraticoMedio = sqrt (sum(scartiQuadratici) / len(self.idfs.keys ()))
            
            s = mean - scartoQuadraticoMedio * int(nVar)
            stopws = [voc for voc in self.idfs.keys() if self.idfs[voc] <= s]

            return stopws
        if metodo == 1:
            return Metodo_1 (val)
        elif metodo == 2:
            return Metodo_2 (val)
        
        
###########################################################################
        
        
class ItalianStopWords (Tools):
    def __init__ (self):
        #Tools.__init__ (self, -1)
        super (ItalianStopWords, self).__init__(-1)
#OK    
    def __StopWordsFrequenza (self):
        r"""
            Questo metodo si occupa di stimare le stopwords, stimandole in 
            base alla loro frequenza assoluta rispetto al corpus analizzato
        """
        
        self.CaricaCorpus ()
        #calcolo la distribuzione di frequenza del corpus 
        freqs = nltk.FreqDist ([w.lower() for w in self.words])
        
        #candidati = [w for w in freqs.keys() if IsAlpha(w) and freqs.freq(w)>0]
        #traformo le distribuzione in tuple  - usato in fase di sviluppo del metodo
        tupleAleatorie = [tuple([k, freqs[k]]) for k in freqs.keys()]# if k in candidati]
        mean = sum([x[1] for x in tupleAleatorie]) / len(tupleAleatorie)
        
        #calcolo la dispersione dei dati intorno alla media
        #e utilizzo lo scostamento come limite per determinare i valori potenziali come stop words
        
        #calcolo sigma e var
        scartiQuadratici = [pow(x[1] - mean,2) for x in tupleAleatorie]
        #print scartiQuadratici
        
        scartoQuadraticoMedio = sqrt (sum(scartiQuadratici) / len(tupleAleatorie))    
        print "scarto quadratico medio:", scartoQuadraticoMedio
        print "media:", mean
        
        s1 = mean + scartoQuadraticoMedio * 1
        s2 = mean + scartoQuadraticoMedio * 2
        s3 = mean + scartoQuadraticoMedio * 3 
         
        
        zs1p=[x[0] for x in tupleAleatorie if x[1]>=s1 and IsAlpha(x[0])]
        zs2p=[x[0] for x in tupleAleatorie if x[1]>=s2 and IsAlpha(x[0])]
        zs3p=[x[0] for x in tupleAleatorie if x[1]>=s3 and IsAlpha(x[0])] 
         
        #salvo le abbreviazioni   
        filename = self.folderDati + "stopwordsFreq_sigma_1" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = zs1p)
        
        filename = self.folderDati + "stopwordsFreq_sigma_2" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = zs2p)
        
        filename = self.folderDati + "stopwordsFreq_sigma_3" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = zs3p)
        
        
#OK
    def __StopWordsIDF (self):
        r"""
            Questo metodo si occupa di stimare le stopwords, stimandole in
            base alla condivisione di un valore molto basso di IDF
            (inverse document frequency)
            
            utilizzeremo il corpora di paisa per questo compito e si considererà 
            ogni documento formato da X frasi. 
        """
        idf = IDF (-1)
        idf.AvviaCalcoli ()
        
        #salvo i vari file formati con metodi e parametri differenti
        stopws = idf.SelezionaStopWords (metodo = 1, val = 0.85)
        filename = self.folderDati + "stopwordsIdf_metodo_1 val_085" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = stopws)
        
        stopws = idf.SelezionaStopWords (metodo = 1, val = 0.90)
        filename = self.folderDati + "stopwordsIdf_metodo_1 val_090" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = stopws)
        
        stopws = idf.SelezionaStopWords (metodo = 1, val = 0.95)
        filename = self.folderDati + "stopwordsIdf_metodo_1 val_095" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = stopws)  
        
        stopws = idf.SelezionaStopWords (metodo = 1, val = 0.99)        
        filename = self.folderDati + "stopwordsIdf_metodo_1 val_099" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = stopws)  
        
        
        stopws = idf.SelezionaStopWords (metodo = 2, val = 1)        
        filename = self.folderDati + "stopwordsIdf_metodo_2 val_1" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = stopws) 
        
        stopws = idf.SelezionaStopWords (metodo = 2, val = 2)        
        filename = self.folderDati + "stopwordsIdf_metodo_2 val_1" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = stopws)
        
        stopws = idf.SelezionaStopWords (metodo = 2, val = 3)        
        filename = self.folderDati + "stopwordsIdf_metodo_2 val_1" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = stopws)
        
        
#OK        
    def __StopWordsDomainSpecific (self):
        r"""
            Questo metodo si occupa di stimare le stopwords in base alle
            caratteristiche morfosintattiche 
            
            Si utilizza la base di dati morphIt per estrarre i dati in 
            base alle seguenti caratteristiche:
            - Determiners
            - Coordinating conjunctions
            - Prepositions
        """
        
        #compilo i patterns re
        #Articoli
        pat_art = re.compile(r'^ART+')
        #Congiunzioni
        pat_con = re.compile(r'^CON+')
        #Preposizioni
        pat_pre = re.compile( r'^PRE+')
        
        patts = [pat_art, pat_con, pat_pre ]
        
        stopws = set ()        
        #Leggo morphIt   
        for line in self.LoadFile(self.morphItFileName):
            line = line.split ()
            if len(line) == 3:
                #verifico se la parola presa in esame appartiene al gruppo di stopwords
                for p in patts:
                    m = re.match(p, line[2])   
                    if m:
                        stopws.add (line[0])

        stopws = list (stopws)
        #salvo le abbreviazioni   
        filename = self.folderDati + "stopwordsDominSpec" + self.fileExtStopW
        self.__SaveStopWords (filename = filename, stopwords = stopws)
       
       
    def StopWords (self):
    #nb mio: queste due le ho già calcolate!
        self.__StopWordsDomainSpecific ()
        self.__StopWordsFrequenza ()
        self.__StopWordsIDF ()
        
        ConfrontaStopwords ("ItalianEsteso_Nltk", 0.55)
            
            
    def __SaveStopWords (self, filename, stopwords):
        r"""
            Questo metodo salva l'elenco su file
        """
        self.DelFile (filename)
        self.SaveByte (filename = filename, dati = stopwords)

###########################################################################

class ConfrontaStopwords (Tools):
    def __init__ (self, filenameStopwords = "ItalianStopwords", perc = 0.55):
        
        super (ConfrontaStopwords, self).__init__(1)
        #my pc
        #self.folderDati = '/home/patrizio/testerTokenizers/dati/'
        self.fileNameStopwords = self.folderDati + filenameStopwords + self.fileExtStopW
        self.perc = perc
       
        stp = self.Confronta (self.LoadStopwords (), escludiNltk = True)
        self.PrintStp (stp)
        self.SalvaFileStopwords(stp)
        
        print "\nProcesso di selezione terminato con successo"
        

    def LoadStopwords (self):
        r"""
            Questo metodo carica tutti i files ottenuti ed effettua un confronto
            tra le liste
        """
        stopwords = dict ()
        
        for file in glob.glob (self.folderDati + '*' + self.fileExtStopW):
            print "file:", file
            k = os.path.basename(file)[:-len (self.fileExtStopW)]
            stopws = self.LoadByte (file)
       
            stopwords[k] = stopws
            #old            
            #stopwords[k] = set (stopws)
        
        return stopwords


    def Confronta (self, italianStopwords = None, escludiNltk = False):
        r"""
            Questo metodo effettua una selezione tra gli elenchi delle stopwords
            precedentemente calcolati.
            Considera una parola come stopwords solo se è presente in almento una 
            percentuale PERC nei files
        """
               
        meanStopws = collections.defaultdict (int)
        
        if not escludiNltk:
            for w in nltk.corpus.stopwords.words ("italian"):
                meanStopws [w.lower()] += 1
            
        for k in italianStopwords.keys ():
            for w in italianStopwords[k]:
                meanStopws [w.lower()] += 1
        stp=[]
        #Considero stopwords solo quelle che sono presenti in almeno il x % dei casi
        mean = sum([1 for k in italianStopwords.keys () if italianStopwords[k] != list ()]) * (1 - self.perc)
   
        for w in meanStopws.keys() :
            if meanStopws[w] >= mean:
                stp.append(meanStopws[k])
        stp = [w for w in meanStopws.keys() if meanStopws[w] >= mean]

        return stp
        
        
    def PrintStp (self, stps):
        print "Le Stopwords stimate sono"       
        for i in stps:
            print i
        print "dimensione:", len(stps)
            
            
    def SalvaFileStopwords (self, dati):
        self.DelFile (self.fileNameStopwords)
        self.SaveByte (filename = self.fileNameStopwords, dati = dati)
        
        
###########################################################################

def TestIDF ():        
    a = IDF (3500)
    stopws = a.AvviaCalcoli ()
    
    print "dim stopws:", len(stopws)
    print "le stopwords sono:"
    
    for i in stopws:
        print i
        
    print "Done"
    print "il:", a.idfs['il']
    print "la:", a.idfs['la']
    print "e:", a.idfs['e']
    
    print "dim Stw:", len(stopws)
    
    mean = sum([a.idfs[voc] for voc in a.idfs.keys ()]) / len(a.idfs.keys ())
    scartiQuadratici = [pow(a.idfs[voc] - mean,2) for voc in a.idfs.keys ()]
    scartoQuadraticoMedio = sqrt (sum(scartiQuadratici) / len(a.idfs.keys ()))

    s1 = mean - scartoQuadraticoMedio * 1
    s2 = mean - scartoQuadraticoMedio * 2
    s3 = mean - scartoQuadraticoMedio * 3 
    
    zs1=[voc for voc in a.idfs.keys() if a.idfs[voc] <= s1]
    zs2=[voc for voc in a.idfs.keys() if a.idfs[voc] <= s2]
    zs3=[voc for voc in a.idfs.keys() if a.idfs[voc] <= s3]
    
    print "zs1:", len (zs1)
    print "zs2:", len (zs2)
    print "zs3:", len (zs3)
    
  
def TestStopWFr ():
    a = ItalianStopWords()
    freqs = a.StopWordsFrequenza ()
    
    def IsAlpha (string):
        #dato che lavoro con unicode non posso usare il metodo isalpha della classe str
        alls=u"qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMèéòàùì"
        for l in string:
            if not l in alls:
                return False
        return True

    #candidati = [w for w in freqs.keys() if IsAlpha(w) and freqs.freq(w)>0]
    #traformo le distribuzione in tuple  - usato in fase di sviluppo del metodo
    tupleAleatorie = [tuple([k, freqs[k]]) for k in freqs.keys()]# if k in candidati]
    mean = sum([x[1] for x in tupleAleatorie]) / len(tupleAleatorie)
    
    #print len(a.words), len(tupleAleatorie)

    #calcolo la dispersione dei dati intorno alla media
    #e utilizzo lo scostamento come limite per determinare i valori potenziali come stop words
    
    #calcolo sigma e var
    scartiQuadratici = [pow(x[1] - mean,2) for x in tupleAleatorie]
    #print scartiQuadratici
    
    scartoQuadraticoMedio = sqrt (sum(scartiQuadratici) / len(tupleAleatorie))    
    print "scarto quadratico medio:", scartoQuadraticoMedio
    print "media:", mean
    
    s1 = mean + scartoQuadraticoMedio * 1
    s2 = mean + scartoQuadraticoMedio * 2
    s3 = mean + scartoQuadraticoMedio * 3 
    
    zs1=[x[0] for x in tupleAleatorie if x[1]>=s1]
    zs2=[x[0] for x in tupleAleatorie if x[1]>=s2]
    zs3=[x[0] for x in tupleAleatorie if x[1]>=s3]  
    
    zs1p=[x[0] for x in tupleAleatorie if x[1]>=s1 and IsAlpha(x[0])]
    zs2p=[x[0] for x in tupleAleatorie if x[1]>=s2 and IsAlpha(x[0])]
    zs3p=[x[0] for x in tupleAleatorie if x[1]>=s3 and IsAlpha(x[0])] 
    
    print "zs1", len(zs1), len(zs1p)    
    print "zs2", len(zs2), len(zs2p)    
    print "zs3", len(zs3), len(zs3p)  

def AvviaCalcoli ():
    print "inizio creazione elenchi di stopwords"
    a = ItalianStopWords ()
    a.StopWords ()
    print "inizio selezione stopwords"
    cstp = ConfrontaStopwords ("ItalianEsteso_Nltk", 0.65)
     
  
def Confronto2 ():
    cstp = ConfrontaStopwords ("ItalianEsteso_Nltk", 0.65)
    
    
if __name__=='__main__':
#    AvviaCalcoli ()
#    ConfrontaStopwords ("ItalianEsteso_Nltk", 0.65)

    ItalianStopWords ().StopWords ()
    ConfrontaStopwords()