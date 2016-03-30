# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 20:59:21 2016

@author: Patrizio
"""

try:
    import reportlab
except ImportError:
    raise ImportError,"The reportlab module is required to run this program\n  installarlo tramite -> pip install reportlab"
    
from reportlab.lib.enums import *

from reportlab.lib.pagesizes import A4

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, ParagraphAndImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


class CreaPdf():
    def __init__ (self):
        self.folderDati = "dati\\"
        self.folderGrafici = self.folderDati + "grafici\\"
        self.folderPdfs = self.folderDati + "pdfs\\"
        
        self.filenameLogoUni = self.folderDati + "res\\" + u"unitn.jpg"        

        self.filenameGraphDim =  u" DIMS.png"
        self.filenameGraphParams = u" PARAMS.png"
        
        
    def CreaPdfTest (self, testName, ValorMedioPrestazioniParams, ValorMedioPrestazioniDims, 
        MigliorRisultatoParams, MigliorRisultatoDims, PeggiorRisultatoParams, PeggiorRisultatoDims,
        ltestp, ltestd):
        
        #per prima cosa carico i grafici ottenuti

        graphParams = self.folderGrafici + testName + self.filenameGraphParams
        graphDims = self.folderGrafici + testName + self.filenameGraphDim
        
        #creo l'oggetto immagine dei grafici
        graphParams = Image(graphParams, 20*cm, 15*cm)
        graphDims = Image(graphDims, 20*cm, 15*cm)
        #carico le immagini standard
        imgLogoUni = Image(self.filenameLogoUni, 5*cm, 5*cm)
        
        #Inizo a creare il documento pdf
        testPdfFilename = self.folderPdfs + testName + u".pdf"
        
        doc = SimpleDocTemplate(testPdfFilename, pagesize=A4,
                                rightMargin=72,leftMargin=72,
                                topMargin=72,bottomMargin=18)
        documento = list ()
        
        documento.append(imgLogoUni)             
        documento.append(Spacer(1,17)) 
        
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_RIGHT))
        ptext = "TEST: %s"% testName
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext = "Risultati Ottenuti dai test:"
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,17))
        ptext = "Media prestazioni test sulla tipologia PARAMS : %f \n"% ValorMedioPrestazioniParams 
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext =  "Media prestazioni test sulla tipologia DIMS   : %f \n"%  ValorMedioPrestazioniDims
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7)) 
        ptext = "Miglior risultato \n"
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext = "Prestazione migliore test in condizioni %s sulla tipologia PARAMS %f: \n"% MigliorRisultatoParams
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext = "Prestazione migliore test in condizioni %s sulla tipologia DIMS   %f: \n"%  MigliorRisultatoDims
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext =  "peggior risultato \n"
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext =  "Prestazione peggiore test in condizioni %s sulla tipologia PARAMS %f: \n"%  PeggiorRisultatoParams
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext =  "Prestazione peggiore test in condizioni %s sulla tipologia DIMS   %f: \n"%  PeggiorRisultatoDims
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        
        
        if len(ltestp) > 0:
            ptext =  "parametri di costruzione corpus:"
            documento.append(Paragraph(ptext, styles["Normal"]))
            documento.append(Spacer(1,7))
            ptext =  "Risultati identici si ottengono anche parametrizzando il tokenizzatore con i seguenti parametri:"
            documento.append(Paragraph(ptext, styles["Normal"]))
            documento.append(Spacer(1,7))
            for ele in ltestp:
                if type(ltestp) == type(list()):
                    ptext =  "%s" % ele
                    documento.append(Paragraph(ptext, styles["Normal"]))
                    documento.append(Spacer(1,7))
                    
                elif type(ltestp) == type (dict()):
                    for e in ele.keys():
                        ptext =  "%s" % ele[e]
                        documento.append(Paragraph(ptext, styles["Normal"]))
                    documento.append(Spacer(1,7))
                    
        if len (ltestd) > 0:
            ptext =  "parametri dimensione corpus"
            documento.append(Paragraph(ptext, styles["Normal"]))
            documento.append(Spacer(1,7))
            ptext =  "Risultati identici si ottengono anche parametrizzando il tokenizzatore con i seguenti parametri:"
            documento.append(Paragraph(ptext, styles["Normal"]))
            documento.append(Spacer(1,7))
            for ele in ltestd:
                if type(ltestd) == type (list()):
                    ptext =  "%s" % ele
                    documento.append(Paragraph(ptext, styles["Normal"]))
                    documento.append(Spacer(1,7))
                        
                elif type(ltestd) == type (dict()):
                    for e in ele.keys():
                        ptext =  "%s" % ele[e]
                        documento.append(Paragraph(ptext, styles["Normal"]))
                    documento.append(Spacer(1,7))
                    
        ltestp, ltestd
        
        documento.append(graphParams)  
        styles=getSampleStyleSheet()
        
        documento.append(Spacer(1,7))
        
        documento.append(graphDims)  
        
        doc.build(documento)                    
                           
                                 
        
############################################################################  
    def CreaPdfBestTest (self, best):
        
        #carico le immagini standard
        imgLogoUni = Image(self.filenameLogoUni, 5*cm, 5*cm)
        
        #Inizo a creare il documento pdf
        testPdfFilename = self.folderPdfs + u"Best results" + u".pdf"
        
        doc = SimpleDocTemplate(testPdfFilename, pagesize=A4,
                                rightMargin=72,leftMargin=72,
                                topMargin=72,bottomMargin=18)
        documento = list ()
        
        documento.append(imgLogoUni)             
                
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_RIGHT))
        
        documento.append(Spacer(1,17))
        ptext = "TOKENIZZATORI CON I RISULTATI MIGLIORI"
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext = "Valore medio prestazioni"
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext = "Media prestazioni test sulla tipologia PARAMS : "
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        for i in best['valMedioParams']:
            ptext = "\nTest : %s \n Value : %f"%(i)
            documento.append(Paragraph(ptext, styles["Normal"]))
            documento.append(Spacer(1,7))
        ptext =  "Media prestazioni test sulla tipologia DIMS : "
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        for i in best['valMedioDms']:
            ptext =  "\nTest : %s \n Value : %f"%(i)
            documento.append(Paragraph(ptext, styles["Normal"]))
            documento.append(Spacer(1,7))
        ptext = "Miglior risultato"
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        ptext = "Prestazione migliore test sulla tipologia PARAMS :"
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        for i in best['BestParams']:
            #ptext = ptext + "\nTest : %s \n Value : %f"%(i)  
            ptext = "Test : %s \ncondizione %s Value : %f"%(i[0], i[1][0], i[1][1]) 
            documento.append(Paragraph(ptext, styles["Normal"]))
            documento.append(Spacer(1,7))
        ptext = "Prestazione migliore test sulla tipologia DIMS :"
        documento.append(Paragraph(ptext, styles["Normal"]))
        documento.append(Spacer(1,7))
        for i in best['BestDims']:
            #ptext = ptext + "\nTest : %s \n Value : %f"%(i) 
            ptext = "Test : %s \ncondizione %s Value : %f"%(i[0], i[1][0], i[1][1])  
            documento.append(Paragraph(ptext, styles["Normal"]))
            documento.append(Spacer(1,7))
        
        doc.build(documento)    
        

if __name__ == '__main__':
    a = CreaPdf()