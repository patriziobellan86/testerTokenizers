# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 15:37:52 2016

@author: Patrizio
"""

from __future__ import unicode_literals

from Tools import Tools
import re
import os


class CreatorePatternRE(Tools):
    def VERSION (self):
        return "vers.0.3.c"
        
        
    def __init__(self):
#        self.folder = os.path.sep + 'mnt' + os.path.sep + '8tera' + os.path.sep + 'shareclic' + os.path.sep + 'lucaNgrams' + os.path.sep + 'Patrizio' + os.path.sep + 'testerTokenizers' + os.path.sep
#        self.folderDati = self.folder + u"dati" + os.path.sep
#
#        self.fileNameRe = self.folderDati + u"RegularExpression.tag"
        #Tools.__init__(self, 0)
        super (CreatorePatternRE, self).__init__(0)
        
        self.patterns = None
        
        self.CaricaPatterns ()
        self.Print ()
        
        
    def CaricaPatterns (self):
        self.patterns = self.LoadByte (self.fileNameRe)
        
        
    def Print (self):
        r"""
            questo metodo stampa a video i patterns registrati
        """
        if self.patterns:
            print "\nI patterns registrati sono:"        
            for i in self.patterns.keys():
                print i, self.patterns[i]
        else:
            self.patterns = dict ()
        
        
    def RegistraPattern (self, patternName, pattern, tipo):
        r"""
            Questo metodo registra un pattern nella variabile self.patterns
            e salva i risultati nel file
        """
        if tipo == self.WORD or tipo == self.SENT:
            print "Registrazione di key:",tuple([patternName, tipo]), "value:", pattern
            self.patterns[tuple([patternName, tipo])] = pattern
            self.Save()
        else:
            print "ERRORE TIPO, tipo", tipo, "non valido, impossibile procedere"
            print "type(tipo):", type(tipo) 
        
        
    def Save (self):
        r""" 
            questo metodo salva i dati sul file
        """
        self.SaveByte (dati = self.patterns, filename = self.fileNameRe)


    def InsertPattern (self):
        r""" 
            Questo metodo richiede i dati all'utente
        """
        
        flag=True
        try:
            while flag:
                print "\nregistrazione Pattern"
                patternName = raw_input ("nome             : ")
                pattern     = raw_input ("pattern          : ")
                patternTipo = input ("tipo 1. Word, 2.Sent : ")                
                self.RegistraPattern (patternName, pattern, patternTipo)
                flag = raw_input ("per uscire premi invio")
           
            self.Save ()
        except:
            pass
        
    
    def DelPattern (self):
        r"""
            Questo metodo cancella un pattern         
        """
        
        self.Print()
        print "\nCancella un pattern"
        
        keys = self.patterns.keys()
        for i, key in enumerate(keys):
            print i, key
        ind = raw_input ("inserisci l'indice da cancellare: ")
        del self.patterns[keys[int(ind)]]
        
        self.Save()
        print "\ni patterns ora sono:"        
        self.Print()
        
        
if __name__ == '__main__':
    a=CreatorePatternRE()
    a.InsertPattern ()

    
      
