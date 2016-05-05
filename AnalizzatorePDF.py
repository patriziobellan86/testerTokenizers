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

#for d in [a,b]:
#    for k in d.keys():
#        c[k]=d[k]
#  
class AnalizzatorePDF (AnalizzatoreBase):
    r"""questa classe analizza tutti i dati dei tests"""
    
    def VERSION(self):
        return u"vers.0.3.1.b"
        
        
    def __init__(self):#, path, resultFilename=False):
        super (AnalizzatorePDF, self).__init__ ()
#        
#        self.tmp=collections.defaultdict(list)
#        #self.risultati = self.LoadByte (resultFilename)
#        
#        
################new       ####### 
#        self.risultati =collections.defaultdict(list)
#        #fondo i risultati in un'unica variabile
#        print self.CaricaParametro(parametro = 'testFiles')
#        files = glob.glob (self.CaricaParametro(parametro = 'testFiles') + os.path.sep + '*.risultati')
#        
#        #files = [self.LoadByte (files)]
#        for file in files:
#            print file    
#            d = self.LoadByte (file)
#            print             
#            print d.items()
#            for d in self.LoadByte (file).items():
#                self.risultati[d[0]].append( d[1])
##                
##                #print d, type(d)
##                for k in d.keys():
##                    self.risultati[d[0]] = d[1]
##                
#                
##        r=self.risultati
#
#
#
##################à        
#        self.tests = collections.defaultdict (list)
#        self.best = collections.defaultdict (list)
#        
#        self.AnalizzaDati()
# 
#        
#    def AnalizzaDati (self):
#        nofiltro = collections.defaultdict (list)
#        filtro = collections.defaultdict (list)
#        
#        self.ltestp = collections.defaultdict (list)
#        self.ltestd = collections.defaultdict (list)
#
#        for key in self.risultati.keys():
#        #divido in due liste distinte
##newwwwwwwwww
#            for eles in self.risultati[key]:
#                
#                for ele in eles:
#                    if ele.has_key ('attributiTok') and ele['attributiTok']:
#                        k_2 = ele['attributiTok'].__str__()
#                        filtro[(key, k_2)].append (ele)
#                    else:
#                        nofiltro[key].append (ele)
#           
#        #ora devo effettuare una selezione tra i test con attributo e 
#        #riportare solo la parametrizzazione migliore
#        
#        for lkey in filtro.keys():
#            bestp = {'score':0}
#            bestd = {'score':0}
#            #ora ho una lista in lkey
#            for ele in filtro[lkey]:
#                if ele.has_key('score'):       
#                    if ele['tipoTest'] == u'PARAMS':
#                        if float(ele['score']) > float(bestp['score']):
#                            bestp = ele
#                            if ele.has_key('attributiTok'):
#                                self.ltestp[lkey[0]] = [ele['attributiTok']]
#                        elif ele['score'] == bestp['score'] and ele.has_key('attributiTok'):    
#                            self.ltestp[lkey[0]].append (ele['attributiTok'])
#                            #self.ltestp[lkey[0]].append (key)
#                    elif ele['tipoTest'] == u'DIMS':
#                        if float(ele['score']) > float(bestp['score']):
#                            bestd = ele
#                            if ele.has_key('attributiTok'):
#                                self.ltestd[lkey[0]] = [ele['attributiTok']]
#                        elif ele['score'] == bestp['score'] and ele.has_key('attributiTok'):    
#                            self.ltestd[lkey[0]].append (ele['attributiTok'])                            
#
#            #aggiungo il test alla lista dei filtrati
#            if bestp['score'] > 0:                        
#                nofiltro[lkey[0]].append (bestp)
#            if bestd['score'] > 0:
#                nofiltro[lkey[0]].append (bestd)
#        
#        self.risultati = nofiltro
    def AvviaCreazionePdf (self):
        for key in self.risultati.keys():
            self.CreaDocumentazioneTest (key)
        self.self.CreaDocumentazioneBestTest ()

  
    #########################################################################
    def CreaDocumentazioneTest (self, key):
        #suddivido le due tipologie di test
        res = self.SuddividiTipiTest (key)

        #creo il documento pdf del test
        self.CreaPaginaPdfTest (key, res)

#
#    def EstraiMiglioriTok (self):
#        #per ogni categoria estraggo il migliore
#        
#        best = (0, 0)
#        blist = []
#        for ele in self.tests ['valMedioParams']:       
#            if float(ele[1]) > float(best[1]):            
#                best = ele
#                blist = [ele]
#            elif float(ele[1]) == float(best[1]):
#                blist.append (ele)
#                    
#        self.best['valMedioParams'] = blist
#        
#        best = (0, 0)
#        blist = []
#        for ele in self.tests ['valMedioDms']:
#            if float(ele[1]) > float(best[1]):
#                best = ele
#                blist = [ele]
#            elif float(ele[1]) == float(best[1]):
#                blist.append (ele)
#        self.best['valMedioDms'] = blist
#        
#        best = (0, (0, 0))
#        blist = []
#        for ele in self.tests ['BestParams']:   
#            if float(ele[1][1]) > float(best[1][1]):            
#                best = ele
#                blist = [ele]
#            elif float(ele[1][1]) == float(best[1][1]):
#                blist.append (ele)
#        self.best['BestParams'] = blist
#        
#        best = (0, (0, 0))
#        blist = []
#        for ele in self.tests ['BestDims']:   
#            if float(ele[1][1]) > float(best[1][1]):            
#                best = ele
#                blist = [ele]
#            elif float(ele[1][1]) == float(best[1][1]):
#                blist.append (ele)
#        self.best['BestDims'] = blist
#             
#        print "TOKENIZZATORI CON I RISULTATI MIGLIORI"
#        
#        print "Valore medio prestazioni"
#        print "Media prestazioni test sulla tipologia PARAMS : "
#        for i in self.best['valMedioParams']:
#            print "Test : %s \n Value : %f"%(i)
#            
#        print "Media prestazioni test sulla tipologia DIMS : "
#        for i in self.best['valMedioDms']:
#            print "Test : %s \n Value : %f"%(i)
#
#        print "Miglior risultato"
#        print "Prestazione migliore test sulla tipologia PARAMS :"
#        for i in self.best['BestParams']:
#            print "Test : %s \ncondizione %s Value : %f"%(i[0], i[1][0], i[1][1])  
#   
#        print "Prestazione migliore test sulla tipologia DIMS :"
#        for i in self.best['BestDims']:
#            print "Test : %s \ncondizione %s Value : %f"%(i[0], i[1][0], i[1][1])  
#            
#        self.CreaDocumentazioneBestTest ()
        
        
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
#    f='C:\\Users\\Patrizio\\Documents\\prova testi\\tokenizer\\risultati\\SimpleLineTokenizer.risultati'#LineTokenizer.risultati'#Risultati.txt'
#    #f='C:\\Users\\Patrizio\\Documents\\prova testi\\tokenizer\\0.3.8.3.1\\testFiles\\rEGULeXPRESSIONsENTStOK.risultati'
#    
#    f='C:\\Users\\Patrizio\\Documents\\prova testi\\tokenizer\\risultati\\'
    a= Analizzatore ()#f)
    