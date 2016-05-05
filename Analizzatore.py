# -*- coding: utf-8 -*-
"""
Created on Thu May 05 18:38:36 2016

@author: Patrizio
"""

from AnalizzatoreGrafici import AnalizzatoreGrafici
from AnalizzatorePDF import AnalizzatorePDF

class Analizzatore (AnalizzatoreGrafici, AnalizzatorePDF):
    def __init__ (self):
        super (Analizzatore, self).__init__()
        self.AvviaCreazioneGrafici ()
        self.AvviaCreazionePdf ()
        
if __name__ == '__main__':
    a= Analizzatore ()#f)
            