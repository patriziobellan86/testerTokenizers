# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:36:48 2016

@author: Patrizio
"""

class A (object):
    def __init__ (self):
        print "sono A"

    def F (self, n):
        self.n = n
        print "n in A è di %d" % self.n

class B (A):
    def __init__ (self, n):
        super (B, self).__init__()
        self.F (n)
    def F (self, n):
        self.n = n
        print "n in B è di %d" % self.n
        
v = B (5)
v.F (6)

class C (object):
    def __init__ (self):
        self.c = "questa è c"

class D (object):
    def __init__ (self):
        self.c = "questa è d"

class E (C, D):
    def __init__ (self):
        super (E, self).__init__()
        print self.c

j= E ()


class F (D, C):
    def __init__ (self):
        super (F, self).__init__()
        print self.c

g= F ()

print j.__class__.__mro__
print g.__class__.__mro__
