#!/usr/bin/env python

from decimal import Decimal
from functools import partial

def maxt(b,c):
    """
    b and c are integer tuples of the same length. I return a new
    tuple d such that d[i] is max(b[i],c[i]).
    """
    return tuple(map(max,zip(b,c)))

def spacer(widths):
    def _spacer():
        yield '%s'
        i = 0
        while i < len(widths[1:]):
            yield ' '*widths[i+1]
            i += 1
            yield '%s'
            i += 1
    return ''.join(_spacer())
        
def span(title,widths):
    # Title is the length of the title string
    # Widths is a list of field lengths.
    
    # For example, [5,3,7] represents 3 fields of length 5, 3 and 7.
    
    # Normally, fields are displayed with a single space separating
    # them, so the display format would be [5,1,3,1,7]. Again, I just
    # show the lengths of the fields, and not their text.
    
    # Sum([5,1,3,1,7]) = 17. if 17 >= title, the normal case holds. The
    # title will not display longer than the fields (when composed as a
    # print line). If title > 17, I need to add extra space between
    # the fields.
    assert len(widths) > 0
    if len(widths) == 1:
        return widths # no gaps to space
    def adjust(n,r):
        yield widths[0]
        for i in widths[1:]:
            if r > 0:
                yield n+1
                r -= 1
            else:
                yield n
            yield i
    if title > sum(widths):
        excess = title-sum(widths)
        gaps = len(widths)-1
        n,r = divmod(excess,gaps)
        return list(adjust(n,r))
    else:
        return list(adjust(1,0))

def papply(functions,values):
    return tuple(f(n) for f,n in zip(functions,values))

def display(rows,headings,title=''):
    if len(rows) == 0:
        if title:
            m = max(len(s) for s in ('<empty>',title))
            yield title.center(m)
            yield '='*m
        yield '<empty>'
        return
    widths = reduce(maxt,[[len(str(a)) for a in b] for b in rows]) # body
    widths = maxt(widths,[len(n) for n in headings]) # and header
    template = tuple(partial(lambda s,w: str(s).ljust(w),w=w) for w in widths)
    def gen_fields():
        yield papply(template,headings)
        yield tuple('-'*i for i in widths)
        for row in rows:
            yield papply(template,row)
    spacing = spacer(span(len(title),widths))
    fields = gen_fields()
    line = fields.next()
    first = spacing % line
    if title:
        yield title.center(len(first))
        yield '='*len(first)
    yield first
    for line in fields:
        yield spacing % line

def demo():
    #     Price List 
    #   =============
    #   item    price
    #   ------- -----
    #   apple   0.10 
    #   peach   0.12 
    #   avocado 1.00 
    headings = ('item','price')
    r0 = ('apple','0.10')
    r1 = ('peach','0.12')
    r2 = ('avocado','1.00')
    rows = [r0,r1,r2]
    for line in display(rows,headings,'Price List'):
        print line

if __name__ == '__main__':
    demo()



