# -*- coding: utf-8 -*-
r"""


                NUOVA VERSIONE
                
"""

from __future__ import division, unicode_literals        
        
from Tools import Tools
  
import glob
import nltk
import os


class MyPunktTokenize(Tools):
    r"""questa classe modella il punkt sents tokenize """
    def VERSION(self):
        return u"vers.0.3.7.c"


    def __init__(self):
        #Tools.__init__ (self, 0)
        super (MyPunktTokenize, self).__init__(0)
        #self.folder = os.path.sep + 'mnt' + os.path.sep + '8tera' + os.path.sep + 'shareclic' + os.path.sep + 'lucaNgrams' + os.path.sep + 'Patrizio' + os.path.sep + 'testerTokenizers' + os.path.sep
        self.folderPunkt = self.folder + u"punkt" + os.path.sep
        self.fileExtPnkt = u".punktTok"
        self.fileExtAbbr = u".abl"
        self.folderSents = self.folder + u"corpus" + os.path.sep
        self.folderDati = self.folder + u"dati" + os.path.sep
        self.loglFilename = self.folderDati + "loglikelihood.pickle" 
        
        self = Tools(0)  # Strumenti vari

        #PARAMETRI LINGUISTICI
        self._internal_punctuation = {'default': ',:;', 'estesa': '_-@#,;:'}
        self._end_sent_punct = {'default': ('.', '?', '!'), 'estesa':('.', '?', '!','}',']')}
        
        #files di abbreviazione
        self.abbs = (glob.glob(self.folderDati + '*' + self.fileExtAbbr))

        if not self.abbs:
            #se non sono state calcolate le abbreviazioni faccio partire i calcoli
            import Abbreviazione
            Abbreviazione.Abbreviazione (-1)
            self.abbs = (glob.glob(self.folderDati + '*' + self.fileExtAbbr))
            
        self._ABBREV = [0.1, 0.3, 0.5, 0.7]  #DEFAULT 0.3
        self._IGNORE_ABBREV_PENALITY = [True, False]    #DEFAULT FALSE
        self._ABBREV_BACKOFF = [1, 3, 5 ,7, 9]     #DEFAULT 5

        logls = self.LoadByte (self.loglFilename)
        if not logls:
            #se non è stato calcolato, calcolo il loglikelihood
            import LogLikelihood
            logls = LogLikelihood.LogLikelihood(-1).LogLikelihoods ()
            
        self._COLLOCATION = [7.88]     #DEFAULT 7.88
        self._COLLOCATION.extend(logls)
      
        self._SENT_STARTER = [25, 30, 35, 40]   #DEFAULT 30 
        self._INCLUDE_ALL_COLLOCS = [True, False]      #DEFAULT FALSE
        self._INCLUDE_ABBREV_COLLOCS = [True, False]    #DEFAULT FALSE 
        self._MIN_COLLOC_FREQ = [1, 2, 3]         #DEFAULT 1

        #parametri di default 
        self.D_internal_punctuation = self._internal_punctuation['default']
        self.D_end_sent_punct = self._end_sent_punct['default']
        
        stopws = glob.glob (self.folderDati + u"*.stopWords")
        if len (stopws) == 0:
            import ItalianStopWords
            
            ItalianStopWords.ItalianStopWords().StopWords ()
            ItalianStopWords.ConfrontaStopwords()

            stopws = glob.glob (self.folderDati + u"*.stopWords")
            
        self.Dabbs = self.abbs[0]
        self.D_ABBREV = 0.3
        self.D_IGNORE_ABBREV_PENALITY = False
        self.D_ABBREV_BACKOFF =  5
        self.D_COLLOCATION = 7.88
        self.D_SENT_STARTER = 30 
        self.D_INCLUDE_ALL_COLLOCS = False
        self.D_INCLUDE_ABBREV_COLLOCS = False 
        self.D_MIN_COLLOC_FREQ = 1       

        
    ########################################################################
       

    def CreaMyPunkt (self, corpusTraining, Pinternal_punctuation, Pend_sent_punct, PabbrevFilename, 
                     Pabbrev, PignoreAbbrevPenality, PabbrevBackoff, Pcollocation, PsentStarter, 
                     PincludeAllCollocs, PincludeAbbrevCollocs, PminCollocFreq):

        trainer = self._CreaTok (Pinternal_punctuation, Pend_sent_punct, PabbrevFilename, Pabbrev, 
                    PignoreAbbrevPenality, PabbrevBackoff, Pcollocation, PsentStarter, 
                    PincludeAllCollocs, PincludeAbbrevCollocs, PminCollocFreq)
        
        if trainer == -1:
            return trainer
            
        trainer = self.Training (trainer, corpusTraining)        
        #Creo il tokenizzatore 
        punktTok = nltk.tokenize.punkt.PunktSentenceTokenizer (trainer.get_params ())
        nltk.tokenize.WordPunctTokenizer
        nltk.tokenize.punkt
        return punktTok

    ########################################################################

    
    def Training (self, trainer, corpusTraining):
        #Effettuo il training del corpora
        trainer.train (text = corpusTraining, verbose = False, finalize = True)
        
        return trainer
        
    ########################################################################
        

    def _CreaTok (self, internal_punctuation, end_sent_punct, 
                  abbrsFilename, ABBREV, 
                  IGNORE_ABBREV_PENALITY,      #·controllare bene i parametri in ingresso
                  ABBREV_BACKOFF, COLLOCATION,
                  SENT_STARTER, INCLUDE_ALL_COLLOCS, 
                  INCLUDE_ABBREV_COLLOCS, MIN_COLLOC_FREQ):
        r"""
            Questa funzione, dati i parametri in ingresso crea il tokenizzatore
        """

        #Language Params
        #inizio creando gli oggetti del punkt
        languageParam = nltk.tokenize.punkt.PunktLanguageVars 
        
        #internal punctuactions    - type string  - 
        languageParam.internal_punctuation = internal_punctuation
        #end sent punctuactions    - type tuple
        languageParam.sent_end_chars = end_sent_punct

        #Punkt Parameters 
        punktParameters = nltk.tokenize.punkt.PunktParameters()

        #Base Class     
        baseClass = nltk.tokenize.punkt.PunktBaseClass (lang_vars=languageParam,  params=punktParameters)

        #Trainer
        #Effettuo il training delle abbreviazioni

        if not abbrsFilename:
            abbrs = self.Dabbs
            
        abbrs = [ele.strip() for ele in self.LoadByte(abbrsFilename)]
            
        abbrs = "\n".join (abbrs) 
        abbrs = "Start" + abbrs  + "End."
#new         
        try:
            trainer = nltk.tokenize.punkt.PunktTrainer (abbrs, baseClass) 
        except ValueError:
            return -1
        #fase 2 aggiungo i parametri
        trainer.ABBREV = ABBREV
        trainer._IGNORE_ABBREV_PENALITY = IGNORE_ABBREV_PENALITY
        trainer.ABBREV_BACKOFF = ABBREV_BACKOFF
        trainer.COLLOCATION = COLLOCATION
        trainer.SENT_STARTER = SENT_STARTER
        trainer.INCLUDE_ALL_COLLOCS = INCLUDE_ALL_COLLOCS
        trainer.INCLUDE_ABBREV_COLLOCS = INCLUDE_ABBREV_COLLOCS
        trainer.MIN_COLLOC_FREQ = MIN_COLLOC_FREQ
    
        return trainer
        
        
    ########################################################################

    def GetStandardParams (self):
        r"""
            Questo metodo restituisce un'array contenente tutti i parametri di default
        """
        return [self.D_internal_punctuation, self.D_end_sent_punct, self.Dabbs, 
                self.D_ABBREV, self.D_IGNORE_ABBREV_PENALITY, self.D_ABBREV_BACKOFF, 
                self.D_COLLOCATION, self.D_SENT_STARTER, self.D_INCLUDE_ALL_COLLOCS,
                self.D_INCLUDE_ABBREV_COLLOCS, self.D_MIN_COLLOC_FREQ]            
    
    
    def GetAllParams (self):
        r"""
            Questo metodo restituisce un'array contenente tutti i parametri con tutte le varianti
        """
        return [self._internal_punctuation, self._end_sent_punct, 
            {e:e for e in self.abbs},
            {e:e for e in self._ABBREV},
            {e:e for e in self._IGNORE_ABBREV_PENALITY},
            {e:e for e in self._ABBREV_BACKOFF},
            {e:e for e in self._COLLOCATION},
            {e:e for e in self._SENT_STARTER},
            {e:e for e in self._INCLUDE_ALL_COLLOCS},
            {e:e for e in self._INCLUDE_ABBREV_COLLOCS},
            {e:e for e in self._MIN_COLLOC_FREQ}]
        
    ########################################################################

    
######### SISTEMARE BENE BENE BENE                                                            
#    def CreaFilename (self):
#        
#        if self.dimSamples == -1:
#            self.dimSamples = self.nSents
#        filename = unicode(self.dimSamples) + u" " + unicode(paramS) + u"_"+unicode(paramW)
#        filename = filename + u" iPun_" + unicode(internalPunct)   
#           
#        filename = filename + u" ePun_" + unicode(endSentPunct)
#        
#        filename = filename + u" abr_" + unicode(str(pktAbbrev))       
#        if pktIgnoreAbbrevPenality:
#            filename = filename+u" IgAbPn_T"
#        else:
#            filename = filename + u" IgAbPn_F"         
#        filename = filename + u" AbbBck_" + unicode(pktAbbrevBackoff)                           
#        filename = filename + u" Col_" + unicode(pktCollocation)            
#        filename = filename + u" sSt_" + unicode(pktSentStarter)          
#        if pktIncAllCollocs:
#            filename = filename + u" ACl_T"
#        else:
#            filename = filename + u" ACl_F"
#        if pktIncAbbrevCollocs:
#            filename = filename + u" Ab_T"
#        else:
#            filename = filename + u" Ab_F"
#        filename = filename + u" mFr_" + unicode(pktMinCollFreq)
#        #abbrev filename
#        filenameAbr = os.path.basename(abbreviaz)[:os.path.basename(abbreviaz).rindex(os.path.extsep)]
#        filename = filename + u" aF_" + unicode(filenameAbr)
#        
#        return filename
                                                            
  
                                                      
if __name__=='__main__':
    print "non utilizzabile - richiamare all'interno di una funzione parametrizzandolo"
    a=MyPunktTokenize()
    
######### TEMPORANEO ###############       
    def functA (a, b, c, d, e):
        print a
        print b
        return (a+b+c+d+e)
    l=[2,3,4,5]
    functA(1, *l)
    
    
