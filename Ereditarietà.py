# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:34:22 2016

@author: Patrizio
"""

print "Esempio per illustrare l'ereditarietà "

#la classe di base deve essere ereditaria di object
class A (object):
    def __init__ (self):
        #definisco una proprietà
        self.proprieta = "Proprietà di A"
        print self.proprieta
        
        
class B (A):
    def __init__ (self):
        #inizializzo i dati ereditati tramite il metodo super
        # super (nome_classe, self).metodo_da_inizializzare
        super (B, self).__init__ ()
        
        #definisco una proprietà
        self.proprieta = "Proprietà di B"
        print self.proprieta
        
        
class C (B):
    def __init__ (self):
        super (C, self).__init__ ()
        #definisco una proprietà
        self.proprieta = "Proprietà di C"
        print self.proprieta
        
        
class D (C):
    def __init__ (self):
        super (D, self).__init__ ()
        #definisco una proprietà
        self.proprieta = "Proprietà di D"
        print self.proprieta
        
        
class E (D):
    def __init__ (self):
        super (E, self).__init__ ()
        #definisco una proprietà
        self.proprieta = "Proprietà di E"
        print self.proprieta
        
#creo l'oggetto di tipo E        
var = E()

print 
print var.proprieta
print
print "in python posso avere anche l'ereditarietà multipla, ossia posso ereditare da più classi"
print

class A (object):
    def __init__ (self):
        self.proprieta_di_A = "proprietà di A"
    def metodoA (self):
        print "Metodo di A"

class B (object):
    def metodoB (self):
        print "Metodo di B"
                
        
class C (A, B):
    def __init__ (self):
        super (C, self).__init__ ()
        #definisco una proprietà
        self.proprieta = "Proprietà di C"
        print self.proprieta
        
var = C ()
print 
var.metodoA ()
var.metodoB ()
print
print var.proprieta_di_A    
print 
print "se avessi avuto ..."
print

class A (object):
    def __init__ (self):
        self.proprieta = "proprietà di A"

class B (object):
    def __init__ (self):
        self.proprieta = "proprietà di B"

class C (A, B):
    def __init__ (self):
        super (C, self).__init__ ()

varC = C ()
print
print var.proprieta
print 
print "ora cambio l'ordine di ereditarietà"

class D (B, A):
    def __init__ (self):
        super (D, self).__init__ ()

varD = D ()
print
print var.proprieta
print 
print "per conoscere l'ordine di ereditarietà devo leggere l'attributo __class__.__mro__"
print 
print "mro di C"
print varC.__class__.__mro__
print
print "mro di D"
print varD.__class__.__mro__
print
print "posso anche decidere di estendere un metodo di classe"
print

class A (object):
    def foo (self):
        return "foo di A"

class B (A):
    def foo (self):
        var = super (B, self).foo ()
        var = var + " e poi continuo con il foo di B"
        return var

class C (B):
    def foo (self):
        return super (C, self).foo () + " e finisco con il foo di C"
         

a = A ()
print a.foo ()       
print
b = B ()
print b.foo ()
print
c = C ()
print c.foo ()      
print        
