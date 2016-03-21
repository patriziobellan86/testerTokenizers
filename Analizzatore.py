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
from pdfTestCreator import CreaPdf

class Analizzatore:
    r"""questa classe analizza tutti i dati dei tests"""
    
    def VERSION(self):
        return u"vers.0.2.3.a"
        
        
    def __init__(self):
        self.folderTest = "test files\\" #cartella files dei risultati dei tests
        self.folderGrafici = "dati\\grafici\\"
        fileRisultati = self.folderTest + "results.pickle"
        self.tools = Tools (0) #strumenti vari
        
        self.risultati = self.tools.LoadByte (fileRisultati)
        self.TIPO_PARAMS = 'PARAMS'
        self.TIPO_DIMENS = 'DIMS'
        
        self.tests = collections.defaultdict (list)
        self.best = collections.defaultdict (list)
        self.AnalizzaDati()
 
        
    def AnalizzaDati (self):
        for k in self.risultati.keys():
            self.AnalizzaDato (k)
        self.EstraiMiglioriTok ()    
        
        
    def AnalizzaDato (self, key):
        
        #controllo se ha superato tutte le prove
        for test in self.risultati[key]:
            self.CreaDocumentazioneTest (key)
  
    #########################################################################
    def CreaDocumentazioneTest (self, key):
        #suddivido le due tipologie di test
        res = self.SuddividiTipiTest (key)
        
        print "Creazione documentazione per il test"
        
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
        
        
        attributi = self.risultati[key]['attributiTok']
        print "attributiTok", attributi
        
        
        print "Grafico su parmas"
        self.GraficoParamas (key, res, attributi)
        
        print "grafico su dims"
        self.GraficoDims (key, res)

        #creo il documento pdf del test
        self.CreaPaginaPdfTest (key, res, attributi)


    def EstraiMiglioriTok (self):
        #per ogni categoria estraggo il migliore
        
        best = 0
        blist = []
        for i in self.tests ['valMedioParams']:
            if i[1] > best[1]:
                best = i
                blist = [i]
            elif i[1] == best [1]:
                blist.append (i)
        self.best['valMedioParams'] = blist
        
        best = 0
        blist = []
        for i in self.tests ['valMedioDms']:
            if i[1] > best[1]:
                best = i
                blist = [i]
            elif i[1] == best [1]:
                blist.append (i)
        self.best['valMedioDms'] = blist
        
        best = 0
        blist = []
        for i in self.tests ['BestParams']:
            if i[1] > best[1]:
                best = i 
                blist = [i]
            elif i[1] == best [1]:
                blist.append (i)
        self.best['BestParams'] = blist
        
        best = 0
        blist = []
        for i in self.tests ['BestDims']:
            if i[1] > best[1]:
                best = i
                blist = [i]
            elif i[1] == best [1]:
                blist.append (i)
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
            print "Test : %s \n Value : %f"%(i)  
            
        print "Prestazione migliore test sulla tipologia DIMS :"
        for i in self.best['BestDims']:
            print "Test : %s \n Value : %f"%(i)  
          
        self.CreaDocumentazioneBestTest ()
        
        
    def CreaDocumentazioneBestTest(self):
        print "crea documentazione best test da controllare bene"        
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
        
        
    def GraficoParamas (self, testName, res, attributi):
        self.Plot(testName, self.TIPO_PARAMS, res, attributi)
            
            
    def GraficoDims (self, testName, res):
        self.Plot(testName, self.TIPO_DIMENS, res, attributi)
        
        
    def CreaPaginaPdfTest (self, key, res):
        print "crea pagina pdf Controllare"
        CreaPdf ().CreaPdfTest (key, 
            self.ValorMedioPrestazioni (self.TIPO_PARAMS, res),
            self.ValorMedioPrestazioni (self.TIPO_DIMENS, res),  
            self.MigliorRisultato (self.TIPO_PARAMS, res), 
            self.MigliorRisultato (self.TIPO_DIMENS, res), 
            self.PeggiorRisultato (self.TIPO_PARAMS, res), 
            self.PeggiorRisultato (self.TIPO_DIMENS, res))
        
    
# TODO BENE BENE    
    def Plot(self, testName, tipo, res, attributi):
        r"""
            Questa funzione plotta i dati
            
        """
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                        '%d' % int(height),
                        ha='center', va='bottom')
                        
        if not attributi:
            attributi = u""
            
        self.xLabel =  [ele[0] for ele in res[tipo]]
        self.yValue =  [ele[1] for ele in res[tipo]]
        
        N = len (self.xLabel)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars 

        valoriY = tuple (self.yValue)
        
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, valoriY, width, color='r')
        
        ax.set_ylabel('Scores')
        ax.set_xlabel('Tipo ricostruzione frase')
        ax.set_title('test scores')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(tuple(self.xLabel), rotation=90)#rotation ='vertical')

        autolabel(rects1)

        plt.title(testName + attributi)

# NEW        
        try:
            mean = sum(self.yValue) / len(self.yValue)
        except ZeroDivisionError:
            mean = 0
            
            
        x_points = xrange(0,len(self.xLabel))
        y_points = np.array([mean]*len(self.yValue))
        p = ax.plot(x_points, y_points, 'g')
        
        plt.tight_layout(pad=1)
#        plt.show()
        
        
        filename = self.folderGrafici + testName + u" " + tipo + u".png"
        plt.savefig(filename, dpi=150, transparent=False)        
        
        plt.close ()
        
if __name__ == '__main__':
    a= Analizzatore ()
    