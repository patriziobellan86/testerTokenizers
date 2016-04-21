# -*- coding: utf-8 -*-


from __future__ import division
from __future__ import unicode_literals

import codecs
import csv
import glob
import nltk
import os
import pickle
import random
import collections

class Tools (object):
    #costanti di classe
    WORD = 1
    SENT = 2
    
    def VERSION(self):
        return u"vers.0.3.7.c"
        
        
    def __init__(self, n = -1, fileRisultati = "File Risultati"):
        #parametri di classe
    
        #per word tok
        self.SPACE='SPACE'
        self.AFTER='AFTER'
        self.BEFORE='BEFORE'
       
        self.TAGS = {'NONE' : u"", 'NEW LINE' : u"\n", 'TABS' : u"\t",
                     'PARAG' : u"\n\t", 'PARAG_2' : u'\n\n\t\t', 'SPACE' : u" "}
                     
        self.TAGW = [self.SPACE, self.AFTER, self.BEFORE]

#share clic
        self.folder = os.path.sep + 'mnt' + os.path.sep + '8tera' + os.path.sep + 'shareclic' + os.path.sep + 'lucaNgrams' + os.path.sep + 'Patrizio' + os.path.sep + 'testerTokenizers' + os.path.sep
#my pc
        #self.folder = "C:\\Users\\Patrizio\\Documents\\prova testi\\tokenizer\\0.3.8.3.1\\"
                
        self.folderCorpus = self.folder + "corpus" + os.path.sep
        
        self.folderDati = self.folder + "dati" + os.path.sep
        self.folderTestFiles = self.folder + u"testFiles" + os.path.sep
        self.folderPunkt = self.folder + u"punkt" + os.path.sep
        self.fileExtPnkt = u".punktTok"
        self.folderDati = self.folder + u"dati" + os.path.sep        
        self.folderCorpusTraining = self.folder + "corpusTraining" + os.path.sep
        
        self.fileRisultati = self.folderTestFiles + "results.pickle"  #file dei risultati
        self.fileNameRe = self.folderDati + u"RegularExpression.tag"   #espressioni regolari 
        self.stopwordsFilename = self.folderDati + u"Italian Stopwords.stopWords"  #file stopwords
        self.fileExtPnkt = u".punktTok" #estensione file punkt
        self.fileExtAbbr = '.abl'   #estensione file abbreviazioni
        self.fileExtStopW = u".stopWords"  #estensione file stopwords
        self.morphItFileName = self.folderDati + "morphit.utf8.txt"
                
        self.extCorpusData = '.datacorpus'  #estensione file di corpus
        
        #riepilogo variabili di classe
        
        #nSamples
        self.n = n
        #type
        self.tagW = None
        self.tagS = None
        #text
        self.sents= None
        self.words = None
        #num 
        self.nSents = None
        self.nWord = None
        #tmp plain text
        self.corpusTxt = None
        self.corpusLst = None
        
        #nomi files
        self.fileRisultati = self.folderTestFiles + fileRisultati + u".txt"
        self.fileCsvRisultati = self.folderTestFiles + fileRisultati + u".csv"
        
        
        
    def PrintOut(self, s):
        r""" questa funzione stampa a video e salva su file i dati s"""
        print s
        self.SaveFile(s,self.fileRisultati)
       
        
#Text File
    #READ INPUT FILE        
    def LoadFile(self, fileIn):
        r"""
            Questo metodo carica un file testuale
            
            :param str fileIn: path file
            :return: il testo del file
            :rtype: uncode(str)
        """
        try:
            with codecs.open(fileIn, "r", "utf-8") as f:
                return f.readlines()
                
        except IOError:
            return False
    
    
    #SALVO I DATI IN UN FILE
    def SaveFile(self, dati, filename):
        r"""
            Questo metodo salva il file testuale
            :param list dati: dati
            :param str filename: path file
        """
	print "temporaneo", filename
        with codecs.open (filename, "a", "utf-8") as f:
            f.writelines (dati)
                       
            
#Byte File
    def SaveByte(self, dati, filename):
        r"""
            Questa funzione registra un pickle
            
            :param pckl_data dati: dati
            :param str filename: path file   
        """
        
        try:
            os.remove(filename)
        except:
            pass
        try:        
            out = open(filename,"wb")
            pickle.dump(dati, out)
            out.close()
            return True
            
        except:
            return False
            
            
    def LoadByte(self,filename):
        r"""
            Questa funzione carica un pickle
            
            :param str filename: path file   
        """
        try:
            in_s=open(filename,'rb')
            dati=pickle.load(in_s)
            in_s.close()
            
            return dati   
            
        except IOError:
            return False

                  
    def DelAllFiles(self, folder, escludeExt = False):
        r"""
            Questo metodo elimina tutti i files in una cartella
            ESCLUSI quelli con estensione "escludeExt"
            
            :param str folder: folder con i files da eliminare
            :param list escludeExt: estensione file da escludere
        """
        files=glob.glob(folder+u"*")
        for file in files:
            try:
                if escludeExt:
                    print file[file.find(os.path.extsep)+1:]
                    if file[file.find(os.path.extsep):] in escludeExt:
                        continue
                os.remove(file)
            except:
                pass
        
    
    def DelFile(self, file):
        r"""
            Questo metodo elimina un singolo file
           
           :param str filename: path file 
        """
        try:
            os.remove(file)
        except:
            pass
                
        
    def SaveTimeCsv(self, filename, testName, nSamples, execTime):
        r"""
            Questo Metodo salva i risultati del test di comparazione tempo nel file csv 
            NON USATA
            :param str filename: path file 
            :param str testName: nome test 
            :param str nSamples: path file 
            :param str execTime: path file 
        """
        
        with open(filename, 'ab') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow( (testName, nSamples, execTime) )
            
           
    def SaveResCsv(self, testName, nIn, nOut, score):
        r"""
            Questo Metodo salva i risultati del test nel file csv 
            
            :param str testName: nome test 
            :param str nIn: n dati in ingresso 
            :param str nOut: n dati in uscita  
            :param str score: score test 
        """
        
        with open(self.fileCsvRisultati, 'ab') as csvfile:
            writer = csv.writer (csvfile)
            writer.writerow( (testName, nIn, nOut, score) )
        

    def SaveTestCsv(self, filename, testName, nSamples, result):
        r"""
            Questo Metodo salva i risultati del test in un file csv 
            
            :param str filename: path file
            :param str testName: nome test 
            :param str nSamples: n dati in ingresso  
            :param str result: score test 
        """
        
        with open(filename, 'ab') as csvfile:
            writer = csv.writer (csvfile)
            writer.writerow( (testName, nSamples, result) )
            
            
    def LoadResCsv(self, filenameCsv):
        r"""
            Questa funzione carica i dati dal file csv
            
            :param str filenameCsv: path file
        """
        
        with open(filenameCsv, 'rb') as csvfile:
            return [line for line in csv.reader(csvfile)]
            
            
    def CaricaCorpus(self, randomCorpus = False, folder = None):
        r""" 
            Questo metodo si occupa di caricare un corpus utilizzato per i tests
            
            :param bool randomCorpus: attiva il random corpus
            :param str folder: cartella da cui prelevare i files
        """
     
        if folder:
            self.folderCorpus = self.folder + folder + os.path.sep
       
#        print "folder corpus:", self.folderCorpus
#        print "len glob corpus:", len(glob.glob (self.folderCorpus+'*'))      

        lst_pos=['ignore','words','ne','ignore','pos','srl','chunk','tree','ignore','ignore']
        
        if self.n == 0:
            return
        #se dim == -1 utilizzo tutti i samples
        if self.n!=-1:
            fileids = glob.glob (self.folderCorpus + '*.*')
            #fileids=self.corpus.fileids()
            if randomCorpus:
                #########   random corpus    #############    
                fileidsRandom = list ()
                for i in xrange(self.n):
                    fileidsRandom.append(fileids[random.randint(0, self.n-1)])   #aggiungo -1 per evitare di uscire dal len della lista
                fileids = fileidsRandom
                ############################################             
            else:
                #controllo di non eccedere con lo slicing della list
                if self.n < len (fileids):
                    fileids = fileids[:self.n]
                    
            fileids = [os.path.basename(w) for w in fileids]  
            self.corpus = nltk.corpus.ConllCorpusReader(root = self.folderCorpus,
                                        fileids = fileids, columntypes = lst_pos)     
        else:
            self.corpus=nltk.corpus.ConllCorpusReader(root=self.folderCorpus, 
                                        fileids = '.*', columntypes = lst_pos)
            
        self.sents= self.corpus.sents()
        self.words = self.corpus.words()
        
        self.nSents=len(self.sents)
        self.nWord=len(self.words)        
        
#        #ricerca bug
#        print "N sent caricati", self.nSents
#        print "ids", len(fileids)
#        print "corS", len(self.corpus.sents())
#        print "n", self.n

#VERIFICARE UTILITA' FUNZIONE    
    def CreaPlainTextFromRandomCorpus (self): #(self, tagW='SPACE', tagS='NONE'):
        r""" 
            Questo metodo si occupa di caricare un corpus utilizzato per i tests
            creando il corpus in modo random
            
        """
        self.CaricaCorpus (randomCorpus = True)
                 
    #new method    
    def CreaPlainText2 (self, tagS='NONE', tagW='SPACE', dim = -1):
        r"""
        Agire su questo e lasciare intatto quello precedente
        
        
            Questo metodo si occupa di creare il corpus da utilizzare per i tests

            # option 'SPACE'|'BEFORE'|'AFTER'
            #SPACE uno spazio tra ogni parola
            #BEFORE niente spazio tra parola e segno dopo
            #AFTER niente spazio tra parola e segno, ma tra segno e parola
                   es. "wordPunct word"

            :param str tagS: tipo di separatore di frasi
            :param str tagW: tipo di separatore delle parole
            :param str dim: dimensione corpus da creare
        """
        
        #carico il corpus
        self.n = dim
        self.CaricaCorpus ()
        #aggiorno i dati interni
        self.tagW = tagW
        self.tagS = tagS
        
        self.corpusLst = list()
        
        corpus=u""
        
        #dati per contatore frasi        
        nsents = len (self.sents)
        i = 0   #contatore frasi
        
        for sent in self.sents:
            print "elaborazione frase %d / %d"% (i, nsents)
            i += 1
            
            if tagW == self.SPACE:
                frase = u" ".join (sent) + self.TAGS[tagS]
                corpus = corpus + frase
                self.corpusLst.append (frase)
              
                continue
            ############################ ok
            elif tagW == self.AFTER:
                frase = u""
                for i in xrange (len(sent)):     
                    if (i+1) < len (sent):
                        if not sent[i+1].isalpha () and len (sent[i+1]) == 1:
                             frase = frase + sent[i]
                        else:
                             frase = frase + sent[i] + u" "
                    else:
                         frase = frase + sent[i] + u" "
                frase = frase + self.TAGS[tagS]
                self.corpusLst.append(frase)    
                corpus=corpus+frase
             
                continue
            ####################### ok
            elif tagW == self.BEFORE:
                frase = u""
                for i in xrange(len(sent)):     
                    if (i+1) < len (sent):
                        if not sent[i].isalpha () and len (sent[i]) == 1:
                             frase = frase + sent[i]
                        else:
                             frase = frase + sent[i] + u" "
                    else:
                         frase = frase + sent[i] + u" "
                frase = frase + self.TAGS[tagS]  
                self.corpusLst.append (frase)
                corpus=corpus+frase+self.TAGS[tagS]
            
                continue
            else:
                print "ATTENZIONE: parametro %s non valido" % tagW
                break
        self.corpusTxt = corpus

        #memorizzo i dati in un dict (list) e salvo il pickle
        dim = len(self.sents)
        filename = str(dim) + tagS + tagW
        filename = self.folderTestFiles + filename + self.extCorpusData        

        dati = dict ()

        dati['lst'] = self.corpusLst
        dati['words'] = list(self.words)

        self.SaveByte(dati, filename)
        
        return self.corpusTxt         
      
      
    #RISULTATI DEI TEST 
    def RisultatiTest(self, testName, datiTest, tipo, words, sents, tag= u""):
        r"""
            Questa funzione crea una stringa di testo con il riepilogo dei dati del test
            
            :param str testName: nome test
            :param var datiTest: dati del test
            :param int tipo: tipo di test
            :param list words: lista parole
            :param list sents: lista frasi
            :param str tag: tag parametro di separazione frasi
            
            :return: la stringa dei risultati e il valore dello score del test
            :rtype: str
            :rtype: float
            
        """
        
        #ripulisco i dati
        sents = [s.strip() for s in sents]
        datiTest = [s.strip() for s in list(datiTest)]
        
        #calcolo lo score in base al tipo di test effettuato
        if tipo == self.WORD:
            nInput = len(words)
            #sistemare quando sono in presenta di parole!!!
            score = self.ScoreTest (fOriginale = list(words), fTest = datiTest, tag = tag)
            
        elif tipo == self.SENT:
            nInput = len(sents)
            score = self.ScoreTest (fOriginale = sents, fTest = datiTest, tag = self.TAGS[tag])
   
       #stringa per stampa a video dei risultati
        s = u"\n" + u"-" * 55 + u"\n"
        s = s + u"Test Name               : {}\n".format(testName)
        s = s + u"numero di dati in input : {}\n".format(nInput)
        s = s + u"numero di dati ottenuti : {}\n".format(len(datiTest))
        s = s + u"score                   : {}\n".format(score)
        s = s + u"error                   : {} %".format((float(1) -float(score)) * 100)
        s = s + u"\n" + u"-" * 55

        return s , score
        
        
    def ScoreTest (self, fOriginale, fTest, tag):
        r""" Questa funzione calcola lo score di un test 
             Ripestto alla funzione utilizzata in Tools, questa verifica la bontà esatta del test
             tenendo conto di eventuali errori non scopribili semplicemente dal rapporto
                                                                float(ottenuti / giusti)
               :param list fOriginale: lista dati di partenza 
               :param list fTest: lista risultante dall'applocazione del tokenizer a dati di partenze
               :return: lo score effettivo del test
               :rtype: float
        
        """
        ERROR = 0
        NO_ERROR = 1 
        
        score = list()     
        assert type(fOriginale) == type(fTest) and type(fOriginale) == type(list())
       
        i = 0   #indice di ciclo
        indOrig = 0  #indice a File Originale
        indTest = 0  #indice a file di Test

        
        while i < len (fOriginale):
            #controllo di non uscire dalle dimensioni delle liste
            if indOrig >= len(fOriginale):
                break
            elif indTest >= len(fTest):
                break

            #azzero gli indici di spostamento
            jo = 0
            jt = 0 
            
            #effettuo il confronto
            if fOriginale[indOrig] == fTest[indTest]:
                score.append(NO_ERROR)
            elif fOriginale[indOrig].startswith(fTest[indTest]):                  
                #attivo lo sfasamento jt
                tmpTest = fTest[indTest]
                jt = 1   #variabile temporanea di sfasamento nella lista fTest
                
                while True:
                    #controllo fine lista           
                    if (indTest + jt) >= len(fTest):
                        break
                    #######new aggiunto: + tag +
                    tmpTest = tmpTest + tag + fTest[indTest + jt]
                    if fOriginale[indOrig] == tmpTest:
                        #aggingo l'error allo score
                        #aggiungo tanti error quanti sono gli j 
                        #ed esco dal ciclo più interno
                        score.extend([ERROR] * jt) 
                        break
                    elif fOriginale[indOrig].startswith(tmpTest):
                            jt += 1
                    else:
                        #se sono qui, la precedente di jt era contenuta
                        #quindi decremento di uno jt e registro l'errore
                        #ed esco dal ciclo
                        jt -= 1
                        score.extend([ERROR] * jt)
                        break
            elif fTest[indTest].startswith(fOriginale[indOrig]):
                #fTest potrebbe aver incluso due parole di fOrig
                #Controllo che anche la successiva si la continuazione 
                #in fTest
                #Metto il tutto in un ciclo
                #attivo lo sfasamento jo
                jo = 1    
                tmpOrig = fOriginale[indOrig]
                
                while True:
                    if (indOrig + jo) >= len (fOriginale):
                        break
                    #######new aggiunto: + tag +
                    tmpOrig = tmpOrig + tag + fOriginale[indOrig + jo]
                    
                    if fTest[indTest]  == tmpOrig:
                        #se sono arrivato a far combaciare origine e test
                        #registro gli errori 
                        score.extend([ERROR] * jo) 
                        break
                    elif fTest[indTest].startswith(tmpOrig):
                        jo += 1
                    else:
                        #se sono qui, la precedente di jo era contenuta
                        #quindi decremento di uno jo e registro l'errore
                        #ed esco dal ciclo
                        jo -= 1
                        score.extend([ERROR] * jo)
                        
                        #se jo è zero un errore lo devo segnare 
                        if jo < 1 :
                            score.extend([ERROR])
                            
                        break
            else:
                #il successivo di orig non è contenuta in test quindi
                #registro l'errore e continuo
                score.append(ERROR)
                    
            indTest += jt + 1              
            indOrig += jo + 1  
            i += 1
        
        if indOrig > indTest:
            #arrivato alla fine del ciclo, se indOrig è maggiore di indTest
            #aggiungo tanti errori quanti sono la loro differenze
            score.extend([ERROR] * (indOrig - indTest))        
        elif indOrig < indTest:
            #arrivato alla fine del ciclo, se indTest è maggiore di indOrig
            #aggiungo tanti errori quanti sono la loro differenze
            score.extend([ERROR] * (indTest - indOrig))
        
        try:
            return float(sum(score) / len(score))
        except ZeroDivisionError:
            return float(0)
        
        
class CorpusObj (Tools):
    def __init__ (self, dim, tagS, tagW):
        r"""
            Questa classe carica il pickle del corpus originale
            
            i dati sono serializzati da un dict(list)
            le cui chiavi sono:
                words -> tutte le parole memorizzate
                lst   -> frasi in list
                
        
        """        
        #Tools.__init__ (self, 0)
        super (CorpusObj, self).__init__ (0)
        
        filename = str(dim) + tagS + tagW
        filename = self.folderTestFiles + filename + self.extCorpusData 
        #my pc
        #filename = 'C:\\Users\\Patrizio\\Documents\\prova testi\\tokenizer\\0.3.8.3.1\\testFiles' + os.path.sep  +str(dim) + tagS + tagW+ self.extCorpusData 
        print "caricamento corpus %s in corso..." %  filename
        self.dati = self.LoadByte (filename)
        print "corpus caricato"
        
    def Txt (self):
        r"""
            Txt -> restituisce il testo in forma piana
            
            :return: il testo
            :rtype: str
        """
        return "".join (self.dati['lst'])
        
    def Lst (self):
        r"""
            Lst -> restituisce il testo in lista
            
            :return: il testo
            :rtype: list
        """
        return self.dati['lst']
        
    def Words (self):
        r"""
            Words -> restituisce le parole
            
            :return: le parole
            :rtype: list
        """
        return self.dati['words']
        
if __name__=='__main__':
    print "No Test Mode!"
    
    a=CorpusObj (54, 'TABS', 'SPACE')           
    print a.Lst()[0]