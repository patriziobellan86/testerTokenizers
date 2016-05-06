# -*- coding: utf-8 -*-


from __future__ import division
from __future__ import unicode_literals

import codecs
import glob
import nltk
import os
import pickle
import random


class InfoProgramma (object):
    def Version (self):
        return "Versione 1.1"
    def Author (self):
        return "Patrizio Bellan\n patrizio.bellan@gmail.com"

##############################################################################
##############################################################################
##############################################################################        
    
class GenericTools (InfoProgramma):
    def __init__ (self):
        super (GenericTools, self).__init__ ()        

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
            
            
        """
        try:
            os.remove(file)
        except:
            pass

    def VerificaFile (self, filename):
        try:
            with open(filename, 'r'):
                pass
            return True
        except IOError:
            return False
        
        
    def VerificaFolder (self, folder):
        return os.path.exists(folder)


##############################################################################
##############################################################################
##############################################################################


class Parametri (GenericTools):
    r""" 
        Questa classe si occupa di verificare e registrare i parametri per il programma di Test
    
    """
    
    def __init__ (self):
        super (Parametri, self).__init__ ()

        self.fileParametri = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "Parametri.pickle" #nome del file
        
        if not self.CaricaParametri ():
            self.parametri = dict ()     #variabile contentente i parametri di configurazione
            self.ImpostaParametri ()
       
       
    def ImpostaParametri (self):
        print "IMPOSTARE I PARAMETRI DEL PROGRAMMA"
        print 
        
        ###### imposto il numero di parole per il test  ######################
        print 
        tmp = 0
        while tmp == 0:
            try:
                tmp = raw_input ("Impostare il numero di WORDS su cui effettuare i test      :")
                tmp = int (tmp)                
            except ValueError:
                tmp = 0
        self.parametri['wordsTest'] = tmp
        
        ###### imposto il numero di parole di training  ######################
        print
        tmp = 0
        while tmp == 0:
            try:
                tmp = raw_input ("Impostare il numero di WORDS su cui effettuare il training :")
                tmp = int (tmp)                
            except ValueError:
                tmp = 0
        self.parametri['wordsTraining'] = tmp

        ###### imposto il percorso a paisà  ######################
        print
        tmp = ""
        while not self.VerificaFile (tmp):
            tmp = raw_input ("Impostare il percorso al file paisa'                          :")
        self.parametri['paisa'] = tmp

        ###### imposto il percorso a morphIt  ######################
        print
        tmp = ""
        while not self.VerificaFile (tmp):
            tmp = raw_input ("Impostare il percorso al file morphIt                       :")
        self.parametri['morphit'] = tmp
        
        ###### imposto il percorso a dati  ######################
        print
        tmp = ""
        while not self.VerificaFolder (tmp):
            tmp = raw_input ("Impostare il percorso alla carttella dati                   :")
        self.parametri['dati'] = tmp

        ###### imposto il percorso a testFiles  ######################
        print
        tmp = ""
        while not self.VerificaFolder (tmp):
            tmp = raw_input ("Impostare il percorso alla carttella testFiles              :")
        self.parametri['testFiles'] = tmp

        
        ###### imposto il percorso a punkt  ######################
        print
        tmp = ""
        while not self.VerificaFolder (tmp):
            tmp = raw_input ("Impostare il percorso alla carttella punkt                 :")
        self.parametri['punkt'] = tmp

        ###### imposto il percorso a corpus  ######################
        print
        tmp = ""
        while not self.VerificaFolder (tmp):
            tmp = raw_input ("Impostare il percorso alla carttella corpus                 :")
        self.parametri['corpus'] = tmp


        ###### imposto il percorso a corpus  Training######################
        print
        tmp = ""
        while not self.VerificaFolder (tmp):
            tmp = raw_input ("Impostare il percorso alla carttella corus Training         :")
        self.parametri['corpusTraining'] = tmp
        
        
        ###### imposto la soglia minima di miglioramento per il training  ######################
        print 
        tmp = 0
        while tmp == 0:
            try:
                tmp = raw_input ("Impostare la soglia (in %) di miglioramento di training :")
                tmp = int (tmp)                
            except ValueError:
                tmp = 0
        self.parametri['sogliaMiglioramento'] = tmp / 100
        
        ###### imposto il passo di training  ######################
        print 
        tmp = 0
        while tmp == 0:
            try:
                tmp = raw_input ("Impostare il passo di training                         :")
                tmp = int (tmp)                
            except ValueError:
                tmp = 0
        self.parametri['passoTraining'] = tmp
        
       ###### imposto la finestra di frasi da usare come corpusIn nel Test  ######################
        print 
        tmp = 0
        while tmp == 0:
            try:
                tmp = raw_input ("Impostare il numero di frasi della finestra CorpusIn   :")
                tmp = int (tmp)                
            except ValueError:
                tmp = 0
        self.parametri['finestraCorpusIn'] = tmp
        ############## FINE IMPOSTAZIONE PARAMETRI  #######################       
                
        #visualizzo il riepilogo dei dati inseriti
        self.RiepilogoParametri ()

        #salvo i dati  inseriti
        print
        print "Salvataggio Paramtri..."
        self.SalvaParametri ()
        
        
    def RiepilogoParametri (self):
        print
        print "Riepilogo Parametri"
        for k in self.parametri.keys ():
            print k, "->", self.parametri[k]
        print
     
     
    def SalvaParametri (self):
        if self.SaveByte (filename = self.fileParametri, dati = self.parametri):
            print "file %s salvato correttamente" % self.fileParametri
        else:
            print "impossibile salvare il file  %s" % self.fileParametri


    def CaricaParametri (self):
         self.parametri = self.LoadByte (filename = self.fileParametri)
         return self.parametri
         
    def CaricaParametro (self, parametro):
        r"""
            Questo metodo restituisce il parametro
            
            accetta in ingresso il nome del parametro
            
        """
        #return self.parametri [parametro]

        return os.path.normpath(self.parametri [parametro])
##############################################################################
##############################################################################
##############################################################################


class Tools (Parametri):
    #costanti di classe
    WORD = 1
    SENT = 2
  
    def __init__(self, n = -1, fileRisultati = "File Risultati"):
        super (Tools, self).__init__ ()
                
        self.TIPO_PARAMS = 'PARAMS'
        self.TIPO_DIMENS = 'DIMS'
        
        #per word tok
        self.SPACE='SPACE'
        self.AFTER='AFTER'
        self.BEFORE='BEFORE'
        
        self.TAGS = {'NONE' : u"", 'NEW LINE' : u"\n", 'TABS' : u"\t",
                     'PARAG' : u"\n\t", 'PARAG_2' : u'\n\n\t\t', 'SPACE' : u" "}

        self.TAGW = [self.SPACE, self.AFTER, self.BEFORE]

        self.folderCorpus = self.CaricaParametro(parametro = 'corpus') + os.path.sep
        self.folderDati = self.CaricaParametro(parametro = 'dati') + os.path.sep
        self.folderGrafici = self.folderDati + u"grafici" + os.path.sep
        self.folderPdfs = self.folderDati + u"pdfs" + os.path.sep       
        self.folderTestFiles = self.CaricaParametro(parametro = 'testFiles') + os.path.sep
        self.folderPunkt = self.CaricaParametro(parametro = 'punkt') + os.path.sep
        self.folderCorpusTraining = self.CaricaParametro(parametro = 'corpusTraining') + os.path.sep

        #ext files
        self.fileExtPnkt = u".punktTok"
        self.fileExtAbbr = '.abl'
        self.fileExtStopW = u".stopWords"

        #files
        self.stopwordsFilename = self.folderDati + u"ItalianStopwords.stopWords"
        self.morphItFileName = self.CaricaParametro(parametro = 'morphit')
        
        #self.fileRisultatiPickle = self.folderTestFiles + "results.pickle"
        self.fileNameRe = self.folderDati + u"RegularExpression.tag"
        self.loglFilename = self.folderDati + "loglikelihood.pickle"
        
        #file risultati testuale
        self.fileRisultati = self.folderTestFiles + fileRisultati + u".risultati"
        self.fileRisultatiTxt = self.folderTestFiles + fileRisultati + u".txt"

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
        
        
    def PrintOut(self, s):
        r""" questa funzione stampa a video e salva su file i dati s"""
        print s
        self.SaveFile (s, self.fileRisultatiTxt)
                              
## da non usare in questa versione lite ma da riscrivere! 
##questo metodo nella strutturazione lite non deve essere presente perchè troppo lento!
##al max usare solo per il carico dei file di training
#                
    def CaricaCorpus(self, randomCorpus = False, folder = None):
        r""" 
            Questo metodo si occupa di caricare un corpus utilizzato per i tests
            
            
        """
     
        if folder:
            self.folderCorpus = folder

        lst_pos=['ignore','words','ne','ignore','pos','srl','chunk','tree','ignore','ignore']
        #self.corpus=nltk.corpus.ConllCorpusReader(root=self.folderCorpus, fileids='.*',columntypes=lst_pos)
        if self.n == 0:
            return
        #se dim == -1 utilizzo tutti i samples
        if self.n!=-1:
            fileids = glob.glob (self.folderCorpus + '*.*')
            #fileids=self.corpus.fileids()
            if randomCorpus:
            ##random corpus        
                fileidsRandom = list ()
                for i in xrange(self.n):
                    fileidsRandom.append(fileids[random.randint(0, self.n-1)])   #aggiungo -1 per evitare di uscire dal len della lista
                fileids = fileidsRandom
            ##############             
            else:
                #controllo di non eccedere con lo slicing della list
                if self.n < len (fileids):
                    fileids = fileids[:self.n]
                    
            fileids = [os.path.basename(w) for w in fileids]  
            self.corpus = nltk.corpus.ConllCorpusReader(root = self.folderCorpus,
                                            fileids = fileids, columntypes = lst_pos)     
        else:
            self.corpus=nltk.corpus.ConllCorpusReader(root=self.folderCorpus, fileids='.*',columntypes=lst_pos)
            
            
        self.sents= self.corpus.sents()
        self.words = self.corpus.words()
        
        self.nSents=len(self.sents)
        self.nWord=len(self.words)        

     
    def CorpusObj  (self, files, paramS, paramW):
        
        return self.CreaPlainTextLite (files, paramS, paramW)
      

    def CreaPlainTextLite (self, files, tagS='NONE', tagW='SPACE'):
        r"""
        Agire su questo e lasciare intatto quello precedente
        
        
            Questo metodo si occupa di creare il corpus da utilizzare per i tests

            # option 'SPACE'|'BEFORE'|'AFTER'
            #SPACE uno spazio tra ogni parola
            #BEFORE niente spazio tra parola e segno dopo
            #AFTER niente spazio tra parola e segno, ma tra segno e parola
                   es. "wordPunct word"

        """
        
        #li registro per poterli utilizzare dopo
        
        self.tagW = tagW
        self.tagS = tagS
        self.corpusLst = list()
        
       
        lst_pos=['ignore','words','ne','ignore','pos','srl','chunk','tree','ignore','ignore']

        corpusConll = nltk.corpus.ConllCorpusReader(root = self.folderCorpus,
                                            fileids = files, columntypes = lst_pos)     
        corpus=u""                                     
        corpusLst = []
        
        for sent in corpusConll.sents():
            if tagW == self.SPACE:
                frase = u" ".join (sent) + self.TAGS[tagS]
                corpus = corpus + frase
                corpusLst.append (frase)
              
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
                corpusLst.append (frase)    
                corpus = corpus + frase
             
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
                corpusLst.append (frase)
                corpus = corpus + frase + self.TAGS[tagS]
            
                continue
            else:
                print "ATTENZIONE: parametro %s non valido" % tagW
                break
        
        dati = dict ()

        dati['txt'] = corpus
        dati['lst'] = corpusLst
        dati['words'] = list(corpusConll.words ())
        
        return dati    
        
        
      
    #RISULTATI DEI TEST 
    def RisultatiTest(self, testName, datiTest, tipo, words, sents, tag= u""):
        r"""
            Questa funzione crea una stringa di testo con il riepilogo dei dati del test
        """
        
        sents = [s.strip() for s in sents]
        datiTest = [s.strip() for s in list(datiTest)]
        
        if tipo == self.WORD:
            nInput = len(words)
            #sistemare quando sono in presenta di parole!!!
            score = self.ScoreTest (fOriginale = list(words), fTest = datiTest, tag = tag)
            
        elif tipo == self.SENT:
            nInput = len(sents)
            score = self.ScoreTest (fOriginale = sents, fTest = datiTest, tag = self.TAGS[tag])
   
        s = u"\n" + u"-" * 55 + u"\n"
        s = s + u"Test Name               : {}\n".format(testName)
        s = s + u"numero di dati in input : {}\n".format(nInput)
        s = s + u"numero di dati ottenuti : {}\n".format(len(datiTest))
        s = s + u"score                   : {}\n".format(score)
        s = s + u"error                   : {} %".format((float(1) -float(score)) * 100)
        s = s + u"\n" + u"-" * 55

#        self.SaveResCsv(testName = testName, nIn = nInput, nOut = nTest, score = score)
#        if tipo == self.WORD:
#            self.SaveResCsv(testName = testName, nIn = nInput, nOut =  len(datiTest), score = score)
#        elif tipo == self.SENT:
#            self.SaveResCsv(testName = testName, nIn = nInput, nOut =  len(datiTest), score = score)
            
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
            if indOrig >= len(fOriginale):
                break
            elif indTest >= len(fTest):
                break

            jo = 0
            jt = 0 
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


    def NumSents (self, nWord):
        r"""            
            dato un numero di parole richiesto, restituisce il numero di frasi 
            si calcolano le frasi ordinate secondo l'ordine di lettura di glob
        """
        nsent = 0
        nw = 0
        nf = 1 #num file
        
        l = glob.glob(self.folderCorpus+'*.*')
        l.sort ()
        for f in l:
            nf+=1
            nw = nw + len (self.LoadFile (f))
            nsent += 1
            print "nWord", nw, "/", nWord
            if nw >= nWord:
                return nsent
                
        print "fine files"
        return -nsent        


    def NumWords (self, nSents):
        r"""            
            dato un numero di frasi richiesto, restituisce il numero di parole 
           
        """
        nw = 0
        try:        
            files = glob.glob(self.folderCorpus+'*.*')[:nSents]
        except:
            return -1
        for file in files:
            nw = nw + len (self.LoadFile (file))
        return nw
            

if __name__ == '__main__':
    a = Parametri () 