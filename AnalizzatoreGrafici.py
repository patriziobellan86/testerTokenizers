# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:04:39 2016

@author: Patrizio
"""
from __future__ import division

from AnalizzatoreBase import AnalizzatoreBase

import collections
import numpy as np
import matplotlib.pyplot as plt
import os

#for d in [a,b]:
#    for k in d.keys():
#        c[k]=d[k]
#  
class AnalizzatoreGrafici (AnalizzatoreBase):
    r"""questa classe analizza tutti i dati dei tests"""
    
    def VERSION(self):
        return u"vers.0.3.1.b"
        
        
    def __init__(self):#, path, resultFilename=False):
        super (AnalizzatoreGrafici, self).__init__ ()
    
    
    def AvviaCreazioneGrafici (self):
        for key in self.risultati.keys():
            self.AnalizzatoreGrafici (key)
 
  
    #########################################################################
    def AnalizzatoreGrafici (self, key):
        #suddivido le due tipologie di test
        res = self.SuddividiTipiTest (key)
        
        print "Creazione Grafici per il test %s"%key
        
        #aggiungo i valori a self.test
        self.tests ['valMedioParams'].append ((key, self.ValorMedioPrestazioni (self.TIPO_PARAMS, res)))
        self.tests ['valMedioDms'].append ((key, self.ValorMedioPrestazioni (self.TIPO_DIMENS, res)))
        self.tests['BestParams'].append ((key, self.MigliorRisultato (self.TIPO_PARAMS, res)))
        self.tests['BestDims'].append ((key, self.MigliorRisultato (self.TIPO_DIMENS, res)))

        print "Creazione Grafico su parmas"
        self.GraficoParamas (key, res)
        
        print "Creazione grafico su dims"
        self.GraficoDims (key, res)


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

#        
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
           yValue = [round(float(ele[1]) * 100, 2) for ele in res[tipo]]

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
    