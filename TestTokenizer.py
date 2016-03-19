# -*- coding: utf-8 -*-
"""

@author: Patrizio

                        
"""


from __future__ import division, unicode_literals

from Tools import Tools
from TestTextTiling import TextTiling
from CreatorePunktTokenize import MyPunktTokenize


import nltk
import re


import collections


class TestTokenizer():
    r""" 
        Questa classe si occupa di lanciare in eseguzione tutti i tests sui tokenizers presenti in nlkt
    """
    def VERSION(self):
        return u"vers.0.3.8.a"
      
      
    def __init__(self, fileRisultati = "Risultati", save = False, dimTests = [0], aggiornaDatiTest = False):
        self.dimTests = dimTests

        self.save = save
          
#sistemare valore - per ora è solo di test
        self.sogliaPrestazioniMedie = 0.005
        self.TIPO_PARAMS = 'PARAMS'
        self.TIPO_DIMENS = 'DIMS'
#######mettere valori giusti        
        self.dimsTrainTok = [5000, 10000]   # dimensioni di training dei tokenizzatore, espressa in num di sents!
        
        self.folderTestFiles = u"test files\\"
        self.folderPunkt = u"punkt\\"
        self.folderDati = u"dati\\"
        self.fileRisultati = self.folderTestFiles + "results.pickle"
        self.fileNameRe = self.folderDati+u"RegularExpression.tag"
        self.stopwordsFilename = self.folderDati + u"Italian Stopwords.stopWords"
        self.fileExtPnkt = u".punktTok"
        
        self.tools=Tools(n = 0, fileRisultati = (self.folderTestFiles+fileRisultati))
        
        self.paramCorpusCreationW = self.tools.TAGW
        self.paramCorpusCreationS = self.tools.TAGS.keys()
        #Condizione Semplice
        self.simpleParamS = 'PARAG_2'
        self.simpleParamW = 'SPACE'
        #Condizione Normale
        self.normalParamS = 'SPACE'
        self.normalParamW = 'SPACE'
        #Stopwords 
        self.stopwords = self.tools.LoadByte (self.stopwordsFilename)
        #patterns per Re
        self.patterns = self.tools.LoadByte (self.fileNameRe)

        if aggiornaDatiTest:
            self.risultatiTest = self.tools.LoadByte (self.fileRisultati)
        else:
            self.risultatiTest = collections.defaultdict(list)
        
        self.AvviaTests ()
        

    ########################################################################
        
    def AvviaTests (self):
        r"""
            Questo metodo si occupa di mandare in eseguzione tutti i tests
        """
        
        s = u"\n Avvio dei Tests"
        s = s + u"\n Avvio dei tests sui Words Tokenizers\n"
        self.tools.PrintOut (s)
        self.AvviaTestWordsTokenizers ()
      
        s = u"\n Avvio dei tests sui Sents Tokenizers\n"
        self.tools.PrintOut (s)
        self.AvviaTestSentsTokenizers ()
      
        #Salvo il file dei risultati
        self.tools.SaveByte (self.risultatiTest, self.fileRisultati)
        print "FINE TEST"
        
        
    ########################################################################
        
    #TESTS SUI WORDS TOKENIZERS
    def AvviaTestWordsTokenizers (self):
        r"""
            Questo metodo testa tutti i tokenizzatori di parole        
        """     
        #nltk.tokenize.simple
        self.TestSimpleSpaceTokenizerWord ()
        
        self.TestSimpleWordTokenizer ()
        self.TestSimpleWordTokenizerIta ()
        self.TestTreeBankTokenizer ()
        
        if self.patterns:
            self.AvviaTestREWordTok (tipo = self.tools.WORD)


    ########################################################################

    def AvviaTestSentsTokenizers (self):
        r"""
            Questo metodo testa tutti i tokenizzatori di frasi        
        """       
        print "jump to MyPunkt tokenizers"
        #nltk.tokenize.simple
        self.TestSimpleLineTokenizerWord ()
        
        self.TestSimpleTokenizer ()
        self.TestSimpleTokenizerIta ()

        if self.patterns:
            self.AvviaTestREWordTok (tipo = self.tools.SENT)

        self.AvviaTestTextTilingTokenizer ()
     
        self.TestMyPunkt ()

    ########################################################################
        
    #SIMPLE SPACE TOKENIZER
    def TestSimpleSpaceTokenizerWord (self): 
        r""" 
            questo metodo effettua il test sullo simple space word tokenize
        """
        #per prima cosa avvio il test nella condizione più semplice
        
        #creo il corpus da utilizzare per i tests

        testName = u"SIMPLE SPACE WORD TOKENIZER"
        s = u"\nTEST : {}".format (testName) 
        
        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut = nltk.tokenize.simple.SpaceTokenizer().tokenize(corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW))
        
        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
        self.tools.PrintOut (s + r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut = nltk.tokenize.simple.SpaceTokenizer().tokenize (corpusObj.CreaPlainText (paramS, paramW))
                    r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut = nltk.tokenize.simple.SpaceTokenizer().tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW))
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)
                  
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
                  
                  
    #SIMPLE WORD TOKENIZER
    def TestSimpleWordTokenizer (self):
        r""" 
            questo metodo effettua il test sullo standard word tokenizer
        """        
        #per prima cosa avvio il test nella condizione più semplice
        #creo il corpus da utilizzare per i tests

        testName = u"STANDARD WORD TOKENIZER"
        s = u"\nTEST : {}".format (testName) 
        
        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut = nltk.tokenize.word_tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW))
        
        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
        self.tools.PrintOut (s + r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut = nltk.tokenize.word_tokenize (corpusObj.CreaPlainText (paramS, paramW))
                    r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut = nltk.tokenize.word_tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW))
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)        
                  
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
              
              
    #SIMPLE WORD TOKENIZER ITA
    def TestSimpleWordTokenizerIta (self):
        r""" 
            questo metodo effettua il test sullo standard word tokenizer ita
        """

        testName = u"STANDARD WORD TOKENIZER ITA"
        s = u"\nTEST : {}".format (testName) 
        
        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut = nltk.tokenize.word_tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW), language='italian') 
        
        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
        self.tools.PrintOut (s + r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut = nltk.tokenize.word_tokenize (corpusObj.CreaPlainText (paramS, paramW), language='italian') 
                    r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut = nltk.tokenize.word_tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW), language='italian') 
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)   
                  
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################


    #TREEBANK TOKENIZER
    def TestTreeBankTokenizer (self):
        r""" 
            questo metodo effettua il test sul treebank tokenizer
        """
        
        testName = u"TREEBANK TOKENIZER"
        s = u"\nTEST : {}".format (testName) 
        
        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut = nltk.tokenize.TreebankWordTokenizer().tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW)) 
        
        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
        self.tools.PrintOut (s + r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut = nltk.tokenize.TreebankWordTokenizer().tokenize (corpusObj.CreaPlainText (paramS, paramW)) 
                    r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut = nltk.tokenize.TreebankWordTokenizer().tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW)) 
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.WORD, corpusObj.words, corpusObj.corpusLst)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)        
        
                  
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
 
  
##########################  SENTENCE TOKENIZERS  ##############################   

    #SIMPLE LINE TOKENIZER
    def TestSimpleLineTokenizerWord (self):
        r""" 
            questo metodo effettua il test sullo simple line tokenize
        """

        testName = u"SIMPLE LINE SENT TOKENIZER"
        s = u"\nTEST : {}".format (testName) 
        
        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut =  nltk.tokenize.simple.LineTokenizer().tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW)) 
#######here new param corpusLst
        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag = self.simpleParamS)
        self.tools.PrintOut (s + r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut =  nltk.tokenize.simple.LineTokenizer().tokenize (corpusObj.CreaPlainText (paramS, paramW)) 
                    r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag =paramS)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut =  nltk.tokenize.simple.LineTokenizer().tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW)) 
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag = self.normalParamS)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)        
        
                  
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
                          


    #SIMPLE TAB TOKENIZER
    def TestSimpleTabTokenizerWord (self):
        r""" 
            questo metodo effettua il test sullo simple tab tokenize
        """
        
        testName = u"SIMPLE TAB SENT TOKENIZER"
        s = u"\nTEST : {}".format (testName) 
        
        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut =  nltk.tokenize.simple.TabTokenizer().tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW)) 
        
        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag = self.simpleParamS)
        self.tools.PrintOut (s + r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut =  nltk.tokenize.simple.TabTokenizer().tokenize (corpusObj.CreaPlainText (paramS, paramW)) 
                    r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag = paramS)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut =  nltk.tokenize.simple.TabTokenizer().tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW)) 
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag= self.normalParamS)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)      
            
            
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
                          

    #SIMPLE TOKENIZER
    def TestSimpleTokenizer (self):
        r""" 
            questo metodo effettua il test sullo standard sent tokenizer
        """
#        datiOut = nltk.tokenize.sent_tokenize(corpus) 
        
        testName =  u"SIMPLE SENT TOKENIZER"
        s = u"\nTEST : {}".format (testName) 
        
        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut =  nltk.tokenize.sent_tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW)) 
        
        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag= self.simpleParamS)
        self.tools.PrintOut (s + r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut =  nltk.tokenize.sent_tokenize (corpusObj.CreaPlainText (paramS, paramW)) 
                    r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag=paramS)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut =  nltk.tokenize.sent_tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW)) 
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag= self.normalParamS)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)           

                  
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
  
  
    #SIMPLE TOKENIZER ITA
    def TestSimpleTokenizerIta (self):
        r""" 
            questo metodo effettua il test sul simple sent tokenizer ita
        """
        testName = u"SIMPLE SENT TOKENIZER ITA"
        s = u"\nTEST : {}".format (testName) 
        
        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut =  nltk.tokenize.sent_tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW), language='italian')
        
        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag= self.simpleParamS)
        self.tools.PrintOut (s + r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut =  nltk.tokenize.sent_tokenize (corpusObj.CreaPlainText (paramS, paramW), language='italian') 
                    r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag= paramS)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut =  nltk.tokenize.sent_tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW), language='italian') 
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag= self.normalParamS)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)           
        
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
        
        
        
    ########################################################################
    #######################    RE TOK   ####################################
    ########################################################################
    def AvviaTestREWordTok(self, tipo):
        r"""
            self.patterns
            dict([tuple(patternName, tipo)]= pattern)
        """        

        s=u"\n\nINIZIO SESSIONE  Regular Expression Tokenizers"
        self.tools.PrintOut(s)
                
#New Vesion
    
        #per prima cosa effettuo un test del pattern in parametrizzazione standard,
        #per poter proseguire deve necessariamente passare l'euristica NoZero
        for pattern in self.patterns.keys():
            if tipo == pattern[1]:
                # se supero il test di allNoZero proseguo con gli altri test
                if self.TestREWordTok_patter_w_gaps_F_discard_empty_T_flags_reUNI (
                    pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo):
                    
                    self.TestREWordTok_patter_w_gaps_F_discardEmpty_T_flags_reMULTI (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)
                    self.TestREWordTok_patter_w_gaps_F_discardEmpty_T_flags_reDOTALL (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)            
                    
                    self.TestREWordTok_patter_w_gaps_F_discard_empty_F_flags_reUNI(
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)
                    self.TestREWordTok_patter_w_gaps_F_discardEmpty_F_flags_reMULTI (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)
                    self.TestREWordTok_patter_w_gaps_F_discardEmpty_F_flags_reDOTALL (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)

                    self.TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reUNI (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)
                    self.TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reMULTI (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)
                    self.TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reDOTALL (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)
                        
                    self.TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reUNI (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)
                    self.TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reMULTI (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)
                    self.TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reDOTALL (
                        pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)
                        
                        
#################################################################################
################## REGULAR EXPRESSION TOKENIZERS ################################        
################################################################################# 

###########################################################################
###############   GENERAL RE TOKENIZER ####################################
###########################################################################

    def TestREWordTok_General (self, tok, testName, pattern, patternName, tipo):   
        r""" 
            General Regular Expression Tokenizer
            
            
            questo metodo modella un generico RE tokenizer
            
            :param obj tok: l'oggetto tokenizzatore modellato
            :param str testName: il nome del test
            
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        s = u"\nTEST : {}".format (testName)   
        
        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut =  tok.tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW))
        if tipo == self.tools.SENT:
            r, score = self.tools.RisultatiTest(testName, datiOut, tipo, corpusObj.words, corpusObj.corpusLst, tag =self.simpleParamS)
        else:
            r, score = self.tools.RisultatiTest(testName, datiOut, tipo, corpusObj.words, corpusObj.corpusLst)    
        self.tools.PrintOut (s + r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut =  tok.tokenize (corpusObj.CreaPlainText (paramS, paramW)) 
                    r, score = self.tools.RisultatiTest(testName, datiOut, tipo, corpusObj.words, corpusObj.corpusLst)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return False
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut =  tok.tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW)) 
                r, score = self.tools.RisultatiTest(testName, datiOut, tipo, corpusObj.words, corpusObj.corpusLst)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)  
            
            return False
            
        return True      
        
    ############################################################################        
               
               
    def TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reUNI (self, 
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        #def TestREWordTok_General (self, tok, testName, pattern, patternName, tipo): 
        
        testName = unicode(patternName) + u" gap=True discardEmpty=True flags=re.UNI"
        tok = nltk.tokenize.RegexpTokenizer(pattern, gaps=True, discard_empty=True, flags=re.UNICODE)
        
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)       
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
      
        testName = unicode(patternName) + u" gap=True discardEmpty=True flags=re.MULTI"
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=True, flags=re.MULTILINE)
        
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
    #################################################################################


    def TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
      
        testName = unicode(patternName) + u" gap=True discardEmpty=True flags=re.DOTALL"
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=True, flags=re.DOTALL)
       
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
        
    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discard_empty_T_flags_reUNI (self,
                                                pattern, patternName, tipo):   
        r""" 
            Standard Regular Expression Tokenizer
           
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        #Creo l'oggetto 
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=True, flags=re.UNICODE)
        testName = unicode(patternName) + u" gap=False discard_empty=True flags=re.UNI"
        
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
        
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_F_discardEmpty_T_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
      
        testName = unicode(patternName) + u" gap=False discardEmpty=True flags=re.MULTI"
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=True, flags=re.MULTILINE)
        
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discardEmpty_T_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
      
        testName = unicode(patternName) + u" gap=False discardEmpty=True flags=re.DOTALL"
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=True, flags=re.DOTALL)
       
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
                
    ##################################################################################
                

    def TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reUNI (self, 
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        #def TestREWordTok_General (self, tok, testName, pattern, patternName, tipo): 
        
        testName = unicode(patternName) + u" gap=True discardEmpty=False flags=re.UNI"
        tok = nltk.tokenize.RegexpTokenizer(pattern, gaps=True, discard_empty=False, flags=re.UNICODE)
        
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)       
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
      
        testName = unicode(patternName) + u" gap=True discardEmpty=False flags=re.MULTI"
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=False, flags=re.MULTILINE)
        
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
    #################################################################################


    def TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
      
        testName = unicode(patternName) + u" gap=True discardEmpty=False flags=re.DOTALL"
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=False, flags=re.DOTALL)
       
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
        
    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discard_empty_F_flags_reUNI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        #Creo l'oggetto 
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=False, flags=re.UNICODE)
        testName = unicode(patternName) + u" gap=False discard_empty=False flags=re.UNI"
        
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
        
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_F_discardEmpty_F_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
      
        testName = unicode(patternName) + u" gap=False discardEmpty=False flags=re.MULTI"
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=False, flags=re.MULTILINE)
        
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discardEmpty_F_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
      
        testName = unicode(patternName) + u" gap=False discardEmpty=False flags=re.DOTALL"
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=False, flags=re.DOTALL)
       
        return self.TestREWordTok_General (tok, testName, pattern, patternName, tipo)
                
    ##################################################################################   
    
############### MY PUNKT TOKENIZERS   #######################################
  



                
######################################################################
######################################################################
##################### SISTEMARE QUESTO  ##############################
######################################################################
######################################################################
   
    
    def TestMyPunkt (self):
        r""" 
            questo metodo effettua i tests sui Punkt Tokenizers
        """
        print 
        print
        print "ricordati che devi impostare il testName"
        print
        print 
        print 
        print 
        
        def CreaTokenizzatore (dimTraining, params):            
            obj = Tools (dimTraining)
            obj.CaricaCorpus ()

            return MyPunktTokenize().CreaMyPunkt (obj.CreaPlainText (self.simpleParamS, self.simpleParamW), *params)            

            #######################################            

        def TestTagsTok (testName, dim, tok, registra = False, paramTest = None):
            """ 
                Questo metodo deve restituire solo True o False
                o list(tuple(paramTest, score))
                
                paramTest rappresenta il parametro che sto testando
            """
            tupleScores = list ()
            
            ###METTERE TESTNAME ##########à        
            #testName = "DEFAULT PUNKT TOKENIZER"
            s = u"\nTEST : {}".format (testName)   
            
            #Oggetto per il corpus
###new            
            corpusObj = Tools (dim) #self.dimTests[0])
            corpusObj.CaricaCorpus ()
                
            datiOut =  tok.tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW))
#############################modificato qui per controllo ricostruzione testo!!!!            
            r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag = self.simpleParamS)
            self.tools.PrintOut (s + r)
#new            
            if self.save and registra:
                #Salvo il file elaborato dal tokenizzatore
                filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + self.simpleParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                self.tools.SaveFile (filename = filename, dati = datiOut)
                
            if self.EuristicaNoZero (score):
                #proseguo con gli altri 
                print "EuristicaNoZero Superata"
    
                #calcolo gli altri score dei tests e poi applico l'euristica successiva
                            
                scores = list ()
                
                for paramS in self.paramCorpusCreationS:
                    for paramW in self.paramCorpusCreationW:            
                        print "TMP: TAGS %s TAGW %s"%(paramS, paramW)
                        s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                        self.tools.PrintOut (s)
                        
                        datiOut =  tok.tokenize (corpusObj.CreaPlainText (paramS, paramW)) 
#########################################here                        
                        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag = paramS)
                        self.tools.PrintOut (r) 
                        
                        tupleScores.append (tuple([paramTest, score]))
                        
                        if self.save:
                            #Salvo il file elaborato dal tokenizzatore
                            filename = self.folderTestFiles + u" " + paramS + u" "  + paramW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                            self.tools.SaveFile (filename = filename, dati = datiOut) 
                            
                        if self.EuristicaNoZero (score):                
                            #registro i risultati
                            tupleScores.append (tuple([paramTest, score]))
                            scores.append (score)
###new                      
                            if registra:
                                test = {'paramS':paramS, 'paramW':paramW, 'dim':dim, 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                                self.risultatiTest[testName].append(test)
                        
                        else:
                            print "Euristica NoZero Non superata, fine test"
    #                        print "registro il fallimento del test ed esco dal metodo"
###new
                            if registra:
                                test = {'paramS':paramS, 'paramW':paramW, 'dim':dim, 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                                self.risultatiTest[testName].append(test)
#####new                                
                            if paramTest == None:
                                return False
                            else:
                                return tupleScores
            else:
                print "Euristica No Zero non superata"
                if registra:
                    test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':dim, 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                    self.risultatiTest[testName].append(test)  
            
            return tupleScores
            #########################################    
                 
        def TestDimsTok (testName, dims, tok, registra = False, paramTest = None):
            r"""
                 Questa funzione deve restituire una
                 list(tuple(paramTest, score))
                 da passare poi alla funzione best
            """
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
            tupleScores = list ()
            
            for dim in dims: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut =  tok.tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW)) 
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag = self.normalParamS)
                self.tools.PrintOut (r)  
                
                if self.save and registra:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
#new                
                if registra:  
                    test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                    self.risultatiTest[testName].append(test)
                if paramTest == None:
                    paramTest = dim
                tupleScores.append (tuple([paramTest, score]))                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
#new
                if registra:
                    test = {'euristicaPrestazioniMedie':True}
                    self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
#new
                if registra:
                    test = {'euristicaPrestazioniMedie':False}
                    self.risultatiTest[testName].append(test)
            
            return tupleScores
            ###################################
            
        def Best (tuplaScores):
            """
               Questa funzione restituisce il primo parametro della tupla migliore
            """
               
            best = (0, 0)
            for i in tuplaScores:
                if best[1] < i[1]:
                       best = i
            return best[0]
           #####################################
                
        # questi due arrays vengono passati direttamente dall'oggetto creatore MyPunktTokenize
        parametri = MyPunktTokenize().GetAllParams ()  # contiene tutte le varianti dei parametri
        params = MyPunktTokenize().GetStandardParams ()  #all'avvio del metodo continene i parametri standard
           
        ########PARTE STANDARD DEL TESTS  #################
        
        print "test preliminare del tokenizzatore standard"
        print "parametri: ", params

        #creo il tokenizzatore
        print "definire dimPreliminare, ora a 5000"
        dimPreliminare = 5000  #dim training tokenizzatore
        tok = CreaTokenizzatore (dimPreliminare, params)        
        print "\n"*15
        #questa prima fase del test è per testare l'euristica NoZero
        #e quindi prosecuire con i tests

        #decidere se passarer n words  o n sents!!!!
        testName = "Default Punkt Tokenizer"

        #TEST PRELIMINARE
        if not TestTagsTok (testName, self.dimTests[0], tok):
            print "Test Preliminare non passato"
              
        #provo le varie dimensioni di addestramento in rapporto con la dimensione
        # media delle dimensioni dei test
            
        meanDimTests = int (sum(self.dimTests) / len (self.dimTests))

        bestDim = Best (TestDimsTok (testName, self.dimsTrainTok, tok))
        #ora ho la dimensione best per creare il tokenizzatore. inizio con i test!
        
        
        
        ########## inizio i test standard veri e propri registrandoli nella variabile dei risultati

        
        #creo il tokenizzatore
        tok = CreaTokenizzatore (bestDim, params)       
        #test Params
        TestTagsTok (testName, meanDimTests , tok, False)
        #test Dims
        TestDimsTok (testName, self.dimTests, tok, False)
        #### FINE TEST CON PARAMETRI DI DEFAULT ###


        ############################################        
        print "ciclo di tests per la stima dei parametri migliori"    
        # ciclo su tutti i parametri    
        #j è posizione su params
        j=0
        while j < len (parametri):
            #azzero le variabili interne del ciclo
           
            # ciclo su tutte le varianti del parametro 
            tmpParams = list ()
            tmpDims = list ()
            for iParam in parametri[j].keys():                
                #modifico un parametro
                params[j] = parametri[j][iParam]
                # Creo il tok
                tok = CreaTokenizzatore (bestDim, params)
                
                paramTest = parametri[j][iParam]
                if type(paramTest) == type(bool()):
                    print "parametro bool\n"*15
                
                #test Params
                tmpParams.extend (TestTagsTok (testName, self.dimTests[0], tok, False, paramTest = paramTest))
                
                #test Dims
                tmpDims.extend (TestDimsTok (testName, self.dimTests, tok, False, paramTest = paramTest))
                
                #############################   

            #sostituisco il parametro migliore nell'array dei parametri da passare all'atto della creazione
            scoreBestParams ={ele[1]:ele[0] for ele in tmpParams}
            scoreBestDims ={ele[1]:ele[0] for ele in tmpDims}

            if max(scoreBestParams.keys()) >= max(scoreBestDims.keys()):    
                params[j] = scoreBestParams[max(scoreBestParams.keys())]
            else:
                params[j] = scoreBestDims[max(scoreBestDims.keys())]                
            j += 1
        #############################
        
        #giunto a questo punto ho stimato i parametri ottimali per il tokenizzatore
        # l'ultimo test dovrebbe essere  quello con i risultati migliori
        
        #effettuo altri test sulle varie dimensione di addestramento del tokenizzatore
        #con i parametri stimati 
        #Questi sono i test che interessano realmente per questa funzione
        #quindi registro anche questi
# o solo questi? 
        print "Ultimo Test"
        
        for dim in self.dimsTrainTok:
            tok = CreaTokenizzatore (dim, params)
        
            #test Params
            TestTagsTok (testName, self.dimTests[0], tok, True)
            #test Dims
            TestDimsTok (testName, self.dimTests, tok, True)
        
######################################################################
######################################################################
################# FINE MY PUNKT SENTENCE TOKENIZER ###################
######################################################################
######################################################################
             

    
#############  TEXTTILING TOKENIZER  #########################################

    def AvviaTestTextTilingTokenizer (self):
        r""" 
            questo metodo effettua il test sul TextTiling Tokenizer
            Questo metodo crea e avvia i test sul texttililng tokenize
            
            :param str corpus: il corpus su cui testare il tokenizzatore
        """
        
        #per prima cosa avvio il test con i parametri standard, se supera le 
        #euristiche NoZero e ValoreMedio allora procedo con gli altri tests
        
        testName = "TEXTTILING TOKENIZER"        
        s = u"\nTEST : {}".format (testName)   
        self.tools.PrintOut (s)
        
        #creo l'oggetto tokenizzatore        

#        PARAMETRI DI DEFAULT 
#                 w=20,
#                 k=10,
#                 similarity_method=BLOCK_COMPARISON,
#                 stopwords=None,
#                 smoothing_method=DEFAULT_SMOOTHING,
#                 smoothing_width=2,
#                 smoothing_rounds=1,
#                 cutoff_policy=HC,
#                 demo_mode=False)
        #L'UNICO PARAMETRO CHE SCELGO DI PASSARE è QUELLO RELATIVO ALLE STOPWORDS
        tok=nltk.tokenize.TextTilingTokenizer(stopwords = self.stopwords)

        #Oggetto per il corpus
        corpusObj = Tools (self.dimTests[0])
        corpusObj.CaricaCorpus ()
            
        datiOut =  tok.tokenize (corpusObj.CreaPlainText (self.simpleParamS, self.simpleParamW))
        
        r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag=self.simpleParamS)
        self.tools.PrintOut (r)
        
        if self.save:
            #Salvo il file elaborato dal tokenizzatore
            filename = self.folderTestFiles + u" " + self.simpleParamS + u" "  + \
              self.simpleParamW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
            self.tools.SaveFile (filename = filename, dati = datiOut)
            
        if self.EuristicaNoZero (score):
            #proseguo con gli altri 
            print "EuristicaNoZero Superata"

            #calcolo gli altri score dei tests e poi applico l'euristica successiva
                        
            scores = list ()
            
            for paramS in self.paramCorpusCreationS:
                for paramW in self.paramCorpusCreationW:            
                    s = "Test su paramS: %s paramW: %s"% (paramS, paramW)
                    self.tools.PrintOut (s)
                    
                    datiOut =  tok.tokenize (corpusObj.CreaPlainText (paramS, paramW)) 
                    r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag=paramS)
                    self.tools.PrintOut (r)   
                    
                    if self.save:
                        #Salvo il file elaborato dal tokenizzatore
                        filename = self.folderTestFiles + u" " + paramS + u" "  + \
                          paramW + u" " +  unicode(self.dimTests[0]) + u" "  + testName + u".txt"
                        self.tools.SaveFile (filename = filename, dati = datiOut) 
                        
                    if self.EuristicaNoZero (score):                
                        #registro i risultati
                        scores.append (score)
                            
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': True, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                    
                    else:
                        print "Euristica NoZero Non superata, fine test"
#                        print "registro il fallimento del test ed esco dal metodo"
                        test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
                        self.risultatiTest[testName].append(test)
                        
                        return False
                        
            # se sono qui le euristiche di selezione precedenti sono superate
            #ora testo il tokenizzatore nella condizione Nomale in cui trovo un testo
            # provando le diverse dimensioni di campione.
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            scores = list ()
  
            for dim in self.dimTests: 
                s = "Test su %s campioni" % (dim)
                self.tools.PrintOut (s)
        
                corpusObj = Tools (dim)
                corpusObj.CaricaCorpus ()        
                
                datiOut =  tok.tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW)) 
                r, score = self.tools.RisultatiTest(testName, datiOut, self.tools.SENT, corpusObj.words, corpusObj.corpusLst, tag=self.normalParamS)
                self.tools.PrintOut (r)  
                
                if self.save:
                    #Salvo il file elaborato dal tokenizzatore
                    filename = self.folderTestFiles + u" " + self.normalParamS + u" "  + \
                        self.normalParamW + u" " +  unicode(dim) + u" "  + testName + u".txt"
                    self.tools.SaveFile (filename = filename, dati = datiOut)
                    
                test = {'paramS':self.normalParamS, 'paramW':self.normalParamW, 'dim':dim, 'score':score, 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[testName].append(test)
                        
                scores.append (score) 
                            
            if self.EuristicaPrestazioniMedie (scores, soglia = self.sogliaPrestazioniMedie):
                print "Euristica Prestazioni Medie Superata"
                
                test = {'euristicaPrestazioniMedie':True}
                self.risultatiTest[testName].append(test)   
            else:
                print "Euristica Prestazioni Medie NON Superata"
                
                test = {'euristicaPrestazioniMedie':False}
                self.risultatiTest[testName].append(test)
                
                return False
        else:
            print "Euristica No Zero non superata"
            
            test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':self.dimTests[0], 'score':score, 'euristicaNoZero': False, 'tipoTest': self.TIPO_PARAMS}
            self.risultatiTest[testName].append(test)  
            
            return False
            
        #se sono qui ho superato i test precedenti                
        #Se supero l'euristica NoZero, avvio tutti i tests sulle combinazioni
        print "Euristiche superate, si procede con i tests successivi"
       
       #test su tutte le dimensioni in tutti i parametri
        for dim in self.dimTests:
            tests =TextTiling(dim, self.simpleParamS, self.simpleParamW, self.save).AvviaTests ()
            
            #aggiorno la variabile dei test
            for k in tests.keys ():
                test = {'paramS':self.simpleParamS, 'paramW':self.simpleParamW, 'dim':dim, 'score':float(tests[k]), 'euristicaNoZero': self.EuristicaNoZero (float(tests[k])), 'tipoTest': self.TIPO_DIMENS}
                self.risultatiTest[k].append (test)
            
        #test su tutti i parametri cost. corpus   
        for paramS in self.paramCorpusCreationS:
            for paramW in self.paramCorpusCreationW:                            
                tests =TextTiling(self.dimTests[0], paramS, paramW, self.save).AvviaTests ()
               
               #aggiorno la variabile dei test
                for k in tests.keys ():
                    test = {'paramS':paramS, 'paramW':paramW, 'dim':self.dimTests[0], 'score':float(tests[k]), 'euristicaNoZero': self.EuristicaNoZero (float(tests[k])), 'tipoTest': self.TIPO_PARAMS}
                    self.risultatiTest[k].append (test)
                
    ##################################################################################                                           

    ########################################################################
    #######################  EURISTICHE  ###################################
    ########################################################################
    def EuristicaNoZero (self, testResult):
        r"""
            Questa euristica rappresenta la condizione minima per proseguire
            con i tests
            il risultato del test non deve essere zero
        """
        if testResult:
            return True
        else:
            return False

    #NON SERVE, CALCOLATA LA SINGOLA OGNI VOLTA
    def EuristicaNoZeroAll (self, scores):
        r""" 
            Questa euristica rappresenta la condizione minima per proseguire 
            con i tests
            il test deve ottenere risultati diversi da zero in ogni condizione
        """
        for score in scores:
            if not self.EuristicaNoZero (score):
                return False
        return True




    def EuristicaPrestazioniMedie (self, scores, soglia):
        r"""
            il test deve ottenere delle prestazioni medie sopra il valore soglia
        """
        if float(sum(scores) / len(scores)) >= float(soglia):
            return True
        return False
        
#PRINT TODO - >  DA FARE PER MODO DINAMICO MYPUNKT TOKENIZERS        
    def EuristicaDelMiglioramento (self, testResults):
        r"""
            
            il test deve ottenere prestazioni crescenti con 
            dimensioni del campione di test. 
            se i risultati non migliorano con il crescere del numero di campioni
            il test è scartato
        """
        print "TODO"
    ########################################################################
    ########################################################################                                                   
    ########################################################################
                                          
#############################################################################
##########  IL SEGUENTE BLOCCO DI INSTRUZIONI E' ############################
##########  UTILIZZATO PER TESTARE I TEMPI TRA   ############################
##########  IL METODO SEQUENZIALE E QUELLO  #################################
##########  MULTI THREADS ###################################################
#############################################################################
                                           
    def TestTimeThreadVsNormal (self):
        r"""
            Questo metodo testa e registra i tempi per eseguire
            lo stesso compito in modalità normale sequenziale
            oppure multithread
        """
        import time
        import TestTextTiling_old
        
        
        nSamples = [100, 150, 300, 500]
        testNames = ['sequenziale', 'multithread']
        print "Avvio Test"
        for n in nSamples:
            for test in testNames:
                print "Test %s su %f campioni " % (test, n)
                tstart = time.time ()
                tools = Tools(n = n)
                tools.CaricaCorpus ()
                
                for paramS in self.paramCorpusCreationS:
                    for paramW in self.paramCorpusCreationW:
                        #creo il corpus da utilizzare per i tests
                        corpus = tools.CreaPlainText (tagS = paramS, tagW = paramW) 
                        
                        filename = self.folderTestFiles + u" " + unicode(paramS) + u" "  + \
                                                 unicode (paramW) + u" "    
                        if test == 'sequenziale':
                            TestTextTiling_old.TextTiling(corpus, tools = tools, folderTestFiles = filename,
                                                   save = False)
                        else:                     
                             #MThreads
                            TextTiling(corpus, tools = tools, folderTestFiles = filename,
                                                   save = False)                           
                tend = time.time ()
                nSample = n
                execTime = tend - tstart
                filename = self.folderDati + "TestMultiTh.csv"
                self.tools.SaveTimeCsv (filename, test, nSample, execTime)
                print "EXEC TIME %s: %f"%(test, execTime)
                
#############################################################################
    def TestTimeThreads (self):
        r"""
            Questo metodo testa e registra i tempi per eseguire
            lo stesso compito in modalità normale sequenziale
            oppure multithread
        """
        import time 
        
        nSamples = [100, 150, 300, 500, 1000, 1500]
        nThreads = [4, 8]
        
        print "Avvio Test"
        for n in nSamples:
            for nt in nThreads:
                print "Test %d threads su %f campioni " % (nt, n)
                tstart = time.time ()
                tools = Tools(n = n)
                tools.CaricaCorpus ()
                
                for paramS in self.paramCorpusCreationS:
                    for paramW in self.paramCorpusCreationW:
                        #creo il corpus da utilizzare per i tests
                        corpus = tools.CreaPlainText (tagS = paramS, tagW = paramW) 
                        
                        filename = self.folderTestFiles + u" " + unicode(paramS) + u" "  + \
                                                 unicode (paramW) + u" "    

                        self.AvviaTestTextTilingTokenizerMultiThreadsNThread(nt, tools,
                                                corpus, paramS, paramW)
                                                                
                test = "nThread " + unicode (nt)            
                tend = time.time ()
                nSample = n
                execTime = tend - tstart
                filename = self.folderDati + "TestMultiThNTh.csv"
                self.tools.SaveTimeCsv (filename, test, nSample, execTime)
                print "EXEC TIME %s: %f"%(test, execTime)

############################################################################
    #TEXTTILING TOKENIZER MULTI THREAD
    def AvviaTestTextTilingTokenizerMultiThreadsNThread (self, nThread, tools, corpus, paramS, paramW):
        r""" 
            questo metodo effettua il test sul TextTiling Tokenizer
            Questo metodo crea e avvia i test sul texttililng tokenize
            
            :param str corpus: il corpus su cui testare il tokenizzatore
        """
        filename = self.folderTestFiles + u" " + unicode(paramS) + u" "  + \
                                                 unicode (paramW) + u" "        

        #MThreads
        TextTiling(corpus, tools = tools, folderTestFiles = filename,
                                       save = False, nThread = nThread)                
############################################################################                                       
    #TEXTTILING TOKENIZER MULTI THREAD
    def AvviaTestTextTilingTokenizerMultiThreads (self, corpus, paramS, paramW):
        r""" 
            questo metodo effettua il test sul TextTiling Tokenizer
            Questo metodo crea e avvia i test sul texttililng tokenize
            
            :param str corpus: il corpus su cui testare il tokenizzatore
        """
        filename = self.folderTestFiles + u" " + unicode(paramS) + u" "  + \
                                                 unicode (paramW) + u" "        

        #MThreads
        TextTiling(corpus, tools = self.tools, folderTestFiles = filename,
                                           save = self.save)
############################################################################                                           
    #TEXTTILING TOKENIZER
    def AvviaTestTextTilingTokenizerNormal (self, corpus, paramS, paramW):
        r""" 
            questo metodo effettua il test sul TextTiling Tokenizer
            Questo metodo crea e avvia i test sul texttililng tokenize
            
            :param str corpus: il corpus su cui testare il tokenizzatore
        """
        filename = self.folderTestFiles + u" " + unicode(paramS) + u" "  + \
                                                 unicode (paramW) + u" "  
        #old without threaads
        import TestTextTiling_old
        TestTextTiling_old.TextTiling(corpus, tools = self.tools, folderTestFiles = filename,
                                           save = self.save)
                                           
############################################################################
    
                                                   
############################################################################                                                
############################################################################ 
                                           
def Test ():
    print """Test Mode\n si utilizza un campione di dimensione limitata\n 
    usare la classe Test.py per lanciare il testing dei tokenizzatori
    """
    import time
    
    a=TestTokenizer(n = 150)
    a = time.time()
    a.AvviaTests ()       
    b = time.time()
    print a
    print b
    print b-a
    
    
def TestThread ():
    a = TestTokenizer ("MTHREAD", 1)    
    a.TestTimeThreadVsNormal ()

def TestThreadNTh ():
    TestTokenizer ("MTHREAD", 1).TestTimeThreads ()
    
def Tests ():
    ncorpus=[1000, 2500]
    
    #(self, fileRisultati = "Risultati", n = 10, save = True, dimTests = [0]):
    TestTokenizer(dimTests = ncorpus)

    
if __name__=="__main__":
#    TestThreadNTh ()
    Tests ()
    