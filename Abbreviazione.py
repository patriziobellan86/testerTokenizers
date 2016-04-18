# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 16:18:38 2016

@author: Patrizio
"""

from Tools import Tools

import re
import glob
import os


class Abbreviazione (Tools):
    r"""
        Questa classe si occupa di trovare e registrare le abbreviazioni 
        da utilizzare nella fase di addestramento del punkt tokenizer
    """
    def VERSION (self):
        return u"vers.3.8.b"
        
        
    def __init__ (self, dimSampPaisa = -1):
        Tools.__init__ (self, -1)
        
#        self.folder = os.path.sep + 'mnt' + os.path.sep + '8tera' + os.path.sep + 'shareclic' + os.path.sep + 'lucaNgrams' + os.path.sep + 'Patrizio' + os.path.sep + 'testerTokenizers' + os.path.sep
#        self.fileExtAbbr = '.abl'
#        self.folderDati = self.folder + 'dati' + os.path.sep
#        self.folderCorpus = self.folder + 'corpus' + os.path.sep
#
#        self.morphItFileName = self.folderDati + u"morphit.utf8.txt"

        self.ABBR = u"SA"
        
        
        self.RegistraDaPaisa (dimSampPaisa)
        self.RegistraDaMorphIt ()
    
    
    def RegistraDaPaisa (self, dim = -1):
        r"""
            Questo metodo ricerca e registra le abbreviazioni dal corpus paisa            
            
            il parametro dim, se è un intero rappresenta quanti file utilizzare
            se è pari a -1 utilizza tutto il campione
            se è una lista, è la lista contenente il numero di files da utilizzare
            per creare i files di abbreaviazione
            
            questo è stato fatto per poter effettuare prove differenti
        """
        abbrs = set ()
        #ciclo su tutte le frasi
        files = glob.glob (self.folderCorpus + u'*.*')        
        if dim != -1:
            files = files[:dim]

        for file in files:
            lines = self.LoadFile(file)
            for line in lines:
                line = line.split (u"\t")
                if line[4] == self.ABBR:
                    abbrs.add (line[1])

        filename = u"paisa"
        self.SaveAbbrFile (filename, abbrs)
                
                    
    def RegistraDaMorphIt (self):
        r"""
            Questo metodo ricerca e registra le abbreviazioni da Morphit
        """
        
        abbrs = set ()
        
        #Creo il pattern di ricerca
        pattern_abl = r'^ABL+'   #r'^ABL+'
        pat_abl = re.compile(pattern_abl)

        #Leggo morphIt  
        print self.morphItFileName 
        for line in self.LoadFile(self.morphItFileName):
            line = line.split ()
            if len(line) == 3:
                match=re.match(pat_abl, line[2])     
                if match:                    
                    abbrs.add (line[0])    
   
        #salvo le abbreviazioni   
        self.SaveAbbrFile (u'morhpit', list(abbrs))
        

    def SaveAbbrFile (self, filename, abbrs):
        r"""
            Questo metodo salva il file delle abbreviazioni
        """
        filename = self.folderDati + filename + self.fileExtAbbr
        self.SaveByte (dati = abbrs, filename = filename)
       
def Test ():
    numSamplesPaisa = -1
    Abbreviazione (numSamplesPaisa)
    print "fine"
       
if __name__ == '__main__':
    Test ()
