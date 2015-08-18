#! /usr/bin/env python

import unittest

import sys
sys.path.insert(0,'../')
from relbis.Tuple import Tuple

class TestTuple(unittest.TestCase):

    def test_attribute(self):
        s1 = Tuple(sno='S1',sname='Smith',status=20)
        self.assertEqual(s1.sno,'S1')
        self.assertEqual(s1.sname,'Smith')
        self.assertEqual(s1.status,20)
        C = Tuple(x=2,y=5)
        self.failUnless(Tuple(x=C.x,y=C.y) == C)
        with self.assertRaises(AttributeError):
            Tuple(x=11).a

    def test_repr(self):
        self.assertEqual(
            repr(Tuple(sno='S1',sname='Smith',status=20)),
            "Tuple(sname='Smith',sno='S1',status=20)")

    def test_names(self):
        # names are sorted
        # no name dups
        s1 = Tuple(s='S1',n='Smith',t=20)
        self.assertEqual(s1.names,('n','s','t'))

    def test_equal(self):
        # transitive,symmetric,associative
        Tuple(s='01',n='S',t=20)
        self.assertEqual(Tuple(),
                         Tuple())
        self.assertEqual(Tuple(s='01'),
                         Tuple(s='01'))
        self.assertEqual(Tuple(s='01',n='S',t=20),
                         Tuple(s='01',n='S',t=20))
        self.assertEqual(Tuple(n='S',t=20,s='01'),
                         Tuple(s='01',n='S',t=20))
        self.failIf(Tuple() == Tuple(a=''))
        self.failIf(Tuple(s='01') == Tuple(t='01'))
        self.failIf(Tuple(s='01') == Tuple(s='02'))

    def test_not_equal(self):
        self.failUnless(Tuple() != Tuple(a=''))
        self.failUnless(Tuple(s='01') != Tuple(t='01'))
        self.failUnless(Tuple(s='01') != Tuple(s='02'))
        self.failUnless(Tuple(s='01') != Tuple(s='01',t='01'))

    def test_degree(self):
        self.failUnless(Tuple().degree == 0)
        self.failUnless(Tuple(a=11).degree == 1)
        self.failUnless(Tuple(a=11,b=22).degree == 2)

    def test_project(self):
        # idempotent
        self.failUnless(Tuple(b=22).project('b') == Tuple(b=22))
        self.failUnless(Tuple(a=11,b=22).project('b') == Tuple(b=22))
        with self.assertRaises(AttributeError):
            Tuple(a=11,b=22).project('c')
        with self.assertRaises(AttributeError):
            Tuple(a=11,b=22).project('c','d')
        with self.assertRaises(AttributeError):
            Tuple(a=11,b=22).project('a','d')
        with self.assertRaises(AttributeError):
            Tuple(a=11,b=22).project('a','b','c')
        self.assertEqual(
            Tuple(a=11,b=22,c=33).project('a','b').project('a'),
            Tuple(a=11,b=22,c=33).project('a','c').project('a'))
        self.failUnless(Tuple().project() == Tuple())
        self.failUnless(Tuple(b=22).project() == Tuple())
        self.assertEqual(
            Tuple(a=11,b=22,c=33).project('a','b','c'),
            Tuple(a=11,b=22,c=33))

    def test_or(self):
        self.failUnless(Tuple() | Tuple() == Tuple())
        self.failUnless(Tuple(b=22) | Tuple(b=22) == Tuple(b=22))
        self.assertEqual(
            Tuple(a=11) | Tuple(),
            Tuple(a=11))
        self.assertEqual(
            Tuple(a=11) | Tuple(b=22),
            Tuple(a=11,b=22))
        self.assertEqual(
            Tuple(a=11,b=22,c=33) | Tuple(b=22,d=44),
            Tuple(a=11,b=22,c=33,d=44))
        with self.assertRaises(TypeError):
            Tuple(b=22) | Tuple(b=99)
        with self.assertRaises(TypeError):
            Tuple(b=22) | Tuple(b='22')

    def test_rename(self):
        self.assertEqual(
            Tuple(a=11,b=22,c=33).rename(a='a'),
            Tuple(a=11,b=22,c=33))
        self.assertEqual(
            Tuple(a=11,b=22,c=33).rename(a='x'),
            Tuple(x=11,b=22,c=33))
        self.assertEqual(
            Tuple(a=11,b=22,c=33).rename(a='x',b='y',c='z'),
            Tuple(x=11,y=22,z=33))
        self.assertEqual(
            Tuple(a=11,b=22,c=33).rename(a='b',b='a'),
            Tuple(b=11,a=22,c=33))
        self.assertEqual(
            Tuple(a=11,b=22,c=33).rename(a='b',b='c',c='a'),
            Tuple(b=11,c=22,a=33))
        with self.assertRaises(AttributeError):
            Tuple(a=11,b=22,c=33).rename(x='w')
        with self.assertRaises(AttributeError):
            Tuple().rename(x='w')
        with self.assertRaises(TypeError):
            Tuple(a=11,b=22,c=33).rename(a='z',b='z')
        with self.assertRaises(TypeError):
            Tuple(a=11,b=22,c=33).rename(a='c')

    def test_extend(self):
        T = Tuple(a=11,b=22,c=33)
        self.assertEqual(
            T.extend(x=lambda t:t.a * 10),
            Tuple(a=11,b=22,c=33,x=110))
        self.assertEqual(
            T.extend(x=lambda t:t.a * 10,
                     y=lambda t:t.a * t.b + t.c,
                     z=lambda _:True),
            Tuple(a=11,b=22,c=33,x=110,y=275,z=True))

    def test_to_pytuple(self):
        self.failUnless(Tuple(a=11,b=22,c=33).to_pytuple() == (11,22,33))
        self.failUnless(Tuple().to_pytuple() == ())
        self.failUnless(Tuple(x='blue').to_pytuple() == ('blue',))
        
if __name__ == '__main__':
    unittest.main()
