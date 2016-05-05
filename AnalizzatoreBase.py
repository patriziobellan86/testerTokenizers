# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:04:39 2016

@author: Patrizio
"""
from __future__ import division

from Tools import Tools

import collections
import os
import glob

#for d in [a,b]:
#    for k in d.keys():
#        c[k]=d[k]
#  
class AnalizzatoreBase (Tools):
    r"""questa classe analizza tutti i dati dei tests"""
    
    def VERSION(self):
        return u"vers.0.1.b"
        
        
    def __init__(self):#, path, resultFilename=False):
        super (AnalizzatoreBase, self).__init__ ()
        
        self.tmp=collections.defaultdict(list)
        #self.risultati = self.LoadByte (resultFilename)
        
        
###############new       ####### 
        self.risultati =collections.defaultdict(list)
        #fondo i risultati in un'unica variabile
        print self.CaricaParametro(parametro = 'testFiles')
        files = glob.glob (self.CaricaParametro(parametro = 'testFiles') + os.path.sep + '*.risultati')
        
        #files = [self.LoadByte (files)]
        for file in files:
            print file    
            d = self.LoadByte (file)
            print             
            print d.items()
            for d in self.LoadByte (file).items():
                self.risultati[d[0]].append( d[1])

#################à        
        self.tests = collections.defaultdict (list)
        self.best = collections.defaultdict (list)
        
        self.AnalizzaDati()
 
        
    def AnalizzaDati (self):
        nofiltro = collections.defaultdict (list)
        filtro = collections.defaultdict (list)
        
        self.ltestp = collections.defaultdict (list)
        self.ltestd = collections.defaultdict (list)

        for key in self.risultati.keys():
        #divido in due liste distinte
#newwwwwwwwww
            for eles in self.risultati[key]:
                
                for ele in eles:
                    if ele.has_key ('attributiTok') and ele['attributiTok']:
                        k_2 = ele['attributiTok'].__str__()
                        filtro[(key, k_2)].append (ele)
                    else:
                        nofiltro[key].append (ele)
           
        #ora devo effettuare una selezione tra i test con attributo e 
        #riportare solo la parametrizzazione migliore
        
        for lkey in filtro.keys():
            bestp = {'score':0}
            bestd = {'score':0}
            #ora ho una lista in lkey
            for ele in filtro[lkey]:
                if ele.has_key('score'):       
                    if ele['tipoTest'] == u'PARAMS':
                        if float(ele['score']) > float(bestp['score']):
                            bestp = ele
                            if ele.has_key('attributiTok'):
                                self.ltestp[lkey[0]] = [ele['attributiTok']]
                        elif ele['score'] == bestp['score'] and ele.has_key('attributiTok'):    
                            self.ltestp[lkey[0]].append (ele['attributiTok'])
                            #self.ltestp[lkey[0]].append (key)
                    elif ele['tipoTest'] == u'DIMS':
                        if float(ele['score']) > float(bestp['score']):
                            bestd = ele
                            if ele.has_key('attributiTok'):
                                self.ltestd[lkey[0]] = [ele['attributiTok']]
                        elif ele['score'] == bestp['score'] and ele.has_key('attributiTok'):    
                            self.ltestd[lkey[0]].append (ele['attributiTok'])                            

            #aggiungo il test alla lista dei filtrati
            if bestp['score'] > 0:                        
                nofiltro[lkey[0]].append (bestp)
            if bestd['score'] > 0:
                nofiltro[lkey[0]].append (bestd)
        
        self.risultati = nofiltro

        for key in self.risultati.keys():
            self.VisualizzaDocumentazioneTest (key)
        #controllare la funzione qui sotto che va in errore!!!!
        self.EstraiMiglioriTok () 

  
    #########################################################################
    def VisualizzaDocumentazioneTest (self, key):
        #suddivido le due tipologie di test
        res = self.SuddividiTipiTest (key)
        
        print "Test %s"%key
        
        #Valor medio dei test
        print "Valore medio prestazioni"
        print "Media prestazioni test sulla tipologia PARAMS : ",  self.ValorMedioPrestazioni (self.TIPO_PARAMS, res)
        print "Media prestazioni test sulla tipologia DIMS   : ",  self.ValorMedioPrestazioni (self.TIPO_DIMENS, res)
        
        
        print "Miglior risultato"
        print "Prestazione migliore test sulla tipologia PARAMS :",  self.MigliorRisultato (self.TIPO_PARAMS, res)
        print "Prestazione migliore test sulla tipologia DIMS   :",  self.MigliorRisultato (self.TIPO_DIMENS, res)
         
        print "peggior risultato"
        print "Prestazione peggiore test sulla tipologia PARAMS :",  self.PeggiorRisultato (self.TIPO_PARAMS, res)
        print "Prestazione peggiore test sulla tipologia DIMS   :",  self.PeggiorRisultato (self.TIPO_DIMENS, res)
        
        #aggiungo i valori a self.test
        self.tests ['valMedioParams'].append ((key, self.ValorMedioPrestazioni (self.TIPO_PARAMS, res)))
        self.tests ['valMedioDms'].append ((key, self.ValorMedioPrestazioni (self.TIPO_DIMENS, res)))
        self.tests['BestParams'].append ((key, self.MigliorRisultato (self.TIPO_PARAMS, res)))
        self.tests['BestDims'].append ((key, self.MigliorRisultato (self.TIPO_DIMENS, res)))


    def EstraiMiglioriTok (self):
        #per ogni categoria estraggo il migliore
        
        best = (0, 0)
        blist = []
        for ele in self.tests ['valMedioParams']:       
            if float(ele[1]) > float(best[1]):            
                best = ele
                blist = [ele]
            elif float(ele[1]) == float(best[1]):
                blist.append (ele)
                    
        self.best['valMedioParams'] = blist
        
        best = (0, 0)
        blist = []
        for ele in self.tests ['valMedioDms']:
            if float(ele[1]) > float(best[1]):
                best = ele
                blist = [ele]
            elif float(ele[1]) == float(best[1]):
                blist.append (ele)
        self.best['valMedioDms'] = blist
        
        best = (0, (0, 0))
        blist = []
        for ele in self.tests ['BestParams']:   
            if float(ele[1][1]) > float(best[1][1]):            
                best = ele
                blist = [ele]
            elif float(ele[1][1]) == float(best[1][1]):
                blist.append (ele)
        self.best['BestParams'] = blist
        
        best = (0, (0, 0))
        blist = []
        for ele in self.tests ['BestDims']:   
            if float(ele[1][1]) > float(best[1][1]):            
                best = ele
                blist = [ele]
            elif float(ele[1][1]) == float(best[1][1]):
                blist.append (ele)
        self.best['BestDims'] = blist
             
        print "TOKENIZZATORI CON I RISULTATI MIGLIORI"
        
        print "Valore medio prestazioni"
        print "Media prestazioni test sulla tipologia PARAMS : "
        for i in self.best['valMedioParams']:
            print "Test : %s \n Value : %f"%(i)
            
        print "Media prestazioni test sulla tipologia DIMS : "
        for i in self.best['valMedioDms']:
            print "Test : %s \n Value : %f"%(i)

        print "Miglior risultato"
        print "Prestazione migliore test sulla tipologia PARAMS :"
        for i in self.best['BestParams']:
            print "Test : %s \ncondizione %s Value : %f"%(i[0], i[1][0], i[1][1])  
   
        print "Prestazione migliore test sulla tipologia DIMS :"
        for i in self.best['BestDims']:
            print "Test : %s \ncondizione %s Value : %f"%(i[0], i[1][0], i[1][1])  
            
        
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
        
        
    def ValorMedioPrestazioni (self, tipo, res):
        r"""
            Questo metodo calcola le prestazioni medie inerente a tutti i tests
            suddivisi in base alla tipologia dei tests
            
            tipo il tipo di test
            res la variabile contente i risultati
        """
        tot = float (0)
        for ele in res[tipo]:
            tot = tot + ele[1]
        try:
            return float (tot / len(res[tipo]))
        except ZeroDivisionError:
            return 0
        
    def MigliorRisultato (self, tipo, res):
        r"""
            Questo metodo estrae il miglior risultato dei test
        """
        best = (0, 0)
        for ele in res[tipo]:
            if ele[1] >= best[1]:
                best = ele
        return best
        
        
    def PeggiorRisultato (self, tipo, res):
        r"""
            Questo metodo estrae il miglior risultato dei test
        """
        best = (1, 1)
        for ele in res[tipo]:
            if ele[1] <= best[1]:
                best = ele
        return best
        
        
if __name__ == '__main__':
#    f='C:\\Users\\Patrizio\\Documents\\prova testi\\tokenizer\\risultati\\SimpleLineTokenizer.risultati'#LineTokenizer.risultati'#Risultati.txt'
#    #f='C:\\Users\\Patrizio\\Documents\\prova testi\\tokenizer\\0.3.8.3.1\\testFiles\\rEGULeXPRESSIONsENTStOK.risultati'
#    
#    f='C:\\Users\\Patrizio\\Documents\\prova testi\\tokenizer\\risultati\\'
    a= Analizzatore ()#f)
    