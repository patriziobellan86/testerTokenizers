# -*- coding: utf-8 -*-
"""

@author: Patrizio

    


            usato ereditarietà di:
            tools
                    
"""


from __future__ import division, unicode_literals

from Tools import Tools, CorpusObj
from TestTextTiling import TextTiling
from CreatorePunktTokenize import MyPunktTokenize
from DimSamplesPunkt import DimSamplesPunkt

import Queue
import threading
import multiprocessing

import nltk
import re
import os

import collections


class TestTokenizer(Tools):
    r""" 
        Questa classe si occupa di lanciare in eseguzione tutti i tests sui tokenizers presenti in nlkt
    """
    def VERSION(self):
        return u"vers.0.3.8.a"
      
      
    def __init__(self, fileRisultati = "Risultati", save = False, 
            dimTests = [0], aggiornaDatiTest = False):
        

        
        #self.folder = os.path.sep + 'mnt' + os.path.sep + '8tera' + os.path.sep + 'shareclic' + os.path.sep + 'lucaNgrams' + os.path.sep + 'Patrizio' + os.path.sep + 'testerTokenizers' + os.path.sep

        self.dimTests = dimTests   #list numerosità test espressa in numero di frasi

        self.sogliaMiglioramento = 0.05
        self.passoTraining = 50000
        #tmp        
#        self.passoTraining = 1000

        self.save = save
                  
        self.TIPO_PARAMS = 'PARAMS'
        self.TIPO_DIMENS = 'DIMS'
        


        #pathFileRisultati = self.folderTestFiles + fileRisultati
        
        #fileRisultati = self.folderTestFiles + fileRisultati

      
#inizializzazione classe ereditata qui!
        
        #self=Tools(n = 0, fileRisultati = (pathFileRisultati))        
        #Tools.__init__ (self, n = 0, fileRisultati = (fileRisultati))
        super (TestTokenizer, self).__init__(n = 0, fileRisultati = (fileRisultati))
#        
#
#        self.folderTestFiles = self.folder + u"testFiles" + os.path.sep
#
#        self.folderPunkt = self.folder + u"punkt" + os.path.sep
#        self.fileExtPnkt = u".punktTok"
#        self.folderDati = self.folder + u"dati" + os.path.sep        
#        
#        self.folderCorpusTraining = self.folder + "corpusTraining" + os.path.sep
#        
#        self.fileRisultati = self.folderTestFiles + "results.pickle"
#        self.fileNameRe = self.folderDati + u"RegularExpression.tag"
#        self.stopwordsFilename = self.folderDati + u"Italian Stopwords.stopWords"
#        self.fileExtPnkt = u".punktTok"
        
#        
#        self.paramCorpusCreationW = self.TAGW
#        self.paramCorpusCreationS = self.TAGS.keys()
#        
        #Condizione Semplice
        self.simpleParamS = 'PARAG_2'
        self.simpleParamW = 'SPACE'
        #Condizione Normale
        self.normalParamS = 'SPACE'
        self.normalParamW = 'SPACE'
        #Stopwords 
        self.stopwords = self.LoadByte (self.stopwordsFilename)
        #patterns per Re
        self.patterns = self.LoadByte (self.fileNameRe)

        if aggiornaDatiTest:
            self.risultatiTest = self.LoadByte (self.fileRisultati)
            if not self.risultatiTest:
                self.risultatiTest = collections.defaultdict (list)
        else:
            self.risultatiTest = collections.defaultdict(list)
#new istr       SPOSTATA IN TEST     
#        self.CreaCorpusOrigin ()
        
        self.AvviaTests ()
        

    ########################################################################
        
    def AvviaTests (self):
        r"""
            Questo metodo si occupa di mandare in eseguzione tutti i tests
        """
        
        s = u"\n Avvio dei Tests"
        s = s + u"\n Avvio dei tests sui Words Tokenizers\n"
        self.PrintOut (s)
        self.AvviaTestWordsTokenizers ()
      
        s = u"\n Avvio dei tests sui Sents Tokenizers\n"
        self.PrintOut (s)
        self.AvviaTestSentsTokenizers ()
        self.__Save ()
        print "FINE TEST"
        
        
    def __Save (self):
        
        #Salvo il file dei risultati
        self.SaveByte (self.risultatiTest, self.fileRisultati)
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
            self.AvviaTestREWordTok (tipo = self.WORD)
        self.__Save ()

    ########################################################################

    def AvviaTestSentsTokenizers (self):
        r"""
            Questo metodo testa tutti i tokenizzatori di frasi        
        """       
       
        #nltk.tokenize.simple
        self.TestSimpleLineTokenizerWord ()

        self.TestSimpleTokenizer ()

        self.TestSimpleTokenizerIta ()

        if self.patterns:
            self.AvviaTestREWordTok (tipo = self.SENT)

        self.AvviaTestTextTilingTokenizer ()

       
        self.TestMyPunkt ()
        self.__Save ()
        
    ########################################################################
        
# ##### spostato in  test       
#    def CreaCorpusOrigin (self):
#        print "creazione dei corpus per i test in corso..."
#        for dim in self.dimTests:        
#            for paramS in self.TAGS.keys():
#                    for paramW in self.TAGW:
#                        self.n = dim
#                        self.CaricaCorpus ()
#                        self.CreaPlainText2 (paramS, paramW)
#                        
#                        print "Corpus %s %s %s creato correttamente" % (dim, paramS, paramW)
                        
    def __TestTokenizer (self, testName, dimTests, tok, tipo, attributi = None, attrFilename = None): 
        def Tests ():             
            self.queue =  Queue.Queue ()
            #popolo la coda di test
            dim = dimTests[0]
            for paramS in self.TAGS.keys():
                for paramW in self.TAGW:            
                    self.queue.put((testName, tok, dim, paramS, paramW, 
                        self.TIPO_PARAMS, tipo, attributi, attrFilename))
            for dim in dimTests:
                self.queue.put((testName, tok, dim, self.normalParamS, 
                        self.normalParamW, self.TIPO_DIMENS, tipo, attributi, attrFilename))
                        
            self.__Save ()
            
            return self.TestTok ()
            ############################
            
        return Tests ()
        
   
    def TestTok (self):
        class MyThread  (threading.Thread):
            def __init__ (self, testFunction, numberTh, dati, r):
                threading.Thread.__init__(self)                
                self.name = numberTh
                self.__test = testFunction
                self.dati = dati
                self.r = r
                
            def run (self):
                
                try:
                    print "Inizio thread", self.name
                    self.r.append(self.__test (*self.dati))
                    print "Fine thread", self.name
                    
                except:
                    print "break thread", self.name
                    #global r
                    self.r.append (False)
                    return
        i=0
        r = []
        while not self.queue.empty ():
          
            lt = []
            #utilizzo tanti thread quanti sono i processori logici dell'elaboratore
            for  i in xrange (1): #dato che il server mi killa il processo decido di mandarne in eseguzione solo 1 alla volta 4): # limito i thread a 4 #multiprocessing.cpu_count()):
            #for  i in xrange (self.queue.qsize ()):
          
                try:
                    if self.queue.empty ():
                        #se non ci sono più dati da elaborare esco dal ciclo di elaborazione
                        break
                    t = MyThread (self.__Test, i, self.queue.get (), r)
                    #thl.release ()
                    t.daemon = True
                    t.start ()
                    #t.join ()
                    i+=1
                    lt.append (t)
                except:
                    pass
            #aspetto finchè ci sono thread vivi
            while sum([l.isAlive() for l in lt]):
                pass
            #r = [r.r for r in t]
            r.sort()
            #dopo sort i False sono messi per primi
            if not r[0]:
                return False
    
        return True
 #       return r

###########################################        
 
    def __Test (self, testName, tok, dim, paramS, paramW, tipoTest, tipo, attributi, attrFilename, registra = True):
        try:
            s = u"\nTEST : {}".format (testName) 
            print s
            s = s + "\nTest su %d in condizioni paramS: %s paramW: %s" % (dim, paramS, paramW)
            #self.PrintOut (s)
#Modifica Qui!

            corpus = CorpusObj(dim, paramS, paramW)
            datiOut = tok.tokenize (corpus.Txt())
            
#old            
#            #Oggetto per il corpus
#            corpusObj = Tools (dim)
#            corpusObj.CaricaCorpus ()
#   
#            datiOut = tok.tokenize (corpusObj.CreaPlainText (paramS, paramW))
########
            
            if tipo == self.SENT:
                tag = paramS
            else:
                tag = u""
                
                
#new new NEW
            r, score = self.RisultatiTest(testName, datiOut, tipo, corpus.Words(), corpus.Lst (), tag)
###old                
#            r, score = self.RisultatiTest(testName, datiOut, tipo, corpusObj.words, corpusObj.corpusLst, tag)
######


            self.PrintOut (s + r)   
            #Salvo il file elaborato dal tokenizzatore
            fileTest = None
            if self.save and registra:
                if not attrFilename:
                    attrFilename = u""

#new                     
                filename = self.folderTestFiles + testName + u" " + attrFilename + u" " + paramS + u" " + paramW + u" " +  unicode(len(corpus.Words())) + u" " + u".txt"
#old
#                filename = self.folderTestFiles + testName + u" " + attrFilename + u" " + paramS + u" " + paramW + u" " +  unicode(len(corpusObj.words)) + u" " + u".txt"                
#####
                fileTest = filename
                
                self.SaveFile (filename = filename, dati = datiOut) 
                
                
            if self.EuristicaNoZero (score): 
                self.PrintOut ("Euristica NoZero superata")     
            else:
                self.PrintOut ("Euristica NoZero Non superata")
                
            test = {'paramS':paramS, 'paramW':paramW, 'dim':len(corpus.Words()), 
                    'score':score, 'euristicaNoZero': self.EuristicaNoZero (score), 
                    'tipoTest': tipoTest, 'fileTest': fileTest, 'attributiTok': attributi}
            if registra:       
                self.risultatiTest[testName].append(test)
            
            return (score, test)
        except:
            print "il testo non è elaborabile dal tokenizzatore %s"% testName
            return False
            

    ########################################################################
    #SIMPLE SPACE TOKENIZER

    def TestSimpleSpaceTokenizerWord (self): 
        r""" 
            questo metodo effettua il test sullo simple space word tokenize
        """
        testName = u"SIMPLE SPACE WORD TOKENIZER"
        dimTests = self.dimTests
        tok = nltk.tokenize.simple.SpaceTokenizer()
        tipo = self.WORD
        self.__TestTokenizer (testName, dimTests, tok, tipo)
                          

        
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################

    ########################################################################
                  
    #SIMPLE WORD TOKENIZER
    def TestSimpleWordTokenizer (self):
        r""" 
            questo metodo effettua il test sullo standard word tokenizer
        """ 
        class Tok :
            def tokenize (self, sents):
                return nltk.tokenize.word_tokenize (sents)
                
        testName = u"STANDARD WORD TOKENIZER"
        dimTests = self.dimTests
        tok = Tok ()
        tipo = self.WORD
        self.__TestTokenizer (testName, dimTests, tok, tipo)
        
 
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
              
              
    #SIMPLE WORD TOKENIZER ITA
    def TestSimpleWordTokenizerIta (self):
        r""" 
            questo metodo effettua il test sullo standard word tokenizer ita
        """
        class Tok :
            def tokenize (self, sents):
                return nltk.tokenize.word_tokenize (sents, language='italian')
                
        testName = u"STANDARD WORD TOKENIZER ITA"
        dimTests = self.dimTests
        tok = Tok ()
        tipo = self.WORD
        self.__TestTokenizer (testName, dimTests, tok, tipo)
        

    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################


    #TREEBANK TOKENIZER
    def TestTreeBankTokenizer (self):
        r""" 
            questo metodo effettua il test sul treebank tokenizer
        """
        testName = u"STANDARD WORD TOKENIZER ITA"
        dimTests = self.dimTests
        tok = nltk.tokenize.TreebankWordTokenizer()
        tipo = self.WORD
        self.__TestTokenizer (testName, dimTests, tok, tipo)
        
                  
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
        dimTests = self.dimTests
        tok = nltk.tokenize.simple.LineTokenizer()
        tipo = self.SENT
        self.__TestTokenizer (testName, dimTests, tok, tipo)
        
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
                          


    #SIMPLE TAB TOKENIZER
    def TestSimpleTabTokenizerWord (self):
        r""" 
            questo metodo effettua il test sullo simple tab tokenize
        """
        testName = u"SIMPLE TAB SENT TOKENIZER"
        dimTests = self.dimTests
        tok = nltk.tokenize.simple.TabTokenizer()
        tipo = self.SENT
        self.__TestTokenizer (testName, dimTests, tok, tipo)
       
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
                          

    #SIMPLE TOKENIZER
    def TestSimpleTokenizer (self):
        r""" 
            questo metodo effettua il test sullo standard sent tokenizer
        """
        class Tok :
            def tokenize (self, sents):
                return nltk.tokenize.sent_tokenize (sents)
         
        testName =  u"SIMPLE SENT TOKENIZER"
        dimTests = self.dimTests
        tok = Tok ()
        tipo = self.SENT
        self.__TestTokenizer (testName, dimTests, tok, tipo)
    
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
  
    #SIMPLE TOKENIZER ITA
    def TestSimpleTokenizerIta (self):
        r""" 
            questo metodo effettua il test sul simple sent tokenizer ita
        """
        class Tok :
            def tokenize (self, sents):
                return nltk.tokenize.sent_tokenize (sents, language='italian')
         
        testName = u"SIMPLE SENT TOKENIZER ITA"
        dimTests = self.dimTests
        tok = Tok ()
        tipo = self.SENT
        self.__TestTokenizer (testName, dimTests, tok, tipo) 
        
        
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
        self.PrintOut(s)
      
        for pattern in self.patterns.keys():
            if tipo == pattern[1]:
                #Avvio i Tests per il tipo  
                self.TestREWordTok_patter_w_gaps_F_discard_empty_T_flags_reUNI (
                    pattern = self.patterns[pattern], patternName = pattern[0], tipo = tipo)                    
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
        
    ############################################################################        
       
    def TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reUNI (self, 
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """

        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=True, flags=re.UNICODE)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': True, 'flags': 're.UNI'}
        attrfn = u"gap=True discardEmpty=True flags=re.UNI"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)
                        
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """

        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=True, flags=re.MULTILINE)
        tipo = tipo
        attributiTok ={'gap': True, 'discardEmpty': True, 'flags': 're.MULTI'}
        attrfn =  u"gap=True discardEmpty=True flags=re.MULTI"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)
              
    #################################################################################


    def TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """

        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=True, flags=re.DOTALL)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': True, 'flags': 're.DOTALL'}
        attrfn = u"gap=True discardEmpty=True flags=re.DOTALL"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)
          
    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discard_empty_T_flags_reUNI (self,
                                                pattern, patternName, tipo):   
        r""" 
            Standard Regular Expression Tokenizer
           
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
 
        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=True, flags=re.UNICODE)
        tipo = tipo
        attributiTok = {'gap': False, 'discard_empty': True, 'flags': 're.UNI'}
        attrfn = u"gap=False discard_empty=True flags=re.UNI"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)

    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_F_discardEmpty_T_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
 
        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=True, flags=re.MULTILINE)
        tipo = tipo
        attributiTok = {'gap': False, 'discardEmpty': True, 'flags': 're.MULTI'}
        attrfn = u"gap=False discardEmpty=True flags=re.MULTI"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)

    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discardEmpty_T_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """

        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=True, flags=re.DOTALL)
        tipo = tipo
        attributiTok = {'gap': False, 'discardEmpty': True, 'flags': 're.DOTALL'}
        attrfn =  u" gap=False discardEmpty=True flags=re.DOTALL"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)

    ##################################################################################
                

    def TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reUNI (self, 
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
 
        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer(pattern, gaps=True, discard_empty=False, flags=re.UNICODE)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': False, 'flags': 're.UNI'}
        attrfn = u"gap=True discardEmpty=False flags=re.UNI"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)
    
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """

        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=False, flags=re.MULTILINE)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': False, 'flags': 're.MULTI'}
        attrfn = u"gap=True discardEmpty=False flags=re.MULTI"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)
        
    #################################################################################


    def TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
 
        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=False, flags=re.DOTALL)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': False, 'flags': 're.DOTALL'}
        attrfn = u"gap=True discardEmpty=False flags=re.DOTALL"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)
               
    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discard_empty_F_flags_reUNI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        
        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=False, flags=re.UNICODE)
        tipo = tipo
        attributiTok = {'gap': False, 'discard_empty': False, 'flags': 're.UNI'}
        attrfn = u"gap=False discard_empty=False flags=re.UNI"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)

    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_F_discardEmpty_F_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        
        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=False, flags=re.MULTILINE)
        tipo = tipo
        attributiTok =  {'gap': False, 'discardEmpty': False, 'flags': 're.MULTI'}
        attrfn = u"gap=False discardEmpty=False flags=re.MULTI"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)

    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discardEmpty_F_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        
        testName = patternName
        dimTests = self.dimTests
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=False, flags=re.DOTALL)
        tipo = tipo
        attributiTok =  {'gap': False, 'discardEmpty': False, 'flags': 're.DOTALL'}
        attrfn = u"gap=False discardEmpty=False flags=re.DOTALL"
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)

    ##################################################################################   
    
############### MY PUNKT TOKENIZERS   #######################################
   
   
    def TestMyPunkt (self):
        r""" 
            questo metodo effettua i tests sui Punkt Tokenizers
        """
        
        def CreaTokenizzatore (dimTraining, params):  
            r"""
                Questo metodo crea il tokenizzatore con i parametri richiesti
                
                :param int dimTraining: la dimensione di training del tok
                :param tuple params: la tupla contenente tutti i parametri con cui modellare il tok
                
                :return: il tokenizzatore modellato
                :rtype: tok
            """
            
            obj = Tools (dimTraining)
            
            obj.CaricaCorpus (folder = self.folderCorpusTraining)
            #test mode
            #obj.CaricaCorpus ()
            
            return MyPunktTokenize().CreaMyPunkt (obj.CreaPlainText (self.simpleParamS, self.simpleParamW), *params)            

            #######################################            

        def TestTagsTok (testName, dim, tok, registra = False, paramTest = None):
            r""" 
                Questo metodo effettua il ciclo dei test sulla dimensione Params
                è utilizzato durante la fase di stima dei parametri
                
                Questo metodo deve restituire solo True o False
                o list(tuple(paramTest, score))
            
                :param str testName: nome del tok
                :param int dim: dimensione di training
                :param tok tok: tokenizzatore da testare
                :param bool registra: flag che indica se il test è da registrare
                :param     paramTest: il parametro in fase di test
                
                :return: i risultati dei test
                :rtype: tuple
            """
            tupleScores = list ()
            
#old    
#            #Oggetto per il corpus      
#            corpusObj = Tools (dim) 
#            corpusObj.CaricaCorpus ()
##
            for paramS in self.TAGS.keys():
                for paramW in self.TAGW:     
#new 
                    corpus = CorpusObj(dim, paramS, paramW)
                    datiOut = tok.tokenize (corpus.Txt())
                    r, score = self.RisultatiTest(testName, datiOut, self.SENT, corpus.Words (), corpus.Lst (), tag = paramS)
#old
#                    datiOut =  tok.tokenize (corpusObj.CreaPlainText (paramS, paramW))                      
#                    r, score = self.RisultatiTest(testName, datiOut, self.SENT, corpusObj.words, corpusObj.corpusLst, tag = paramS)

                    tupleScores.append (tuple([paramTest, score]))
                    
            return tupleScores
            
            #########################################    
                 
        def TestDimsTok (testName, dims, tok, registra = False, paramTest = None):
            r""" 
                Questo metodo effettua il ciclo dei test sulla dimensione Dims
                è utilizzato durante la fase di stima dei parametri
                
                Questo metodo deve restituire solo True o False
                o list(tuple(paramTest, score))
            
                :param str testName: nome del tok
                :param int dim: dimensione di training
                :param tok tok: tokenizzatore da testare
                :param bool registra: flag che indica se il test è da registrare
                :param     paramTest: il parametro in fase di test
                
                :return: i risultati dei test
                :rtype: tuple
            """
            
            tupleScores = list ()
            
            for dim in dims: 
#new                 
                
                corpus = CorpusObj(dim, self.normalParamS, self.normalParamW)
                datiOut = tok.tokenize (corpus.Txt())
                r, score = self.RisultatiTest(testName, datiOut, self.SENT, corpus.Words (), corpus.Lst (), tag = self.normalParamS)
#old
#                corpusObj = Tools (dim)
#                corpusObj.CaricaCorpus ()        
#                datiOut =  tok.tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW)) 
#                r, score = self.RisultatiTest(testName, datiOut, self.SENT, corpusObj.words, corpusObj.corpusLst, tag = self.normalParamS)
####            
                tupleScores.append (tuple([paramTest, score]))                        
                
            return tupleScores
            
            ###################################
            
        def Best (tuplaScores):
            """
               Questa funzione restituisce il primo parametro della tupla migliore
             
                :param list(tuple) tuplaScores: lista di tuple (param, score)
                
                :return: il parametro con il punteggio più alto
                :rtype: param
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
        #per prima cosa addestro e testo il tokenizzatore con i parametri standard

        #Stimo il dimensionamento di training migliore, calcolato sul primo valore delle dimensioni dei test
        #questi parametri servono per effettuare almeno una volta il ciclo
        precScore = 0
        attScore = self.sogliaMiglioramento
        dim = self.passoTraining
        dimsent = abs(DimSamplesPunkt().NumSents (dim))
        nsentprec = 0 #questa var mi serve per controllare di non eccedere oltre le dimensioini del corpus di training
        
        print "inizio euristica miglioramento default punkt"
        while self.EuristicaMiglioramento (precScore, attScore):

            precScore = attScore
            if nsentprec == dimsent:
                break
            
            testName =   u"DEFAULT PUNKT TOKENIZER"
            
            #creo il tokenizzatore
            tok = CreaTokenizzatore (dimsent, params)    
            if tok == -1:
                continue
            
            tipo = self.SENT
            attributiTok =  {'dimTrainingWords': dim}
            attrfn = unicode(dim)
            attScore, test_ = self.__Test (testName, tok, self.dimTests[0], 
                    self.normalParamS, self.normalParamW, self.TIPO_DIMENS, 
                    self.SENT, attributiTok, attrfn)
            
            nsentprec = dimsent         
            #precScore = attScore
            dim = dim + self.passoTraining
            dimsent = abs(DimSamplesPunkt().NumSents (dim))
        print "fine stima dimensione di training"
        print "inizio test su default punkt tok"
        #Effettuo e registro il test con i parametri standard
        testName =   u"DEFAULT PUNKT TOKENIZER"
        #effettuo i test
        dimTests = self.dimTests
        #creo il tokenizzatore
        tok = CreaTokenizzatore (dimsent, params)    
        
        tipo = self.SENT
        attributiTok =  {'dimTrainingWords': dim}
        attrfn = unicode(dim)
        self.__TestTokenizer (testName, dimTests, tok, tipo, attributiTok, attrfn)
            
        #ora inizio a cercare i parametri migliori per il tokenizzatore
        #utilizzando come dimensione di training la minore 

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
                tok = CreaTokenizzatore (dimsent, params)
 
                if tok == -1:
                    print "Parametri non utilizzabili per creare il tokenizzatore"
                    print params
                                        
                    continue
                
                paramTest = parametri[j][iParam]
                
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

        #Calcolo la dimensione di Training Migliore
        precScore = 0
        attScore = self.sogliaMiglioramento
        dim = self.passoTraining
        dimsent = abs(DimSamplesPunkt().NumSents (dim))
        nsentprec = 0 #questa var mi serve per controllare di non eccedere oltre le dimensioini del corpus di training
        print "inizio stima dim training my punkt"
        while self.EuristicaMiglioramento (precScore, attScore):
            precScore = attScore
            if nsentprec == dimsent:
                break
            
            testName =   u"MY PUNKT TOKENIZER"
            
            #creo il tokenizzatore
            tok = CreaTokenizzatore (dimsent, params)    
            
            tipo = self.SENT
            attributiTok =  {'dimTrainingWords': dim}
            attrfn = unicode(dim)
            
            attScore, test_ = self.__Test (testName, tok, self.dimTests[0], 
                    self.normalParamS, self.normalParamW, self.TIPO_DIMENS, 
                    self.SENT, attributiTok, attrfn)
            
            nsentprec = dimsent  
            dim = dim + self.passoTraining
            dimsent = abs(DimSamplesPunkt().NumSents (dim))

        print "fine stima dimensione di training"
        print "inizio test my punkt"
        
        #Test con il dimensionamento del tok già effettuato dall'istr prec
        testName = u"MY BEST PUNKT TOKENIZER"
        #creo il tokenizzatore
        tok = CreaTokenizzatore (dimsent, params)    
        
        #salvo il tokenizzatore
        tokfilename = self.folderPunkt + testName + self.fileExtPnkt
        
        self.SaveByte (tok, tokfilename)
        #devo implementare tokenize method!!!!
        tipo = self.SENT
        attributiTok =  {'dimTrainingWords': dim}
        attrfn = unicode(dimsent)
        self.__TestTokenizer (testName, [self.dimTests[0]], tok, tipo, attributiTok, attrfn)  
           
        ############################################      
           
######################################################################
################# FINE MY PUNKT SENTENCE TOKENIZER ###################
######################################################################


#############  TEXTTILING TOKENIZER  #########################################

    def AvviaTestTextTilingTokenizer (self):
        r""" 
            questo metodo effettua il test sul TextTiling Tokenizer
            Questo metodo crea e avvia i test sul texttililng tokenize
            
            :param str corpus: il corpus su cui testare il tokenizzatore
        """
        #utilizzo la stessa procedura di stima dei parametri del mypunkt tokenizer
        def CreaTokenizzatore (params):
            r"""
                Questo metodo crea il tokenizzatore con i parametri richiesti
                
                :param tuple params: la tupla contenente tutti i parametri con cui modellare il tok
                
                :return: il tokenizzatore modellato
                :rtype: tok
            """            
            return TextTiling().CreaTextTilingTokenizer (*params)            

            #######################################            

        def TestTagsTok (testName, dim, tok, registra = False, paramTest = None):
            r""" 
                Questo metodo effettua il ciclo dei test sulla dimensione Params
                è utilizzato durante la fase di stima dei parametri
                
                Questo metodo deve restituire solo True o False
                o list(tuple(paramTest, score))
            
                :param str testName: nome del tok
                :param int dim: dimensione di training
                :param tok tok: tokenizzatore da testare
                :param bool registra: flag che indica se il test è da registrare
                :param     paramTest: il parametro in fase di test
                
                :return: i risultati dei test
                :rtype: tuple
            """
           
            tupleScores = list ()
#old
#            #Oggetto per il corpus      
#            corpusObj = Tools (dim) 
#            corpusObj.CaricaCorpus ()
#              
            for paramS in self.TAGS.keys():
                for paramW in self.TAGW:  
                    try:
#new 
                        corpus = CorpusObj(dim, paramS, paramW)
                        datiOut = tok.tokenize (corpus.Txt())
                        r, score = self.RisultatiTest(testName, datiOut, self.SENT, corpus.Words (), corpus.Lst (), tag = paramS)
#old
#                        datiOut =  tok.tokenize (corpusObj.CreaPlainText (paramS, paramW))             
#                        r, score = self.RisultatiTest(testName, datiOut, self.SENT, corpusObj.words, corpusObj.corpusLst, tag = paramS)
####àà                    
                        tupleScores.append (tuple([paramTest, score]))
                    except:
                        #se il tokenizzatore non è applicabile al testo
                        tupleScores.append (tuple([paramTest, 0.0]))
            return tupleScores
            
            #########################################    
                 
        def TestDimsTok (testName, dims, tok, registra = False, paramTest = None):
            r""" 
                Questo metodo effettua il ciclo dei test sulla dimensione Dims
                è utilizzato durante la fase di stima dei parametri
                
                Questo metodo deve restituire solo True o False
                o list(tuple(paramTest, score))
            
                :param str testName: nome del tok
                :param int dim: dimensione di training
                :param tok tok: tokenizzatore da testare
                :param bool registra: flag che indica se il test è da registrare
                :param     paramTest: il parametro in fase di test
                
                :return: i risultati dei test
                :rtype: tuple
            """
            #in questo caso per passare deve superare l'euristica delle prestazioni medie
            tupleScores = list ()
            
            for dim in dims: 
#old                
#                corpusObj = Tools (dim)
#                corpusObj.CaricaCorpus ()        
#                try:
#                    datiOut =  tok.tokenize (corpusObj.CreaPlainText (self.normalParamS, self.normalParamW)) 
#                    r, score = self.RisultatiTest(testName, datiOut, self.SENT, corpusObj.words, corpusObj.corpusLst, tag = self.normalParamS)
#            
#new 
                corpus = CorpusObj(dim, self.normalParamS, self.normalParamW)
                try:                
                    datiOut = tok.tokenize (corpus.Txt())
                    r, score = self.RisultatiTest(testName, datiOut, self.SENT, corpus.Words (), corpus.Lst (), tag = self.normalParamS)
#########
                    tupleScores.append (tuple([paramTest, score]))                        
                except:
                    #se il tokenizzatore non è applicabile al testo
                    tupleScores.append (tuple([paramTest, 0.0]))
            return tupleScores
            
            ###################################
            
        def Best (tuplaScores):
            """
               Questa funzione restituisce il primo parametro della tupla migliore
             
                :param list(tuple) tuplaScores: lista di tuple (param, score)
                
                :return: il parametro con il punteggio più alto
                :rtype: param
            """
                              
            best = (0, 0)
            for i in tuplaScores:
                if best[1] < i[1]:
                       best = i
            return best[0]
            #####################################
                
        # questi due arrays vengono passati direttamente dall'oggetto creatore MyPunktTokenize
        parametri = TextTiling().GetAllParams ()  # contiene tutte le varianti dei parametri
        params = TextTiling().GetStandardParams ()  #all'avvio del metodo continene i parametri standard
           
        ########PARTE STANDARD DEL TESTS  #################
        #per prima cosa addestro e testo il tokenizzatore con i parametri standard
        testName =   u"DEFAULT TEXTITILING TOKENIZER"
            
        #creo il tokenizzatore
        tok = CreaTokenizzatore (params)    
        tipo = self.SENT
        attributiTok =  {'params default': params}
        attrfn = "_default_params"
        #inserita espressione di controllo - dato che questo tipo di tokenizzatore è applicabile solo
        # ad un campo ristretto di tipologie di testo        
        if not self.__TestTokenizer (testName, self.dimTests, tok, tipo, attributiTok, attrfn):        
            print "Fine funzione di test ", testName
            return
            
        print "fine prima parte test"
        ##################################
            
        #ora inizio a cercare i parametri migliori per il tokenizzatore
       
        print "ciclo di tests per la stima dei parametri migliori"    
        # ciclo su tutti i parametri    
        #j è posizione su params
        j = 0
        while j < len (parametri):
            #azzero le variabili interne del ciclo
           
            # ciclo su tutte le varianti del parametro 
            tmpParams = list ()
            tmpDims = list ()
            for iParam in parametri[j].keys():                
                #modifico un parametro
                params[j] = parametri[j][iParam]
                # Creo il tok
                tok = CreaTokenizzatore (params)
                
                paramTest = parametri[j][iParam]
                
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
       
        #testo con i parametri stimati
        testName =   u"MY TEXTITILING TOKENIZER"
            
        #creo il tokenizzatore
        tok = CreaTokenizzatore (params)    
            
        tipo = self.SENT
        attributiTok =  {'my params': params}
        attrfn = "_my_params"
        
        self.__TestTokenizer (testName, self.dimTests, tok, tipo, attributiTok, attrfn)
                
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
        if testResult > 0:
            return True
        else:
            return False


    def EuristicaMiglioramento (self, precScore, attScore):
        r"""
            Questo metodo ritorna True se c'è stato un miglioramento
            False altrimenti
            
        """
        if float (attScore) > float (precScore) * (1 + float (self.sogliaMiglioramento)):
            return True
        return False
                                                      
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
                
                for paramS in self.TAGS.keys():
                    for paramW in self.TAGW:
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
                self.SaveTimeCsv (filename, test, nSample, execTime)
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
                
                for paramS in self.TAGS.keys():
                    for paramW in self.TAGW:
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
                self.SaveTimeCsv (filename, test, nSample, execTime)
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
        TextTiling(corpus, tools = self, folderTestFiles = filename,
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
        TestTextTiling_old.TextTiling(corpus, tools = self, folderTestFiles = filename,
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
    nc = 20000
    TestTokenizer (dimTests = [nc / 2, nc / 4, nc], save =True, aggiornaDatiTest=True)

    
if __name__=="__main__":
#    TestThreadNTh ()
    Tests ()
    
