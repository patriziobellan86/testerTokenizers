# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 16:18:38 2016

@author: Patrizio
"""

from Tools import Tools

import re
import glob

class Abbreviazione ():
    r"""
        Questa classe si occupa di trovare e registrare le abbreviazioni 
        da utilizzare nella fase di addestramento del punkt tokenizer
    """
    def VERSION (self):
        return u"vers.0.1.c"
        
        
    def __init__ (self, dimSampPaisa = -1):
        self.fileExtAbbr = u".abl"
        self.folderDati = u"dati\\"
        self.folderCorpus="corpus\\"
        self.fileMorphIt = self.folderDati + u"morphit.utf8.txt"
        self.ABBR = u"SA"
        self.tools = Tools ()
        
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
        files = glob.glob (self.folderCorpus + u'*')        
                
        if type(dim) == type(int()):
            dim = list(dim)
        if type(dim) == type (list()):
            _ = list ()            
            for ele in dim:
                if ele == -1:
                    ele = len (files)
                _.append (ele)
            dim = _
            dim.sort ()

        i = 0   #indice di scorrimento nel campione
        j = float(0)   #indice di scorrimento dei files - uso float per evitare overflow
        
        for file in files:
            for line in self.tools.LoadFile(file):
                line = line.split (u"\t")
                if line[4] == self.ABBR:
                    abbrs.add (line[1])
            if dim[i] == j:
                filename = unicode(str(dim[i])) + u"_" + u"paisa"
                self.SaveAbbrFile (filename, list(abbrs))
                i += 1
            j += 1
        filename = unicode(str(dim[i])) + u"_" + u"paisa"
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
        for line in self.tools.LoadFile(self.fileMorphIt):
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
        self.tools.SaveByte (dati = abbrs, filename = filename)
       
def Test ():
    numSamplesPaisa = [-1]
    Abbreviazione (numSamplesPaisa)
    print "fine"
       
if __name__ == '__main__':
    Test ()