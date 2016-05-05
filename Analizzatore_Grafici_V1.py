# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:04:39 2016

@author: Patrizio
"""
from __future__ import division

from Tools import Tools

import collections

import numpy as np
import matplotlib.pyplot as plt
import os
import glob

#for d in [a,b]:
#    for k in d.keys():
#        c[k]=d[k]
#  
class Analizzatore (Tools):
    r"""questa classe analizza tutti i dati dei tests"""
    
    def VERSION(self):
        return u"vers.0.3.1.b"
        
        
    def __init__(self):#, path, resultFilename=False):
        super (Analizzatore, self).__init__ ()
        
        self.tmp=collections.defaultdict(list)
        #self.risultati = self.LoadByte (resultFilename)
        
        
###############new       ####### 
        self.risultati =collections.defaultdict(list)
        #fondo i risultati in un'unica variabile
        print self.CaricaParametro(parametro = 'testFiles')
        files = glob.glob (self.CaricaParametro(parametro = 'testFiles') + os.path.sep + '*.risultati')
        
        #files = [self.LoadByte (files)]
        for file in files:
            d = self.LoadByte (file)
            for d in self.LoadByte (file).items():
                self.risultati[d[0]].append( d[1])
#                
#                #print d, type(d)
#                for k in d.keys():
#                    self.risultati[d[0]] = d[1]
#                
                
#        r=self.risultati



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
            self.CreaDocumentazioneTest (key)
        #controllare la funzione qui sotto che va in errore!!!!
        self.EstraiMiglioriTok () 

  
    #########################################################################
    def CreaDocumentazioneTest (self, key):
        #suddivido le due tipologie di test
        res = self.SuddividiTipiTest (key)
        
        print "Creazione documentazione per il test %s"%key
        
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

        print "Creazione Grafico su parmas"
        self.GraficoParamas (key, res)
        
        print "Creazione grafico su dims"
        self.GraficoDims (key, res)


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
        
        
    def GraficoParamas (self, testName, res):
        self.Plot(testName, self.TIPO_PARAMS, res)
            
            
    def GraficoDims (self, testName, res):
        self.Plot(testName, self.TIPO_DIMENS, res)
        
    
    def Plot(self, testName, tipo, res):
        r"""
            Questa funzione plotta i dati
        """
        def autolabel(rects):
            i=0
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                        '%f perc.' % yValue[i], ha='center', va='bottom') 
                i+=1
    
        #dati 
    
        #etichette dei dati
        xLabel =  [ele[0] for ele in res[tipo]]
        if tipo == "PARAMS":
            #tipi di ricostruzione TagS e TagW
            xLabel = ["tagS: " + ele[0] + " tagW: " + ele[1] for ele in xLabel]
            yValue = [round(float(ele[1]) * 100, 2) for ele in res[tipo]]
        else:
            #Numero di parole nel corpus di test   
           xLabel = ["words: " + str(self.NumWords(ele)) for ele in xLabel] 
           yValue = [round(float(ele) * 100, 2) for ele[1] in res[tipo]]

        N = len (xLabel)
        ind = np.arange (N)  # coordinate x
        width = 0.25       # dimensione bar
        valoriY = tuple (yValue)
        
        #creo le figure
        fig, ax = plt.subplots ()
        rects1 = ax.bar (ind, valoriY, width, color='r')
        
        #asse y
        ax.set_ylabel('Score medio dei test')
        if tipo == "PARAMS":
            ax.set_xlabel('parametri di ricostruzione frase e parole')
        elif tipo == "DIMS":
            ax.set_xlabel('dimensioni del corpus di test')
            
        #asse x            
        ax.set_xticks (ind + width)
        ax.set_xticklabels (tuple(xLabel), rotation=90)
        
        #etichette dati
        autolabel(rects1)
  
        #titolo del grafico
        plt.title("Risultati dei test del tokenizzatore: " + testName)
        
        #calcolo la media
        try:
            mean = sum(yValue) / len(yValue)
        except ZeroDivisionError:
            mean = 0


        #plotto la media
        x = np.linspace(0,len(xLabel),50,endpoint=True)
        y1= [mean]*50
        plt.plot(x,y1, color='yellow', label='media prestazioni',linewidth=1.0, linestyle="-")
         
        #imposto i limiti degli assi
        ax.set_xlim(0, len (xLabel))
        ax.set_ylim(0, 100)
       
        #aggiungo la leggenda
        ax.legend(fontsize=8)
        
        #sistemo la figura
        plt.tight_layout(pad=2)
        
        #salvo la figura
        filename = self.folderGrafici + os.path.sep + testName + u"_" + tipo + u".png"
        plt.savefig(filename, dpi=150, transparent=False)        
        
        #chiudo il plot
        plt.close ()
        
        
if __name__ == '__main__':
    a= Analizzatore ()#f)
    