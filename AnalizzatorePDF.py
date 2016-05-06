# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:04:39 2016

@author: Patrizio
"""
from __future__ import division

from AnalizzatoreBase import AnalizzatoreBase

import collections

from pdfTestCreator import CreaPdf
import os


class AnalizzatorePDF (AnalizzatoreBase):
    r"""questa classe analizza tutti i dati dei tests"""
    
    def VERSION(self):
        return u"vers.0.3.1.b"
        
        
    def __init__(self):#, path, resultFilename=False):
        super (AnalizzatorePDF, self).__init__ ()

    def AvviaCreazionePdf (self):
        for key in self.risultati.keys():
            self.CreaDocumentazioneTest (key)
        self.CreaDocumentazioneBestTest ()

  
    #########################################################################
    def CreaDocumentazioneTest (self, key):
        #suddivido le due tipologie di test
        res = self.SuddividiTipiTest (key)

        #creo il documento pdf del test
        self.CreaPaginaPdfTest (key, res)
     
        
    def CreaDocumentazioneBestTest(self):       
        CreaPdf ().CreaPdfBestTest (self.best)
        
        
    def SuddividiTipiTest (self, key):
        r"""
            Questo metodo suddivide i tests del tokenizers
            in liste differenti secondo la tipologia di test
        """
        res = collections.defaultdict(list)
        
        for test in self.risultati[key]:
            if test.has_key('tipoTest') and  test.has_key('dim'):
                if test['tipoTest'] == self.TIPO_PARAMS:
                    attribute = (test['paramS'], test['paramW'])
                else:
                    attribute = test['dim']
                    
                res[test['tipoTest']].append((attribute, test['score']))
        
        return res
        
        
    def CreaPaginaPdfTest (self, key, res):
        CreaPdf ().CreaPdfTest (key, 
            self.ValorMedioPrestazioni (self.TIPO_PARAMS, res),
            self.ValorMedioPrestazioni (self.TIPO_DIMENS, res),  
            self.MigliorRisultato (self.TIPO_PARAMS, res), 
            self.MigliorRisultato (self.TIPO_DIMENS, res), 
            self.PeggiorRisultato (self.TIPO_PARAMS, res), 
            self.PeggiorRisultato (self.TIPO_DIMENS, res), 
            self.ltestp[key], 
            self.ltestd[key])
        
  
        
if __name__ == '__main__':
# 
    a= AnalizzatorePDF ()
    