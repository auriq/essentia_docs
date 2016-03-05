*********************
Using R with Essentia
*********************

In order to use R with Essentia, you must install the RESS package from C-RAN. Open R and then run::

   install.packages("RESS")

 
This package contains three R functions that can be used to capture the output of Essentia commands into
R.

* **read.essentia** takes an Essentia script and captures the output csv data into R, where you can save the output to a dataframe or stream it directly into additional analysis. The output can only contain the csv formatted data that you want to read into R.
* **essQuery** is used to directly query the database using a single statement. You can call **essQuery** multiple times to run different statements. You can save the output to a dataframe or stream it directly into additional analysis.
* **capture.essentia**, on the other hand, takes a file containing any number of Essentia commands and captures the output of the specified statements into R dataframes. Thus if you plan to run multiple statements that may be somewhat related to each other, you may want to use **capture.essentia**.

All three functions require an Essentia Bash script to be executed that sets up the Essentia environment and optionally loads data into the UDB database. Thus they require you to run ::

    sh **load_script_name**.sh

You can call any of these functions in an R script or on the R interactive prompt. It may be useful to maintain your RESS function calls in such an R script and refer to a separate script containing your R analyses by storing its filename as ``rscriptfile`` ::

    rscriptfile <- "**r_analysis_script**.R"

.. Note: These filenames do NOT have to be the same.

This makes the R script containing your RESS function calls more readable but is not required. You can always type your R analysis directly into the script you're using to call **read.essentia**, **essQuery**, or **capture.essentia**. 
You can also choose to work on the R interactive prompt instead.

To have R run both the essentia queries and the commands found in your R file and then exit, run ::

    R -f **your_r_script**.R
    
If you want to stay in R after your R script is run, first enter R by typing ::

    R
    
at the command prompt. Then run the R command::

    source("**your_r_script**.R", echo=FALSE)
    
.. note::

    The rest of this document only describes the options and sytax of ``essQuery`` and ``capture.essentia``. To see an example of how read.essentia is used, go through :doc:`rtutorial` or :doc:`rtutorial2`.

Apache Example
==============
    
*The Apache Example assumes you are working in the* ``casestudies/apache/`` *directory of the github repository. If you are not currently in this directory, please switch to it now.*
    
**Running the Apache Example with essQuery**

1. Run ``sh setupapache.sh``  on the command line.
2. Run ``R`` on the command line.
3. In the R prompt that appears, run ``source("essqueryapache.R", echo=FALSE)``
    
**Running the Apache Example with capture.essentia**

1. Run ``sh setupapache.sh``  on the command line.
2. Run ``R`` on the command line.
3. In the R prompt that appears, run ``source("readudbapache.R", echo=FALSE)``

You will see the results of the analysis print to the screen.

To see the commands involved in getting this analysis, open essqueryapache.R and analyzeapache.R for **essQuery** or queryapache.sh and analyzeapache.R for **capture.essentia**.

R Integration Format Requirements
=================================

For statements that you want to capture the output from, you must either 

* call them separately with **read.essentia** or **essQuery** or
 
* include all of these statements in the script containing your essentia query commands and call the query script with **capture.essentia**.

Ess Exec Statements
------------------------

By default, the R Integrator captures the output of ``ess exec`` statements.

You must have one output to standard out per ``ess exec`` statement.

Thus you must separate multiple database exports or counts into multiple ``ess exec`` statements.

To ignore a statement, put ``#Rignore`` at the end of the statement line.

Ess Stream Statements
--------------------------

To include an ``ess stream`` statement, put ``#Rinclude`` at the end of the statement line.

If you want to capture the output of an ``ess stream`` statement, you CANNOT use its ``--debug`` option.

If you are streaming multiple files from one category and want to include that statement, you must include a ``-notitle`` flag somewhere in your statement, in addition to ``#Rinclude``.

To separate these files into separate variables in R, include ``#Rseparate`` somewhere in your statement line. 
You can also then use the ``#filelist`` flag to store an extra dataframe in R that saves the list of files you streamed into R.

Ess Query Statements
--------------------

To include an ``ess query`` statement, put ``#Rinclude`` at the end of the statement line.

You can stream a single file or multiple files from one category into R using ``ess query``; however, you cannot separate these files into separate R variables with the ``#Rseparate`` flag.

The benefits gained from using ``ess query`` are the sql-like commands and a small speed advantage when streaming a moderate amount of data.

Flags for RIntegration
-----------------------

The flags added to the essentia commands in the **essQuery** call or query script can include:

*    ``#Rignore`` : Ignore an ``ess exec`` statement. Do not capture
     the output of the statement into R.

*    ``#Rinclude`` : Include an ``ess stream`` or ``ess query`` statement. Capture the
     output of the statement into R.

*    ``#-notitle`` : Tell R not to use the first line of the output as
     the header.

*    ``#Rseparate`` : Can be used when saving multiple files into an R
     dataframe using an ``ess stream`` command. Saves each file into
     a different R dataframe.

*    ``#filelist`` : Causes an extra dataframe to be stored in R that
     saves the list of files streamed into R when streaming multiple
     files.

*    ``#R#name#R#`` : Allows any automatically saved dataframe to be
     renamed to whatever is entered in place of ``name``. When used with
     ``#Rseparate``, saves the files as name1 to nameN, where N is the
     number of files.  Since this still counts as a statement, the next
     default dataframe saved will be stored as command followed by the
     number of previous statements run plus one. This only
     applies in **essQuery** when streaming multiple files with ``#Rseparate``.


Output of essQuery
-------------------

The value returned by **essQuery** is the output from querying the database. This can be saved into an R dataframe :: 

    **my_dataframe_name** <- essQuery(essentia_command, aq_command, flags)

or directly analyzed in R.

If you use **essQuery** to save multiple files into separate R dataframes using a single ``ess stream`` command, the files are stored automatically in R dataframes called command1 to commandN
(where N is the number of files) and no value is returned. 

To change the names of the stored dataframes, use the ``#R#any_name#R#`` flag. The dataframes will then be stored as any_name1 to any_nameN.

With ``#filelist``, the extra dataframe is saved as "commandN+1" by default, or "any_nameN+1" if ``#R#any_name#R#`` is also used.

Order of R Variables with capture.essentia
------------------------------------------

The output you capture from each statement will be saved into R variables labeled command1, command2, .... in order.

Thus if you have 4 statements total and capture the output from only the second and fourth statements, then the output of those two statements would be saved into R variables command1 and command2.

Similarly if you have 10 statements total and capture the output from any 6 of the statements they would be stored as ::

    command1, command2, command3, command4, command5, command6

in the order that you wrote those six statements.

You can change the name of the output variable by including ``#R#any_variable_name#R#`` somewhere in your statement line. When used with ``#Rseparate``, this saves the files as name1 to nameN, 
where N is the number of files. Since this still counts as a statement, the next default dataframe saved will be stored as ``command`` followed by the number of previous statements run plus one.

Therefore if command3 above had been an ``ess stream`` statement that saved 3 files into R with the flags ``#Rseparate`` and ``#R#myvariable#R#``, the 6 statements would be stored as ::

    command1, command2, myvariable1, myvariable2, myvariable3, command4, command5, command6
    
If the ``ess stream`` statement also included the ``#filelist`` flag then the statements would be stored as ::

    command1, command2, myvariable1, myvariable2, myvariable3, myvariable4, command4, command5, command6
    
where myvariable4 contains the list of filenames.

Syntax Examples for capture.essentia
------------------------------------

You can enter any commands with the syntax demonstrated in this section into your query script and then call **capture.essentia** on that file, ::

    capture.essentia("**query_script_name**")

on a specific line of the file, ::

    capture.essentia("**query_script_name**", 10)
    
or on a series of lines in the file ::

    capture.essentia("**query_script_name**",c(13,14,15))
    
.. note::

    The rest of the commands in this section demonstrate the correct syntax for commands in your ``query`` script.
    
``ess exec "aq_udb -cnt **database_name**:vector1'" --debug``

* Outputs to std. out. (default) and will be captured in an R variable. This is the main use for the R integrator.

``ess exec "aq_udb -cnt **database_name**:vector1'" --debug #Rignore``

* This will IGNORE this ``ess exec`` statement and this statement's output will NOT be stored in a variable in R.

``ess stream category startdate enddate "**command**'" #Rinclude``

* Takes the output of this ``ess stream`` command and saves it into a variable in R.

* A command such as ``head -30`` will work with the R integrator. You can use it to preview and analyze the top records in each of your files.

* Similarly you could run 

  ``ess query "select * from category:startdate:enddate limit 30" #Rinclude`` 

  to achieve the same effect.

.. maybe remove this part (when i use etl_commands) or switch to tail-30 and bottom records or subset of the records in.

**Saving Files into R Variables using 'ess stream'**

You can also save your files into R variables using ``ess stream category startdate enddate "cat -" #Rinclude`` for .csv files only or ``ess stream category startdate enddate "aq_pp -f,eok - -d %cols" #Rinclude`` for any file with a constant delimiter. This should only be used to explore or analyze a few files so the data doesnt become too large (this feature just streams the files you select into variables in R). 

When saving multiple files from one category into R, you MUST include Essentia's ``-notitle`` flag somewhere on the line. You also have the option of saving all of the files you are streaming as one variable or into separate variables (one for each file). By default, the R integrator loads all of the files used in one
``ess stream`` statement into a single R variable. To store each file into its own distinct R variable, run ::

    ess stream category startdate enddate "aq_pp -notitle -f,eok - -d %cols" #Rseparate #Rinclude #filelist
    
This will also cause the R integrator to automatically save the filenames of the stored files into a single additional R variable.

.. **Saving Files into R Variables using 'ess query'**

.. You can stream any files with a constant delimiter into an R dataframe using ``ess query "select * from category:startdate:enddate" #Rinclude`` 

**Access Log Data Integration Syntax Examples**

For any more complicated, delimited format you can use ``aq_pp`` to convert the format to csv within the ``ess stream`` commmand. All of the following examples have the correct syntax. The data they're acting on is in Extended Apache Log Format. ::

    ess stream 125accesslogs "2014-12-07" "2014-12-07" "aq_pp -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' s:time_s sep:'] \"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | cat -" #Rinclude
    
    ess stream 125accesslogs "2014-12-07" "2014-12-07" "head -30 | aq_pp -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' s:time_s sep:'] \"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X" #Rinclude
    
    ess stream 125accesslogs "2014-12-07" "2014-12-07" "head -q | aq_pp -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' s:time_s sep:'] \"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X" #Rinclude
    
    ess stream 125accesslogs "2014-12-07" "2014-12-07" "aq_pp -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' s:time_s sep:'] \"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X" #Rinclude

**Purchase Data Integration Syntax Examples**

These next examples work on the diy_workshop purchase data available in the samples folder provided with Essentia or on Auriq's publicly accessible bucket asi_public. ::
    
    ess stream purchase "2014-09-15" "2014-09-15" "aq_pp -f,eok - -d X s:userid X f:price X" #Rinclude
    
    ess stream purchase "2014-09-16" "2014-09-16" "aq_pp -notitle -f,+1,eok - -d X s:userid X f:price X" #Rinclude
    
    ess stream purchase "2014-09-17" "2014-09-17" "aq_pp -notitle -f,+1,eok - -d X s:userid X f:price X" #Rinclude
    
    ess stream purchase "2014-09-15" "2014-09-16" "aq_pp -notitle -f,+1,eok - -d X s:userid X f:price X" #Rseparate #Rinclude
    
    ess stream purchase 2014-09-01 2014-09-03 "aq_pp -notitle -stat -f,eok - -d %cols" #Rinclude
    
    ess exec "echo \"1, 2, 3, 4, 5\"" #-notitle
    
    ess stream purchase "*" "*" \
    "head -10 | aq_pp -notitle -f,+1,eok - -d %cols" \
    #Rinclude
    
    ess query "select * from browse:*:*" #-notitle #Rinclude #R#querybrowse#R#
    
    ess query "select * from purchase:*:*" #-notitle #Rinclude #R#querypurchase#R#
    
    ess query "select count(refID) from purchase:2014-09-01:2014-09-15 where articleID>=46 group by price" #Rinclude
    
    ess query "select count(distinct userID) from purchase:2014-09-01:2014-09-15 where articleID>=46" #Rinclude
    
    ess query "select count(refID) from purchase:2014-09-01:2014-09-15 where articleID>=46 group by userID" #Rinclude
    
    ess query "select * from purchase:*:* where articleID <= 20" #Rinclude #R#querystream#R#    
    
Syntax Examples for essQuery
-----------------------------

``essQuery("ess exec", "aq_udb -cnt **database_name**:vector1'", "--debug")``

* Outputs to std. out. (default) and will be returned by **essQuery**. This is the main use for the R integrator.

``essQuery("ess exec", "aq_udb -cnt **database_name**:vector1'", "--debug #Rignore")``

* This will IGNORE this ``ess exec`` statement and this statement's output will NOT be captured or returned by **essQuery**.

``essQuery("ess stream category startdate enddate", "**command**'", "#Rinclude")``

* Takes the output of this ``ess stream`` command and returns it to R using **essQuery**.

* A command such as ``head -30`` will work with the R integrator. You can use it to preview and analyze the top records in each of your files.

* Similarly you could run 

  ``essQuery("ess query", "select * from category:startdate:enddate limit 30", "#Rinclude")`` 

  to achieve the same effect.

**Saving Files into R Variables**

You can also send your files into R using ``essQuery("ess stream category startdate enddate", "cat -", "#Rinclude")`` for .csv files only or 
``essQuery("ess stream category startdate enddate", "aq_pp -f,eok - -d %cols", "#Rinclude")`` for any file with a constant delimiter. 
This should only be used to explore or analyze a few files so the data doesnt become too large (this feature just streams the files you select into variables in R).

When saving multiple files from one category into R, you MUST include Essentia's ``-notitle`` flag somewhere on the line. You also have the option of sending all of the files you are streaming into R as a single returned output or as separate dataframes (one for each file). By default, the R integrator loads all of the files used in one
``ess stream`` statement into a single returned output. To store each file into its own distinct R variable, run ::

    essQuery("ess stream category startdate enddate", "aq_pp -notitle -f,eok - -d %cols", "#Rseparate #Rinclude #filelist")
    
This will also cause the R integrator to automatically save the filenames of the stored files into a single additional R variable.

**Access Log Data Integration Syntax Examples**

For any more complicated, delimited format you can use ``aq_pp`` to convert the format to csv within the stream commmand. All of the following examples have the correct syntax. The data they're acting on is in Extended Apache Log Format. ::

    essQuery("ess stream 125accesslogs \"2014-12-07\" \"2014-12-07\"", "aq_pp -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' s:time_s sep:'] \\\"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\\\" ' i:res_status sep:' ' i:res_size sep:' \\\"' s,clf:referrer sep:'\\\" \\\"' s,clf:user_agent sep:'\\\"' X | cat -", "#Rinclude")
    
    essQuery("ess stream 125accesslogs \"2014-12-07\" \"2014-12-07\"", "head -30 | aq_pp -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' s:time_s sep:'] \\\"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\\\" ' i:res_status sep:' ' i:res_size sep:' \\\"' s,clf:referrer sep:'\\\" \\\"' s,clf:user_agent sep:'\\\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X", "#Rinclude")
    
    essQuery("ess stream 125accesslogs \"2014-12-07\" \"2014-12-07\"", "head -q | aq_pp -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' s:time_s sep:'] \\\"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\\\" ' i:res_status sep:' ' i:res_size sep:' \\\"' s,clf:referrer sep:'\\\" \\\"' s,clf:user_agent sep:'\\\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X", "#Rinclude")
    
    essQuery("ess stream 125accesslogs \"2014-12-07\" \"2014-12-07\"", "aq_pp -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' s:time_s sep:'] \\\"' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 sep:'\\\" ' i:res_status sep:' ' i:res_size sep:' \\\"' s,clf:referrer sep:'\\\" \\\"' s,clf:user_agent sep:'\\\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X", "#Rinclude")

**Purchase Data Integration Syntax Examples**

These next examples work on the diy_workshop purchase data available in the samples folder provided with Essentia or on Auriq's publicly accessible bucket asi_public. ::
    
    essQuery("ess stream purchase \"2014-09-15\" \"2014-09-15\"", "aq_pp -f,eok - -d X s:userid X f:price X", "#Rinclude")
    
    essQuery("ess stream purchase \"2014-09-16\" \"2014-09-16\"", "aq_pp -notitle -f,+1,eok - -d X s:userid X f:price X", "#Rinclude")
    
    essQuery("ess stream purchase \"2014-09-17\" \"2014-09-17\"", "aq_pp -notitle -f,+1,eok - -d X s:userid X f:price X", "#Rinclude")
    
    essQuery("ess stream purchase \"2014-09-15\" \"2014-09-16\"", "aq_pp -notitle -f,+1,eok - -d X s:userid X f:price X", "#Rseparate #Rinclude")
    
    essQuery("ess stream purchase 2014-09-01 2014-09-03", "aq_pp -notitle -stat -f,eok - -d %cols", "#Rinclude")
    
    essQuery("ess exec", "echo \\\"1, 2, 3, 4, 5\\\"", "#-notitle")
    
    essQuery("ess stream purchase \"*\" \"*\"", "head -10 | aq_pp -notitle -f,+1,eok - -d %cols", "#Rinclude")
    
    querybrowse <- essQuery("ess query", "select * from browse:*:*", "#-notitle #Rinclude")
    
    querypurchase <- essQuery("ess query", "select * from purchase:*:*", "#-notitle #Rinclude")
        
    pricecounts <- essQuery("ess query","select count(refID) from purchase:2014-09-01:2014-09-15 where articleID>=46 group by price","#Rinclude")
    
    distinctusers <- essQuery("ess query", "select count(distinct userID) from purchase:2014-09-01:2014-09-15 where articleID>=46", "#Rinclude")
    
    usercounts <- essQuery("ess query", "select count(refID) from purchase:2014-09-01:2014-09-15 where articleID>=46 group by userID", "#Rinclude")
    
    querystream <- essQuery("ess query", "select * from purchase:*:* where articleID <= 20", "#Rinclude")