#! /usr/bin/env python

import unittest

import functools
import sys
sys.path.insert(0,'../')
from relbis.relD import (Relation,Header,DEE,DUM)
from relbis.TupleSet import TupleSet
from relbis.Tuple import Tuple

R = Relation(
    Header(a=int,b=int,c=int),
    Tuple(a=2,b=2,c=0),
    Tuple(a=2,b=3,c=1),
    Tuple(a=3,b=2,c=2),
    Tuple(a=9,b=2,c=3),
    Tuple(a=9,b=4,c=4))

Rc = Relation.create(('a','b','c'),
                     (int,int,int),
                     [(2,2,0),
                      (2,3,1),
                      (3,2,2),
                      (9,2,3),
                      (9,4,4)])

M = Relation(
    Header(a=int,b=int,c=int),
    Tuple(a=2,b=2,c=0),
    Tuple(a=2,b=3,c=1),
    Tuple(a=3,b=2,c=2))

A = Relation(
    Header(a=int,b=int,c=int),
    Tuple(a=2,b=2,c=0),
    Tuple(a=2,b=3,c=1))

B = Relation(
    Header(a=int,b=int,c=int),
    Tuple(a=2,b=3,c=1),
    Tuple(a=3,b=2,c=2))

I = Relation(
    Header(a=int,b=int,c=int),
    Tuple(a=2,b=2,c=0))

J = Relation(
    Header(a=int,b=int,c=int),
    Tuple(a=2,b=3,c=1))

K = Relation(
    Header(a=int,b=int,c=int),
    Tuple(a=3,b=2,c=2))

class test_relation(unittest.TestCase):
    
    def test_create(self):
        self.failUnless(R == Rc)
        I = Relation(Header(a=int,b=int,c=int),Tuple(a=2,b=2,c=0))
        Ic = Relation.create(('a','b','c'),(int,int,int),[(2,2,0)])
        DEE = Relation(Header(),Tuple())
        DEEc = Relation.create((),(),[()])
        self.failUnless(DEE == DEEc)
        DUM = Relation(Header())
        DUMc = Relation.create((),(),[])
        self.failUnless(DUM == DUMc)
        self.failUnless(I == Ic)
        self.failUnless(Relation.create(R.names,R.types,R.rows) == R)
        # crazy:
        header = Header(**dict(zip(R.names,R.types)))
        rows = list(Tuple(**dict(zip(R.names,t))) for t in R.rows)
        self.failUnless(Relation(header,*rows) == R)

    def test_count(self):
        self.failUnless(Relation(Header()).count == 0)
        self.failUnless(Relation(Header(a=str)).count == 0)
        self.failUnless(
            Relation(
                Header(a=str),
                Tuple(a='aaa')).count == 1)
        self.failUnless(
            Relation(
                Header(a=str,b=int),
                Tuple(a='aaa',b=123),
                Tuple(a='ccc',b=456)).count == 2)

    def test_names(self):
        # names is a sorted tuple with no dups.
        self.failUnless(Relation(Header()).names == ())
        self.failUnless(Relation(Header(),Tuple()).names == ())
        self.failUnless(Relation(Header(a=int)).names == ('a',))
        self.assertEqual(
            Relation(Header(c=int,b=str,a=float)).names,
            ('a','b','c'))
        self.assertEqual(
            Relation(Header(c=int,b=str,a=float),
                     Tuple(c=123,b="abc",a=1.0)).names,
            ('a','b','c'))
        
    def test_restrict(self):
        C = R.restrict(lambda row: row.c == 1)
        NC = R.restrict(lambda row: row.c != 1)
        self.failUnless(C.union(NC) == R)        
        self.failUnless(R.restrict(lambda row: True) == R)
        self.assertEqual(
            R.restrict(lambda row: False),
            Relation(Header(a=int,b=int,c=int)))
        self.assertEqual(
            R.restrict(lambda row: row.a == row.b),
            R.restrict(lambda row: row.c == 0))
        
    def test_rename(self):
        X = Relation(
            Header(x=int,b=int,c=int),
            Tuple(x=2,b=2,c=0),
            Tuple(x=2,b=3,c=1),
            Tuple(x=3,b=2,c=2),
            Tuple(x=9,b=2,c=3),
            Tuple(x=9,b=4,c=4))
        XY = Relation(
            Header(x=int,y=int,c=int),
            Tuple(x=2,y=2,c=0),
            Tuple(x=2,y=3,c=1),
            Tuple(x=3,y=2,c=2),
            Tuple(x=9,y=2,c=3),
            Tuple(x=9,y=4,c=4))
        AB = Relation(
            Header(b=int,a=int,c=int),
            Tuple(b=2,a=2,c=0),
            Tuple(b=2,a=3,c=1),
            Tuple(b=3,a=2,c=2),
            Tuple(b=9,a=2,c=3),
            Tuple(b=9,a=4,c=4))
        self.failUnless(R.rename(a='a') == R)
        self.failUnless(R.rename(a='x') == X)
        self.failUnless(R.rename(a='x',b='y') == XY)
        self.failUnless(R.rename(a='b',b='a') == AB)
    
    def test_union(self):
        N = Relation(Header())
        self.assertEqual(Relation(Header()).union(Relation(Header())),
                         Relation(Header()))
        E = Relation(Header(a=int,b=int,c=int))
        self.failUnless(E.union(E) == E)
        self.failUnless(R.union(R) == R)
        self.failUnless(R.union(E) == R)
        self.failUnless(E.union(R) == R)
        self.failUnless(A.union(B) == M)
        self.failUnless(B.union(A) == A.union(B))
        self.failUnless(B.union(M) == M)
        self.failUnless(M.union(B) == M)
        self.failIf(M.union(B) == B)
        with self.assertRaises(TypeError): 
            E.union(N)
        u = lambda x,y: x.union(y)
        self.failUnless(reduce(u,[I,J,K],E) == M)

    def test_intersect(self):
        N = Relation(Header())
        self.assertEqual(Relation(Header()).intersect(Relation(Header())),
                         Relation(Header()))
        E = Relation(Header(a=int,b=int,c=int))
        self.failUnless(E.intersect(E) == E)
        self.failUnless(R.intersect(R) == R)
        self.failUnless(R.intersect(E) == E)
        self.failUnless(E.intersect(R) == E)
        self.failUnless(A.intersect(B) == J)
        self.failUnless(B.intersect(A) == A.intersect(B))
        self.failUnless(B.intersect(M) == B)
        self.failUnless(M.intersect(B) == B)
        self.failIf(M.intersect(B) == M)
        with self.assertRaises(TypeError): 
            E.intersect(N)
        i = lambda x,y: x.intersect(y)
        self.failUnless(reduce(i,[I,J,K]) == E)
        self.failUnless(reduce(i,[I,J,K],M) == E)

    def test_set_relation(self):
        rf = functools.partial(Relation.create,('a','b','c'),(int,int,int))
        r1 = rf([(2,2,0),(2,3,1),(3,2,2)])
        self.failUnless(rf([(2,2,0),(2,3,1),(3,2,2)]) == rf([(2,2,0),(2,3,1),(3,2,2)]))
        self.failUnless(rf([(2,2,0),(2,3,1),(3,2,2)]) <= rf([(2,2,0),(2,3,1),(3,2,2)]))
        self.failIf(rf([(2,2,0),(2,3,1),(3,2,2)]) != rf([(2,2,0),(2,3,1),(3,2,2)]))

        self.failUnless(rf([(2,2,0),(2,3,1)]) != rf([(2,2,0),(2,3,1),(3,2,2)]))
        self.failUnless(rf([(2,2,0),(2,3,1)]) <= rf([(2,2,0),(2,3,1),(3,2,2)]))
        self.failUnless(rf([(2,2,0),(2,3,1)]) < rf([(2,2,0),(2,3,1),(3,2,2)]))

        self.failIf(rf([(2,2,0),(2,3,1)]) == rf([(2,2,0),(2,3,1),(3,2,2)]))
        self.failIf(rf([(2,2,0),(2,3,1)]) > rf([(2,2,0),(2,3,1),(3,2,2)]))
        self.failIf(rf([(2,2,0),(2,3,1)]) >= rf([(2,2,0),(2,3,1),(3,2,2)]))
        
        self.failUnless(rf([]) != rf([(2,2,0),(2,3,1),(3,2,2)]))
        self.failUnless(rf([]) < rf([(2,2,0),(2,3,1),(3,2,2)]))
        self.failUnless(rf([]) <= rf([(2,2,0),(2,3,1),(3,2,2)]))

    def test_difference(self):
        rf = functools.partial(Relation.create,('a','b','c'),(int,int,int))
        r = rf([(2,2,0),(2,3,1),(3,2,2)])
        s = rf([(2,2,0),(7,3,1),(3,2,2)])
        e = rf([])
        self.failUnless(r.difference(r) == e) 
        self.failUnless(r.difference(e) == r) 
        self.failUnless(e.difference(e) == e) 
        self.failUnless(e.difference(r) == e) 
        self.failUnless(r.difference(s) == rf([(2,3,1)]))
        self.failUnless(s.difference(r) == rf([(7,3,1)]))

    def test_cross(self):
        rfa = functools.partial(Relation.create,('a',),(int,))
        rfb = functools.partial(Relation.create,('b',),(int,))
        ra = rfa([(0,),(1,),(2,)])
        rb = rfb([(5,),(6,),(7,)])
        self.failUnless(ra.cross(rb) == rb.cross(ra))
        # print ra.cross(rfb([])) # empty yes, but "a b" col names?

    def test_join(self):
        A = Relation(
            Header(a=int,cx=int),
            Tuple(a=2,cx=0),
            Tuple(a=2,cx=1),
            Tuple(a=3,cx=2),
            Tuple(a=7,cx=3),
            Tuple(a=9,cx=4))
        B = Relation(
            Header(a=int,cy=int),
            Tuple(a=2,cy=5),
            Tuple(a=8,cy=6),
            Tuple(a=3,cy=7),
            Tuple(a=9,cy=8),
            Tuple(a=9,cy=9))
        self.assertEqual(A.join(A),A)
        self.assertEqual(A.join(B),B.join(A))

    def test_sum(self):
        self.failUnless(R.sum(lambda r:r.c) == 10)
        self.assertEqual(R.restrict(lambda _:False).sum(lambda r:r.c),0)
        self.failUnless(R.ave(lambda r:r.c) == 2)
        self.failUnless(R.min(lambda r:r.c) == 0)
        self.failUnless(R.max(lambda r:r.c) == 4)
        # E1 = Relation(Header(),Tuple())
        E = Relation(Header(b=bool))
        T = Relation(Header(b=bool),Tuple(b=True))
        F = Relation(Header(b=bool),Tuple(b=False))
        self.failUnless(E.all(lambda r:r.b) == True)
        self.failUnless(E.any(lambda r:r.b) == False)
        self.failUnless(T.all(lambda r:r.b) == True)
        self.failUnless(T.any(lambda r:r.b) == True)
        self.failUnless(F.all(lambda r:r.b) == False)
        self.failUnless(F.any(lambda r:r.b) == False)
        
    # def test_matching(self,other): pass
    # def test_not_matching(self,other): pass
    # def test_xunion(self,other): pass
    # def test_image(self,other): pass
    
    def test_extend(self):
        Hello = Relation(
            Header(a=int,b=int,c=int,greeting=str),
            Tuple(a=2,b=2,c=0,greeting="Hello, World!"),
            Tuple(a=2,b=3,c=1,greeting="Hello, World!"),
            Tuple(a=3,b=2,c=2,greeting="Hello, World!"),
            Tuple(a=9,b=2,c=3,greeting="Hello, World!"),
            Tuple(a=9,b=4,c=4,greeting="Hello, World!"))

        D = Relation(
            Header(a=int,b=int,c=int,d=int),
            Tuple(a=2,b=2,c=0,d=0),
            Tuple(a=2,b=3,c=1,d=10),
            Tuple(a=3,b=2,c=2,d=20),
            Tuple(a=9,b=2,c=3,d=30),
            Tuple(a=9,b=4,c=4,d=40))

        X = Relation(
            Header(a=int,b=int,c=int,d=int,e=int),
            Tuple(a=2,b=2,c=0,d=0,e=220),
            Tuple(a=3,b=2,c=2,d=20,e=322),
            Tuple(a=2,b=3,c=1,d=10,e=231),
            Tuple(a=9,b=2,c=3,d=30,e=923),
            Tuple(a=9,b=4,c=4,d=40,e=944))
        
        self.assertEqual(
            R.extend(greeting=(str,lambda _:"Hello, World!")),
            Hello)
        self.assertEqual(R.extend(d=(int,lambda r:r.c*10)),D)
        self.assertEqual(R.extend(
            d=(int,lambda r:r.c*10),
            e=(int,lambda r:r.a*100 + r.b*10 + r.c)),X)
        self.assertEqual(
            DEE.extend(x=(int,lambda _:27)),
            Relation(Header(x=int),Tuple(x=27)))

    def test_project(self):
        self.assertEqual(
            Relation(Header(a=int)).project().names,
            ())
        self.assertEqual(
            Relation(Header(a=int)).project('a').names,
            ('a',))
        self.assertEqual(
            Relation(Header(a=int,b=int)).project('a').names,
            ('a',))
        self.assertEqual(
            Relation(Header(b=int,a=int)).project('b','a').names,
            ('a','b'))

        R = Relation(
            Header(a=int,b=int),
            Tuple(a=2,b=2),
            Tuple(a=2,b=3),
            Tuple(a=3,b=2),
            Tuple(a=9,b=2))

        self.assertEqual(R.project('a').names,('a',))
        self.assertEqual(R.project('b').names,('b',))
        self.assertEqual(R.project('a','b').names,('a','b'))
        self.assertEqual(R.project('b','a').names,('a','b'))
        self.assertEqual(R.project('a').count,3)
        self.assertEqual(R.project('b').count,2)
        self.assertEqual(R.project('a','b'),R)        
        self.assertEqual(R.project(),Relation(Header()))

    def test_allbut(self):
        self.assertEqual(R.allbut('a').names,('b','c'))
        # print R.allbut('a')

    # def test_repr(self):
    #     print
    #     print repr(R)
    #     print str(R)
        
if __name__ == '__main__':
    unittest.main()
