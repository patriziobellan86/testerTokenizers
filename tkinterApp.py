# -*- coding: utf-8 -*-

"""
Created on Fri Mar 18 13:00:12 2016

@author: Patrizio
"""

from Tkinter import *

class Application:
    def __init__ (self, parent):
        
        self.parent = parent

        #Frame principale in cui si caricano gli altri frames        
        self.fbody =Frame (self.parent)        
        self.fbody.pack (fill = BOTH, expand = 1)

    def CreaMenu (self):
        pass
    
    #### GENREAL FUNCTION  ############
    def Esci (self):
        self.parent.destroy()

    
    ##################################
    
    
    #####   VIEW   ####################
    def MostraFrameImpostazioni (self):
        
        fImpostazioni = Frame (self.fbody)
        fImpostazioni.pack ()
        
    def MostraFrameTest (self):
        
        fTests = Frame (self.fbody)
        fTests.pack ()

        fTree = Frame (fTests)
        fTree.pack(side = LEFT, fill=X)
        
        fTest = Frame (fTests)
        fTest.pack(side = RIGHT, fill=Y)
    
    def MostraFrameDocumenti (self):
        
        fDocumenti = Frame (self.fbody)
        fDocumenti.pack ()

    ##################################

        
class MiaApp:
  def __init__(self, genitore):

    #--- costanti per il controllo della disposizione
    #--- dei pulsanti
    larghezza_pulsanti = 8
    imb_pulsantex = "2m"
    imb_pulsantey = "1m"
    imb_quadro_pulsantix = "3m"
    imb_quadro_pulsantiy = "2m"
    imb_int_quadro_pulsantix = "3m"
    imb_int_quadro_pulsantiy = "1m"
    #--------------------- fine costanti -----------------------

    # impostazione delle variabili di controllo Tkinter,
    # controllate dai pulsanti radio
    self.nome_pulsante = StringVar()
    self.nome_pulsante.set("C")

    self.opzione_lato = StringVar()
    self.opzione_lato.set(LEFT)

    self.opzione_riempimento = StringVar()
    self.opzione_riempimento.set(NONE)

    self.opzione_espansione = StringVar()
    self.opzione_espansione.set(YES)

    self.opzione_ancoraggio = StringVar()
    self.opzione_ancoraggio.set(CENTER)

    #---------------

    self.mioGenitore = genitore
    self.mioGenitore.geometry("640x400")

    ### Il quadro principale si chiama 'quadro_grande'
    self.quadro_grande = Frame(genitore) ###
    self.quadro_grande.pack(expand = YES, fill = BOTH)

    ### Viene usata l'orientazione ORIZZONTALE (da sinistra a
    ### destra) all'interno di 'quadro_grande'.
    ### Dentro 'quadro_grande' si creano 'quadro_controllo' e
    ### 'quadro_dimostrativo'.

    # 'quadro_controllo' - praticamente tutto tranne la
    # dimostrazione
    self.quadro_controllo = Frame(self.quadro_grande) ###
    self.quadro_controllo.pack(side = LEFT, expand = NO, padx = 10,
                               pady = 5, ipadx = 5, ipady = 5)

    # All'interno di 'quadro_controllo' si creano un'etichetta
    # per il titolo e un 'quadro_pulsanti'

    mioMessaggio = "Questa finestra illustra l'effetto \ndelle \
opzioni di impacchettamento \n 'expand', 'fill' e 'anchor'."
    Label(self.quadro_controllo,
      text = mioMessaggio,
      justify = LEFT).pack(side = TOP, anchor = W)

    # 'quadro_pulsanti'
    self.quadro_pulsanti = Frame(self.quadro_controllo)
    self.quadro_pulsanti.pack(side = TOP, expand = NO, fill = Y,
                              ipadx = 5, ipady = 5)

    # 'quadro_dimostrativo'
    self.quadro_dimostrativo = Frame(self.quadro_grande)
    self.quadro_dimostrativo.pack(side = RIGHT, expand = YES,
                                  fill = BOTH)

    ### Dentro 'quadro_dimostrativo' vengono creati
    ### 'quadro_alto' e 'quadro_basso'.
    ### Essi saranno i quadri della dimostrazione.
    # 'quadro_alto'
    self.quadro_alto = Frame(self.quadro_dimostrativo)
    self.quadro_alto.pack(side = TOP, expand = YES, fill = BOTH)

    # 'quadro_basso'
    self.quadro_basso = Frame(self.quadro_dimostrativo,
      borderwidth = 5,
      relief = RIDGE,
      height = 50,
      bg = "cyan",
      )
    self.quadro_basso.pack(side = TOP, fill = X)

    ### Vengono aggiunti altri due quadri, 'quadro_sx' e
    ### 'quadro_dx' all'interno di 'quadro_alto'. Si utilizza
    ### l'orientazione ORIZZONTALE (da sinistra a destra)
    ### dentro 'quadro_alto'.

    # 'quadro_sx'
    self.quadro_sx = Frame(self.quadro_alto,
      background = "red",
      borderwidth = 5,
      relief = RIDGE,
      width = 50
      ) 
    self.quadro_sx.pack(side = LEFT, expand = NO, fill = Y)

    # 'quadro_dx'
    self.quadro_dx = Frame(self.quadro_alto,
      background = "tan",
      borderwidth = 5,
      relief = RIDGE,
      width = 250
      )
    self.quadro_dx.pack(side = RIGHT, expand = YES, fill = BOTH)

    # Si pone un pulsante in ciascun quadro significativo
    nomi_pulsanti = ["A", "B", "C"]
    opzioni_lato = [LEFT, TOP, RIGHT, BOTTOM]
    opzioni_riempimento = [X, Y, BOTH, NONE]
    opzioni_espansione = [YES, NO]
    opzioni_ancoraggio = [NW, N, NE, E, SE, S, SW, W, CENTER]

    self.pulsanteA = Button(self.quadro_basso, text = "A")
    self.pulsanteA.pack()
    self.pulsanteB = Button(self.quadro_sx, text = "B")
    self.pulsanteB.pack()
    self.pulsanteC = Button(self.quadro_dx, text = "C")
    self.pulsanteC.pack()
    self.pulsante_con_nome = {"A": self.pulsanteA,
      "B": self.pulsanteB,
      "C": self.pulsanteC
      }

    # Si aggiungono alcuni sottoquadri a 'quadro_pulsanti'
    self.quadro_nomi_pulsanti = Frame(self.quadro_pulsanti,
                                      borderwidth = 5)
    self.quadro_opzioni_lato = Frame(self.quadro_pulsanti,
                                     borderwidth = 5)
    self.quadro_opzioni_riempimento = Frame(self.quadro_pulsanti,
                                            borderwidth = 5)
    self.quadro_opzioni_espansione = Frame(self.quadro_pulsanti,
                                           borderwidth = 5)
    self.quadro_opzioni_ancoraggio = Frame(self.quadro_pulsanti,
                                           borderwidth = 5)

    self.quadro_nomi_pulsanti.pack(side = LEFT, expand = YES,
                                   fill = Y, anchor = N)
    self.quadro_opzioni_lato.pack(side = LEFT, expand = YES,
                                  anchor = N)
    self.quadro_opzioni_riempimento.pack(side = LEFT, expand = YES,
                                         anchor = N)
    self.quadro_opzioni_espansione.pack(side = LEFT, expand = YES,
                                        anchor = N)
    self.quadro_opzioni_ancoraggio.pack(side = LEFT, expand = YES,
                                        anchor = N)

    Label(self.quadro_nomi_pulsanti,
      text = "\nPulsante").pack()
    Label(self.quadro_opzioni_lato,
      text = "Opzione\n'side'").pack()
    Label(self.quadro_opzioni_riempimento,
      text = "Opzione\n'fill'").pack()
    Label(self.quadro_opzioni_espansione,
      text = "Opzione\n'expand'").pack()
    Label(self.quadro_opzioni_ancoraggio,
      text = "Opzione\n'anchor'").pack()

    for opzione in nomi_pulsanti:
      pulsante = Radiobutton(self.quadro_nomi_pulsanti,
                             text = str(opzione),
                             indicatoron = 1,
                             value = opzione,
                             command = self.aggiorna_pulsante,
                             variable = self.nome_pulsante)
      pulsante["width"] = larghezza_pulsanti
      pulsante.pack(side = TOP)

    for opzione in opzioni_lato:
      pulsante = Radiobutton(self.quadro_opzioni_lato,
                             text = str(opzione),
                             indicatoron = 0, 
                             value = opzione, 
                             command = self.aggiorna_dimostrazione, 
                             variable = self.opzione_lato)
      pulsante["width"] = larghezza_pulsanti
      pulsante.pack(side = TOP)

    for opzione in opzioni_riempimento:
      pulsante = Radiobutton(self.quadro_opzioni_riempimento, 
                             text = str(opzione), 
                             indicatoron = 0, 
                             value = opzione, 
                             command = self.aggiorna_dimostrazione, 
                             variable = self.opzione_riempimento)
      pulsante["width"] = larghezza_pulsanti
      pulsante.pack(side = TOP)

    for opzione in opzioni_espansione:
      pulsante = Radiobutton(self.quadro_opzioni_espansione, 
                             text = str(opzione), 
                             indicatoron = 0, 
                             value = opzione, 
                             command = self.aggiorna_dimostrazione, 
                             variable = self.opzione_espansione)
      pulsante["width"] = larghezza_pulsanti
      pulsante.pack(side = TOP)

    for opzione in opzioni_ancoraggio:
      pulsante = Radiobutton(self.quadro_opzioni_ancoraggio, 
                             text = str(opzione), 
                             indicatoron = 0, 
                             value = opzione, 
                             command = self.aggiorna_dimostrazione, 
                             variable = self.opzione_ancoraggio)
      pulsante["width"] = larghezza_pulsanti
      pulsante.pack(side = TOP)

    self.quadroPulsanteAnnulla = Frame(self.quadro_nomi_pulsanti)
    self.quadroPulsanteAnnulla.pack(side = BOTTOM, 
                                    expand = YES, 
                                    anchor = SW)

    self.pulsanteAnnulla = Button(self.quadroPulsanteAnnulla,
                                  text = "Annulla", 
                                  background = "red", 
                                  width = larghezza_pulsanti, 
                                  padx = imb_pulsantex, 
                                  pady = imb_pulsantey)
    self.pulsanteAnnulla.pack(side = BOTTOM, anchor = S)

    self.pulsanteAnnulla.bind("<Button-1>", 
      self.pulsanteAnnullaPremuto)
    self.pulsanteAnnulla.bind("<Return>", 
      self.pulsanteAnnullaPremuto)

    # Si impostano i pulsanti nella posizione iniziale
    self.aggiorna_dimostrazione()

  def aggiorna_pulsante(self):
    pulsante = self.pulsante_con_nome[self.nome_pulsante.get()]
    proprieta = pulsante.pack_info()
    self.opzione_riempimento.set(proprieta["fill"])
    self.opzione_lato.set(proprieta["side"])
    self.opzione_espansione.set(proprieta["expand"])
    self.opzione_ancoraggio.set(proprieta["anchor"])

  def aggiorna_dimostrazione(self):
    pulsante = self.pulsante_con_nome[self.nome_pulsante.get()]
    pulsante.pack(fill = self.opzione_riempimento.get(), 
      side = self.opzione_lato.get(), 
      expand = self.opzione_espansione.get(), 
      anchor = self.opzione_ancoraggio.get()
      )

  def pulsanteAnnullaPremuto(self, evento):
      self.mioGenitore.destroy()


radice = Tk()
miaApp = MiaApp(radice)
radice.mainloop()