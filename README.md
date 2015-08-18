## Goals

* Write a clear description of the design and implementation
* Write RDB queries in the style of Tutorial D
* Provide a testsuite

Relbis is *not* a serious attempt to implement a relation data system.
It is for play and practice.

## Versions

### relbis-0.0.3
Mostly working library modules. Testsuite is provided. There is little
documentation as yet. Look for it in the next release.

## ToDo

* Document

## Design

A tuple in this setting is a function from names to values. This kind
of tuple is unrelated to Python's tuple type.

* As a function, no name may map to different values.
* A function is also a set of name value pairs.

Tuples are the building blocks of db relations. A relation has a header
and a body. The header is a `name -> type` tuple. The body is a set of
uniform `name -> value` tuples. The names in the body are the same as
those in the header, so that every value has a type.

A relational db is firstly a set, and the traditional set operations
are implemented on it. It is also a relation that has operations such
as select, project and join. It is interesting that many of these
operations can be implemented on the tuple type and 'lifted' to the
relation.

```
project :: a -> [Name] -> a
allBut :: a -> [Name] -> a
restrict :: a -> Predicate -> a
cross :: a -> a -> a
join :: a -> a -> a
extend :: a -> [(Name,Value)] -> a
rename :: a -> [(Name,Name)] -> a
sum,ave,min,max,all,any :: a -> Predicate -> a
```

## Development Notes

### Build and Install Distribution
```
cd ~/1/relbis-proj
virtualenv2 2
. 2/bin/activate
python setup.py sdist
tar tfvz dist/relbis-0.0.3.tar.gz
cp dist/relbis-0.0.3.tar.gz /tmp
cd /tmp
tar xvfz relbis-0.0.3.tar.gz
cd relbis-0.0.3/test
exec bash # clear virtualenv path
python -m unittest discover
```

### Test
```
cd test
python -m unittest discover
```

### View rendered markdown.
```
pandoc -r markdown_github README.md >README.html
lynx README.html
```

