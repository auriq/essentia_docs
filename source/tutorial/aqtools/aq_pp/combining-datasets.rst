Combining Datasets
==================

cat for merging datasets
------------------------

There are a number of scenarios (particularly with log data) where merging two different types of files is useful.
Lets consider the case where we want to merge our chemistry and physics grades into a single table::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -cat,+1 physics.csv i:id s,up:lastname s:firstname f:phys_mid s:phys_fin
  "id","lastname","firstname","chem_mid","chem_fin","phys_mid","phys_fin"
  1,"DAWSON","Leona",76.5,"B-",0,
  2,"JORDAN","Colin",25.899999999999999,"D",0,
  3,"MALONE","Peter",97.200000000000003,"A+",0,
  1,"DAWSON","Leona",88.5,"A",0,
  3,"MALONE","Peter",77.200000000000003,"B",0,
  4,"CANNON","Roman",55.799999999999997,"C+",0,


The ``-cat`` option is used for such a merge, and it is easiest to think of it as the ``aq_pp`` specific version of
the unix command of the same name.  The difference here is that ``aq_pp`` will create new columns in the output,
while simply concatenating the two files will result in just the same 5 columns as before.

cmb for joining datasets
------------------------

However most users will want to JOIN datasets based on common values between two files.  In this case, the first and
last name, as well as the country, are the common columns between the two files.  The ``-cmb`` option is similar to
``-f`` and ``-d`` since it defines the number of lines to skip and the column specification for the second file.
Records will be matched based on all the columns that share the same names between the two files.  For example::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
        -cmb,+1 physics.csv i:id X X f:phys_mid s:phys_fin
  "id","lastname","firstname","chem_mid","chem_fin","phys_mid","phys_fin"
  1,"DAWSON","Leona",76.5,"B-",88.5,"A"
  2,"JORDAN","Colin",25.899999999999999,"D",0,
  3,"MALONE","Peter",97.200000000000003,"A+",77.200000000000003,"B"


Users familiar with SQL will recognize this as a LEFT OUTER JOIN. All the data from the first file is preserved,
while data from the second file is included when there is a match.  Where there is no match,
the value is 0 for numeric columns, or the empty string for string columns.  In this case,
since the label ``i:id`` is common between both file specifications, that is the join key.
We could also have joined based off multiple keys as well: For example matching first AND last
names will achieve the same result::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
  -cmb,+1 physics.csv X s,up:lastname s:firstname f:phys_mid s:phys_fin


sub for lookup tables
---------------------

An important type of dataset joining is replacing some value in a file with a matching entry in a lookup table.
In the following example, we wish to convert a students letter grade from 'A,B,C...' etc into a simple PASS/FAIL::

  aq_pp -f,+1 chemistry.csv -d i:id s,up:lastname s:firstname f:chem_mid s:chem_fin \
  -sub,+1,pat chem_fin grades.csv

  "id","lastname","firstname","chem_mid","chem_fin"
  1,"DAWSON","Leona",76.5,"PASS"
  2,"JORDAN","Colin",25.899999999999999,"FAIL"
  3,"MALONE","Peter",97.200000000000003,"PASS"

Note the use of the ``pat`` attribute when we designate the lookup table.  This means that column 1 of the lookup
table can have a pattern instead of a static value.  In our case, we can cover grades 'A+,A,
and A-' by the pattern 'A*'.


The ``-cmb`` can be used substituting data, but for situations similar to the one above, ``-sub`` is perferred because:

1. It does not create additional columns like ``-cmb`` does.  Values are modified in place.
2. ``-sub`` can match regular expressions and patterns, while ``-cmb`` is limited to exact matches.
3. ``-sub`` is faster.
