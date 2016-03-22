# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 20:59:21 2016

@author: Patrizio
"""

try:
    import reportlab
except ImportError:
    raise ImportError,"The reportlab module is required to run this program\n  installarlo tramite -> pip install reportlab"
    
import collections
    
#da sistemare 
import time
from reportlab.lib.enums import *
#TA_JUSTIFY
#TA_CENTER 
#TA_RIGHT 
#TA_JUSTIFY 

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
        MigliorRisultatoParams, MigliorRisultatoDims, PeggiorRisultatoParams, PeggiorRisultatoDims):
        
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#    def TestPaginaPdf (self):  
#        doc = SimpleDocTemplate("test.pdf",pagesize=A4,
#                                rightMargin=72,leftMargin=72,
#                                topMargin=72,bottomMargin=18)
#        documento = list ()
#            
#        grafico = "STANDARD WORD TOKENIZER.png"
#        im = Image(grafico, 20*cm, 15*cm)
#        documento.append(im)             
#                
#        styles=getSampleStyleSheet()
#        styles.add(ParagraphStyle(name='Justify', alignment=TA_RIGHT))
#        ptext = '<font size=15>%s</font>' % "PROVA allineamento a destra"
#        documento.append(Paragraph(ptext, styles["Normal"]))
#        documento.append(Spacer(1,32))
#          
#
#
#        styles=getSampleStyleSheet()
#        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))                       
#        ptext = '<font size=12>Ima Sucker</font>'
#        documento.append(Paragraph(ptext, styles["Normal"]))
#        documento.append(Spacer(1, 12))
#        doc.build(documento)                    
#                           
#                           
#                           
#                           
##  class ParagraphStyle(PropertySet):
##    defaults = {
##        'fontName':_baseFontName,
##        'fontSize':10,
##        'leading':12,
##        'leftIndent':0,
##        'rightIndent':0,
##        'firstLineIndent':0,
##        'alignment':TA_LEFT,
##        'spaceBefore':0,
##        'spaceAfter':0,
##        'bulletFontName':_baseFontName,
##        'bulletFontSize':10,
##        'bulletIndent':0,
##        #'bulletColor':black,
##        'textColor': black,
##        'backColor':None,
##        'wordWrap':None,        #None means do nothing special
##                                #CJK use Chinese Line breaking
##                                #LTR RTL use left to right / right to left
##                                #with support from pyfribi2 if available
##        'borderWidth': 0,
##        'borderPadding': 0,
##        'borderColor': None,
##        'borderRadius': None,
##        'allowWidows': 1,
##        'allowOrphans': 0,
##        'textTransform':None,   #uppercase lowercase (captitalize not yet) or None or absent
##        'endDots':None,         #dots on the last line of left/right justified paras
##                                #string or object with text and optional fontName, fontSize, textColor & backColor
##                                #dy
##        'splitLongWords':1,     #make best efforts to split long words
##        'underlineProportion': _baseUnderlineProportion,    #set to non-zero to get proportional
##        'bulletAnchor': 'start',    #where the bullet is anchored ie start, middle, end or numeric
##        'justifyLastLine': 0,   #n allow justification on the last line for more than n words 0 means don't bother
##        'justifyBreaks': 0,     #justify lines broken with <br/>
##        }
#                         
#                           
#                           
#                           
##                           
##    def CreaPaginaPdfGrafico (self, pdfPageName = "pagina.pdf"):
##        doc = SimpleDocTemplate("test.pdf",pagesize=A4,
##                                rightMargin=72,leftMargin=72,
##                                topMargin=72,bottomMargin=18)
##                                
##        Story=[]
##        
##        logoUnitn = "unitn.jpg"
##        
##        magName = "Pythonista"
##        issueNum = 12
##        subPrice = "99.00"
##        limitedDate = "03/05/2010"
##        freeGift = "tin foil hat"
##         
##        formatted_time = time.ctime()
##        full_name = "Mike Driscoll"
##        address_parts = ["411 State St.", "Marshalltown, IA 50158"]
##
#                           
##        #da qui 
##        im = Image(logoUnitn, 5*cm, 5*cm)
##        Story.append(im)
##         
##        styles=getSampleStyleSheet()
##        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
##        ptext = '<font size=12>%s</font>' % formatted_time
##        Story.append(Paragraph(ptext, styles["Normal"]))
##        Story.append(Spacer(1, 12))
##         
##        grafico = "STANDARD WORD TOKENIZER.png"
##        im = Image(grafico, 20*cm, 15*cm)
##        Story.append(im) 
##         
#    
##         
##        # Create return address
##        ptext = '<font size=12>%s</font>' % full_name
##        Story.append(Paragraph(ptext, styles["Normal"]))       
##        for part in address_parts:
##            ptext = '<font size=12>%s</font>' % part.strip()
##            Story.append(Paragraph(ptext, styles["Normal"]))   
##         
##        Story.append(Spacer(1, 12))
##        ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
##        Story.append(Paragraph(ptext, styles["Normal"]))
##        Story.append(Spacer(1, 12))
##         
##        ptext = '<font size=12>We would like to welcome you to our subscriber base for %s Magazine! \
##                You will receive %s issues at the excellent introductory price of $%s. Please respond by\
##                %s to start receiving your subscription and get the following free gift: %s.</font>' % (magName, 
##                                                                                                        issueNum,
##                                                                                                        subPrice,
##                                                                                                        limitedDate,
##                                                                                                        freeGift)
##        Story.append(Paragraph(ptext, styles["Justify"]))
##        Story.append(Spacer(1, 12))
##         
##         
##        ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
##        Story.append(Paragraph(ptext, styles["Justify"]))
##        Story.append(Spacer(1, 12))
##        ptext = '<font size=12>Sincerely,</font>'
##        Story.append(Paragraph(ptext, styles["Normal"]))
##        Story.append(Spacer(1, 48))
##        ptext = '<font size=12>Ima Sucker</font>'
##        Story.append(Paragraph(ptext, styles["Normal"]))
##        Story.append(Spacer(1, 12))
#        doc.build(Story)

if __name__ == '__main__':
    a = CreaPdf()