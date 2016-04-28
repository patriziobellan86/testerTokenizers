# -*- coding: utf-8 -*-
"""

@author: Patrizio

    


            usato ereditarietà di:
            tools
                    
"""


from __future__ import division, unicode_literals

from Tools import Tools
from TestTextTiling import TextTiling
from CreatorePunktTokenize import MyPunktTokenize

import nltk
import re
import glob
import collections


class TestTokenizer(Tools):
    r""" 
        Questa classe si occupa di lanciare in eseguzione tutti i tests sui tokenizers presenti in nlkt
    """
    def VERSION(self):
        return u"vers.0.3.8.a"
      
      
    def __init__(self, fileRisultati = "Risultati", save = False, 
            dimTests = [0], aggiornaDatiTest = False):
        
        super (TestTokenizer, self).__init__(n = 0, fileRisultati = (fileRisultati))
        
        self.dimTests = dimTests   #list numerosità test espressa in numero di frasi

        self.sogliaMiglioramento = float (self.CaricaParametro(parametro = 'sogliaMiglioramento'))
        self.passoTraining = int (self.CaricaParametro(parametro = 'passoTraining'))
        
        self.save = save
                  
        self.TIPO_PARAMS = 'PARAMS'
        self.TIPO_DIMENS = 'DIMS'
        
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
            self.risultatiTest = self.LoadByte (self.fileRisultatiPickle)
            if not self.risultatiTest:
                self.risultatiTest = collections.defaultdict (list)
        else:
            self.risultatiTest = collections.defaultdict(list)
        print "File risultati %s" % (self.fileRisultatiPickle)
        self.__Save ()
        self.AvviaTests ()
        

    ########################################################################
        
    def AvviaTests (self):
        r"""
            Questo metodo si occupa di mandare in esecuzione tutti i tests
        """
        
        s = u"\n Avvio dei Tests"
        s = s + u"\n Avvio dei tests sui Words Tokenizers\n"
        self.PrintOut (s)
        self.AvviaTestWordsTokenizers ()
      
        s = u"\n Avvio dei tests sui Sents Tokenizers\n"
        self.PrintOut (s)
        self.AvviaTestSentsTokenizers ()
        self.__Save ()
        
        print 
        print "FINE TEST"
        
    ########################################################################
        
    def __Save (self):
        
        #Salvo il file dei risultati
        return self.SaveByte (dati = self.risultatiTest, filename = self.fileRisultatiPickle)
        
    ########################################################################
        
    #TESTS SUI WORDS TOKENIZERS
    def AvviaTestWordsTokenizers (self):
        r"""
            Questo metodo testa tutti i tokenizzatori di parole        
        """     

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
        
    def __TestTokenizer2 (self, testName, tok, tipo, attributi = None, attrFilename = None): 
        r"""
            Nuova Versione
            
            non uso il multithread perchè ho notato che mi dà problemi sul server
            
        """
        #ciclo di test
      
        for paramS in self.TAGS.keys():
            for paramW in self.TAGW:   
                score, test = self.__Test2 (testName, tok, self.dimTests[0], paramS, paramW, self.TIPO_PARAMS, tipo, attributi, attrFilename)   
                s=self.__Save ()                
                print "risultati salvati: ", s
                if not s:
                    print "Errore salvataggio file %s" % self.fileRisultatiPickle
                if score == False:
                    return False
        
        for dim in self.dimTests:
            score, test = self.__Test2(testName, tok, dim, self.normalParamS, self.normalParamW, self.TIPO_DIMENS, tipo, attributi, attrFilename)
            s=self.__Save ()                
            print "risultati salvati: ", s
            if not s:
                print "Errore salvataggio file %s" % self.fileRisultatiPickle
            if score == False:
                return False
        
         #mettere un return!!!!!!!!!

    def __Test2 (self, testName, tok, dim, paramS, paramW, tipoTest, tipo, attributi, attrFilename, registra = True):
     
        scores = []
       
        if tipo == self.SENT:
            tag = paramS
        else:
            tag = u""
            
        s = u"\nTEST : {}".format (testName) 
        s = s + "\nTest %s sù %d campioni, in condizioni paramS: %s paramW: %s" % (testName, dim, paramS, paramW)
        print s

        #suddivido il carico di elaborazione in sottotest
        ws = int (self.CaricaParametro (parametro = "finestraCorpusIn"))
        
        #dimenisone max frasi
        filesCorpus = glob.glob (self.folderCorpus + '*')
        filesCorpus = filesCorpus [:dim]       #seleziono solo la parte di dimensione dim
        
        dimFilesCorpus = len (filesCorpus)    #lo calcolo una volta per tutte
        
        totTest = int(dimFilesCorpus/ ws)
        print "totTest: ", totTest
        
        for i in xrange (totTest):
            
            print "esecuzione test %s %d / %d - params %s %s %s %s" % (testName, i, totTest, dim, paramS, paramW, tipoTest)
            #carico la finestra di corpus
            files = filesCorpus[i * ws: i * ws + ws]
            
            #creo il corpus
            corpus = self.CorpusObj(files, paramS, paramW)

            try:
                #effettuo il test
                datiOut = tok.tokenize (corpus['txt'])#.Txt ())
            except:
                print "il testo non è elaborabile dal tokenizzatore %s" % testName
                return (False, False)
                
            r, score = self.RisultatiTest(testName, datiOut, tipo, corpus['words'], corpus['lst'], tag) #.Words(), corpus.Lst (), tag)
            
            #self.PrintOut (r)
            
            #registro i dati del test e passo al successivo
            scores.append (score)
            
        #calcolo la media dei risultati
        score = sum (scores) / len (scores)
              
        print "Score medio test: ", score
        
        if self.EuristicaNoZero (score): 
            self.PrintOut ("Euristica NoZero superata")     
        else:
            self.PrintOut ("Euristica NoZero Non superata")
            
        test = {'paramS':paramS, 'paramW':paramW, 'dim':len(corpus['words']), 
                'score':score, 'euristicaNoZero': self.EuristicaNoZero (score), 
                'tipoTest': tipoTest, 'fileTest': 'NONE - LITE VERSION', 'attributiTok': attributi}
        
        if registra:       
            self.risultatiTest[testName].append(test)
            s = self.__Save ()
            print "file risultati %s salvato: " % self.fileRisultatiPickle
            print s
            if not s:
                print "Errore salvataggio file %s" % self.fileRisultatiPickle
        return (score, test)

    ########################################################################
    #SIMPLE SPACE TOKENIZER

    def TestSimpleSpaceTokenizerWord (self): 
        r""" 
            questo metodo effettua il test sullo simple space word tokenize
        """

        testName = u"SIMPLE SPACE WORD TOKENIZER"
        
        tok = nltk.tokenize.simple.SpaceTokenizer()
        tipo = self.WORD

        self.__TestTokenizer2 (testName, tok, tipo)
          
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
        tok = Tok ()
        tipo = self.WORD
        
        self.__TestTokenizer2 (testName, tok, tipo)
        
 
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
        tok = Tok ()
        tipo = self.WORD
        
        self.__TestTokenizer2 (testName, tok, tipo)
        

    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################


    #TREEBANK TOKENIZER
    def TestTreeBankTokenizer (self):
        r""" 
            questo metodo effettua il test sul treebank tokenizer
        """
        testName = u"STANDARD WORD TOKENIZER ITA"
        tok = nltk.tokenize.TreebankWordTokenizer()
        tipo = self.WORD
        
        self.__TestTokenizer2 (testName, tok, tipo)
        
                  
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
        tok = nltk.tokenize.simple.LineTokenizer()
        tipo = self.SENT
        
        self.__TestTokenizer2 (testName, tok, tipo)
        
    ########## FINE TESTS SU QUESTO TOKENIZER ##############################
    ########################################################################
    ########################################################################
                          


    #SIMPLE TAB TOKENIZER
    def TestSimpleTabTokenizerWord (self):
        r""" 
            questo metodo effettua il test sullo simple tab tokenize
        """
        testName = u"SIMPLE TAB SENT TOKENIZER"
        tok = nltk.tokenize.simple.TabTokenizer()
        tipo = self.SENT
        
        self.__TestTokenizer2 (testName, tok, tipo)
       
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
        tok = Tok ()
        tipo = self.SENT
        
        self.__TestTokenizer2 (testName, tok, tipo)
    
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
        tok = Tok ()
        tipo = self.SENT
        
        self.__TestTokenizer2 (testName, tok, tipo)
        
        
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
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=True, flags=re.UNICODE)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': True, 'flags': 're.UNI'}
        attrfn = u"gap=True discardEmpty=True flags=re.UNI"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
                        
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """

        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=True, flags=re.MULTILINE)
        tipo = tipo
        attributiTok ={'gap': True, 'discardEmpty': True, 'flags': 're.MULTI'}
        attrfn =  u"gap=True discardEmpty=True flags=re.MULTI"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
                
    #################################################################################


    def TestREWordTok_patter_w_gaps_T_discardEmpty_T_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """

        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=True, flags=re.DOTALL)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': True, 'flags': 're.DOTALL'}
        attrfn = u"gap=True discardEmpty=True flags=re.DOTALL"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
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
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=True, flags=re.UNICODE)
        tipo = tipo
        attributiTok = {'gap': False, 'discard_empty': True, 'flags': 're.UNI'}
        attrfn = u"gap=False discard_empty=True flags=re.UNI"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_F_discardEmpty_T_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
 
        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=True, flags=re.MULTILINE)
        tipo = tipo
        attributiTok = {'gap': False, 'discardEmpty': True, 'flags': 're.MULTI'}
        attrfn = u"gap=False discardEmpty=True flags=re.MULTI"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discardEmpty_T_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """

        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=True, flags=re.DOTALL)
        tipo = tipo
        attributiTok = {'gap': False, 'discardEmpty': True, 'flags': 're.DOTALL'}
        attrfn =  u" gap=False discardEmpty=True flags=re.DOTALL"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
    ##################################################################################
                

    def TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reUNI (self, 
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
 
        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer(pattern, gaps=True, discard_empty=False, flags=re.UNICODE)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': False, 'flags': 're.UNI'}
        attrfn = u"gap=True discardEmpty=False flags=re.UNI"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """

        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=False, flags=re.MULTILINE)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': False, 'flags': 're.MULTI'}
        attrfn = u"gap=True discardEmpty=False flags=re.MULTI"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
    #################################################################################


    def TestREWordTok_patter_w_gaps_T_discardEmpty_F_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
 
        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=True, discard_empty=False, flags=re.DOTALL)
        tipo = tipo
        attributiTok = {'gap': True, 'discardEmpty': False, 'flags': 're.DOTALL'}
        attrfn = u"gap=True discardEmpty=False flags=re.DOTALL"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discard_empty_F_flags_reUNI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        
        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=False, flags=re.UNICODE)
        tipo = tipo
        attributiTok = {'gap': False, 'discard_empty': False, 'flags': 're.UNI'}
        attrfn = u"gap=False discard_empty=False flags=re.UNI"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
    #################################################################################   
        
        
    def TestREWordTok_patter_w_gaps_F_discardEmpty_F_flags_reMULTI (self,
                                                pattern, patternName, tipo):   
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        
        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=False, flags=re.MULTILINE)
        tipo = tipo
        attributiTok =  {'gap': False, 'discardEmpty': False, 'flags': 're.MULTI'}
        attrfn = u"gap=False discardEmpty=False flags=re.MULTI"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
    #################################################################################


    def TestREWordTok_patter_w_gaps_F_discardEmpty_F_flags_reDOTALL (self,
                                                pattern, patternName, tipo): 
        r""" 
            questo metodo effettua sui RE tokenizer
        
            :param str pattern: il pattern re da testare
            :param str patternName: il nome del patten
        """
        
        testName = patternName
        tok = nltk.tokenize.RegexpTokenizer (pattern, gaps=False, discard_empty=False, flags=re.DOTALL)
        tipo = tipo
        attributiTok =  {'gap': False, 'discardEmpty': False, 'flags': 're.DOTALL'}
        attrfn = u"gap=False discardEmpty=False flags=re.DOTALL"
        
        self.__TestTokenizer2 (testName,  tok, tipo, attributiTok, attrfn)
          
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

            for paramS in self.TAGS.keys():
                for paramW in self.TAGW:     
                    attributi = None
                    attrFilename = None
                    score, test = self.__Test2 (testName, tok, dim, paramS, paramW, self.TIPO_PARAMS, tipo, attributi, attrFilename, registra = False)
                            
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
                attributi = None
                attrFilename = None
                score, test = self.__Test2 (testName, tok, dim, self.normalParamS, self.normalParamW, self.TIPO_DIMENS, tipo, attributi, attrFilename, registra = False)

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
        dimsent = self.NumSents (dim)
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
            dimsent = self.NumSents (dim)
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
        dimsent = self.NumSents (dim)
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
            dimsent = self.NumSents (dim)

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

            for paramS in self.TAGS.keys():
                for paramW in self.TAGW:  
                    try:
                        attributi = None
                        attrFilename = None
                        score, test = self.__Test2 (testName, tok, dim, paramS, paramW, self.TIPO_PARAMS, tipo, attributi, attrFilename, registra = False)
                                            
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
                try: 
                    attributi = None
                    attrFilename = None
                    score, test = self.__Test2 (testName, tok, dim, self.normalParamS, self.normalParamW, self.TIPO_DIMENS, tipo, attributi, attrFilename, registra = False)
                          
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
        if not self.__TestTokenizer2 (testName, self.dimTests, tok, tipo, attributiTok, attrfn):        
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
              
if __name__=="__main__":
    print "No Test mode"
    
