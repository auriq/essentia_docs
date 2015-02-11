Combining Datasets
==================

--------------------------------------------------------------------------------

First lets **combine** the two example files **by row** using the ``-cat`` option. 

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -cat,+1 lookup.csv s:grade f:float_2 s:last_name s:first_name s:country``
        
* This tells aq_pp to skip the first line of tutorialdata.csv and import the rest of the data. Then it uses ``-cat,+1`` to add all except for the first line of lookup.csv to the imported records. 
* The columns last_name, first_name, and country are in both files so they will have values for all eight resulting rows. However, float_col and integer_col only exist in tutorialdata.csv so only the first four records of the result will have values for these columns. Similarly, grade and float_2 only exist in lookup.csv so only the last four rows of the result will have values for these columns. The output is::

    "float_col","integer_col","last_name","first_name","country","grade","float_2"
    99.909999999999997,5350,"Lawrence","Lois","Philippines",,0
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal",,0
    45.289999999999999,8356,"Wheeler","Sarah","Portugal",,0
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines",,0
    0,0,"Lawrence","Lois","Philippines","A",12.300000000000001
    0,0,"Hamilton","Evelyn","Portugal","C",96.599999999999994
    0,0,"Wheeler","Sarah","Portugal","F",89
    0,0,"Kelley","Jacqueline","Philippines","F",57.600000000000001

\ 

--------------------------------------------------------------------------------

As you can see this automatically gives values of zero or the empty string ("") to rows from a dataset that is missing the full set of columns. However, what if we wanted just one set of rows with meaningful values in all of the columns? 

With these example datasets, this actually makes more sense since both datasets contain some identical columns with identical values in those columns. Thus we want to **combine** these two datasets **by column** using the ``-cmb`` option.

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -cmb,+1 lookup.csv s:grade f:float_2 s:last_name s:first_name s:country``
        
* This command tells aq_pp to skip the first line of tutorialdata.csv and import the rest of the data. It then combines all except for the first line of lookup.csv with the imported records by the datasets' shared columns using ``-cmb,+1``. 
* The columns last_name, first_name, and country are in both files so they are used to combine the datasets. The columns float_col, integer_col, grade, and float_2 are added to the resulting dataset by their unique values in the last_name, first_name, and country columns. The resulting data set will contain columns float_col, integer_col, last_name, first_name, country, grade, and float_2. The output is::

    "float_col","integer_col","last_name","first_name","country","grade","float_2"
    99.909999999999997,5350,"Lawrence","Lois","Philippines","A",12.300000000000001
    73.609999999999999,1249,"Hamilton","Evelyn","Portugal","C",96.599999999999994
    45.289999999999999,8356,"Wheeler","Sarah","Portugal","F",89
    3.5299999999999998,9678,"Kelley","Jacqueline","Philippines","F",57.600000000000001
    
\ 
    
--------------------------------------------------------------------------------
    
This added on the extra two columns from lookup.csv onto the corresponding columns from tutorialdata.csv. The ``-cmb`` option also includes the capability to **overwrite existing columns** in the input dataset with values from columns with the same name in the combined dataset. 

We can adjust our command to utilize this feature by simply changing the specification of the combined dataset's columns to match those of the input dataset. 
 
``aq_pp -f,+1 tutorialdata.csv -d s:float_col f:integer_col s:last_name s:first_name s:country -cmb,+1 lookup.csv s,cmb:float_col f,cmb:integer_col s,key:last_name s,key:first_name s,key:country``

* This command tells aq_pp to skip the first line of tutorialdata.csv and import the rest of the data just as before. It also still combines all except for the first line of lookup.csv with the imported records by the datasets' shared columns. However, the first two columns in the combine statement are given the attribute 'cmb'. 
* This attribute tells aq_pp to replace any existing values of the attributed columns with the values in the combining file. In this case, the first two columns in tutorialdata.csv are replaced by the first two columns in lookup.csv. The output is::

    "float_col","integer_col","last_name","first_name","country"
    "A",12.300000000000001,"Lawrence","Lois","Philippines"
    "C",96.599999999999994,"Hamilton","Evelyn","Portugal"
    "F",89,"Wheeler","Sarah","Portugal"
    "F",57.600000000000001,"Kelley","Jacqueline","Philippines"

\ 

--------------------------------------------------------------------------------

What if you just want to **replace** values of **one of the columns** in your dataset **with values from another dataset**?

This is where you would use ``-sub``. By simply specifying which file contains the values you want to compare your data to and which values you want to replace your data with, you can easily overwrite an existing column with new values. 

``aq_pp -f,+1 tutorialdata.csv -d f:float_col i:integer_col s:last_name s:first_name s:country -sub last_name lookup.csv TO X FROM X X``

* This checks whether any values in last_name match any of the values in the third column of lookup.csv and, if they do, replaces those values with the value in the first column of lookup.csv. The output is::
 
    "float_col","integer_col","last_name","first_name","country"
    99.909999999999997,5350,"A","Lois","Philippines"
    73.609999999999999,1249,"C","Evelyn","Portugal"
    45.289999999999999,8356,"F","Sarah","Portugal"
    3.5299999999999998,9678,"F","Jacqueline","Philippines"
    
While this offers similar behavior to ``-cmb`` when it tries to overwrite existing columns it differs in three ways:

1. ``-sub`` acts compares and replaces only one column in the input dataset, whereas ``-cmb`` must by definition have a key column used to compare and a separate column where the values are placed into. 
2. ``-sub`` can match reular expressions and patterns between the datasets, whereas ``-cmb`` will only match values that are identical.
3. ``-sub`` is faster.