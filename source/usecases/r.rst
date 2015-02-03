Using R with Essentia on AWS
----------------------------

<p style="font-size: 32px; font-weight: 300;">Explore, Preprocess, and Shrink Your Big Data for Easy Loading and Analysis
in R</p><p>&nbsp;</p><p style="font-size: 18px;">Essentia’s selection, merge, and parallelization capabilities make it
the perfect fit to extend R into the regime of big data. With a single R script, you can now stream terabytes of data
directly through Essentia’s preprocessor and into your R analysis.</p><p style="font-size: 18px;">This tutorial provides
instructions and sample scripts for integrating R with Essentia.</p>


Instructions
~~~~~~~~~~~~

It is a good idea to have port 8787 open when using the R integrator on an AWS instance.

In order to use R with essentia, you must have an **any_file_name**.sh script containing your essentia commands and an **any_file_name**.R script containing your R analyses. These filenames do NOT have to be the same.

The next requirement is that you store those filenames as 'file' and 'rscriptfile' in the integrater.R script.
<pre class="lang:r decode:true">file &lt;- "**Any_Script_Name**.sh"
rscriptfile &lt;- "**Any_Script_Name**.R"</pre>
You then simply have R run integrater.R and it will execute both the essentia and R commands.

To have R run both the essentia commands and the commands found in your R file and then exit, run

<span class="lang:sh decode:true  crayon-inline ">R -f integrater.R</span>

If you want to stay in R after integrater.R is run, first enter R by typing

<span class="lang:sh decode:true  crayon-inline ">R</span>

at the command prompt. Then run the R command:

<span class="lang:sh decode:true  crayon-inline ">source("integrater.R", echo=FALSE)</span>

Format Requirements
~~~~~~~~~~~~~~~~~~~

<p style="text-align: left;">For each statement that you want to capture the output from, you must follow it with
<br> <span class="lang:sh decode:true  crayon-inline ">; echo 'RSTOPHERE'</span>&nbsp;(see the syntax examples below).
</p><h4 style="text-align: left;"><strong>Ess Task Exec&nbsp;Statements</strong></h4><p style="text-align: left;">
By default, the R Integrator captures the output of <span class="lang:sh decode:true  crayon-inline ">
ess task exec</span>&nbsp;&nbsp;statements.<br>
You must have one output to standard out per <span class="lang:sh decode:true  crayon-inline ">
ess task exec</span>&nbsp;&nbsp;statement.<br> Thus you must separate multiple database exports or counts into multiple
<span class="lang:sh decode:true  crayon-inline ">ess task exec</span>&nbsp;&nbsp;statements.<br> To ignore a statement,
put <span class="lang:sh decode:true  crayon-inline ">#Rignore</span>&nbsp;&nbsp;at the end of the statement line.
</p><h4 style="text-align: left;"><strong>Ess Task Stream Statements</strong></h4><p style="text-align: left;">To
include an <span class="lang:sh decode:true  crayon-inline ">ess task stream</span>&nbsp;&nbsp;statement, put
<span class="lang:sh decode:true  crayon-inline ">#Rinclude</span>&nbsp;&nbsp;at the end of the statement line.<br>
If you want to capture the output of an <span class="lang:sh decode:true  crayon-inline ">
ess task stream</span>&nbsp;&nbsp;statement, you CANNOT use its
 <span class="lang:sh decode:true  crayon-inline ">--debug</span>&nbsp;&nbsp;option.</p><p>
 If you are streaming multiple files from one category and want to include that statement, you must include
 a<br> <span class="lang:sh decode:true  crayon-inline ">-notitle</span>&nbsp;&nbsp;flag somewhere in your statement,
 in addition to&nbsp;<span class="lang:sh decode:true  crayon-inline ">#Rinclude</span>&nbsp;.</p><p>To separate these
 files into separate variables in R, include
 <span class="lang:sh decode:true  crayon-inline ">#Rseparate</span>&nbsp;&nbsp;somewhere in your statement line.
 </p><h4 style="text-align: left;"><strong>Order of R Variables</strong></h4><p style="text-align: left;">T
 he output you capture from each statement will be saved into R variables labeled command1, command2, .... in order.</p
 ><p style="text-align: left;">Thus if you have 4 statements total and capture the output from only the second and fourth
 statements, then<br> the output of those two statements would be saved into R variables 'command1' and 'command2'</p>
 <p style="text-align: left;">Similarly if you have 10 statements total and capture the output from any 6 of the statements
 they would be stored as<br> 'command1', 'command2', 'command3', 'command4', 'command5', 'command6'<br> in the order that
 you wrote those six statements.</p><p style="text-align: left;">You can change the name of the output variable by including
 <span class="toolbar:2 lang:sh decode:true  crayon-inline ">#R#any_variable_name#R#</span>&nbsp;&nbsp;somewhere in your
 statement line.&nbsp;However, this is NOT compatible with an <span class="lang:sh decode:true  crayon-inline ">
 ess task stream</span>&nbsp;&nbsp;statement that uses <span class="lang:sh decode:true  crayon-inline ">#Rseparate</span>&nbsp;.</p>


General Syntax Examples
~~~~~~~~~~~~~~~~~~~~~~~

<span class="lang:sh decode:true  crayon-inline ">ess task exec "aq_udb -cnt **database_name**:vector1; echo 'RSTOPHERE'" --debug</span>
Outputs to std. out. (default) and will be captured in an R variable. This is the main use for the R integrator.

<span class="lang:sh decode:true  crayon-inline ">ess task exec "aq_udb -cnt **database_name**:vector1; echo 'RSTOPHERE'" --debug #Rignore </span>
This will IGNORE this 'ess task exec' statement and this statement's output will NOT be stored in a variable in R.

<span class="lang:sh decode:true  crayon-inline ">ess task stream category startdate enddate "**command**; echo 'RSTOPHERE'" --debug #Rinclude</span>
Takes the output of this 'ess task stream' command and saves it into a variable in R.

A command such as <span class="lang:sh decode:true  crayon-inline">head -30</span>&nbsp; will work with the R integrator. You can use it to preview and analyze the top records in each of your files.
<h5><strong>Saving Files Into R Variables</strong></h5>
You can also save your files into R variables using
<span class="lang:sh decode:true  crayon-inline ">ess task stream category startdate enddate "cat -; echo 'RSTOPHERE'" #Rinclude </span>&nbsp;for .csv files only or
<span class="lang:sh decode:true  crayon-inline">ess task stream category startdate enddate "aq_pp -f,eok - -d %cols; echo 'RSTOPHERE'" #Rinclude</span>&nbsp;for any file with a constant delimiter.&nbsp;This should only be used to explore or analyze a few files so the data doesnt become too large (this feature just streams the files you select into variables in R).

When saving multiple files from one category into R, you MUST include Essentia's <span class="lang:sh decode:true  crayon-inline ">-notitle</span>&nbsp;&nbsp;flag somewhere on the line (it can be in a comment if you prefer). You also have the option of saving all of the files you are streaming as one variable or into separate variables (one for each file).&nbsp;By default, the R integrator loads all of the files used in one
<span class="lang:sh decode:true  crayon-inline ">ess task stream</span>&nbsp;&nbsp;statement into a single&nbsp;R variable.&nbsp;To store each file into its own distinct R variable, run
<pre class="toolbar:2 lang:sh decode:true">ess task stream category startdate enddate "aq_pp -notitle -f,eok - -d %cols; echo 'RSTOPHERE'" #Rseparate #Rinclude</pre>
This will also cause the R integrator to automatically save the filenames of the stored files into a single additional R variable.

Examples 1
~~~~~~~~~~

For any more complicated, delimited format you can use logcnv to convert the format to csv within the stream commmand. All of the following examples have the correct syntax. The data they're acting on is in Extended Apache Log Format.
<pre class="toolbar:1 lang:sh decode:true" title="Access Log Data Integration Examples">ess task stream 125accesslogs "2014-12-07" "2014-12-07" "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf,hl1:req_line1 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | cat -; echo 'RSTOPHERE'" #Rinclude

ess task stream 125accesslogs "2014-12-07" "2014-12-07" "head -30 | logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf,hl1:req_line1 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X; echo 'RSTOPHERE'" #Rinclude

ess task stream 125accesslogs "2014-12-07" "2014-12-07" "head -q | logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf,hl1:req_line1 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X; echo 'RSTOPHERE'" #Rinclude

ess task stream 125accesslogs "2014-12-07" "2014-12-07" "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf,hl1:req_line1 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X; echo 'RSTOPHERE'" #Rinclude

ess task stream 125accesslogs "2014-12-07" "2014-12-07" "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf,hl1:req_line1 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X | head -30; echo 'RSTOPHERE'" #Rinclude

ess task stream 125accesslogs "2014-12-07" "2014-12-07" "logcnv -f,eok - -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] \"' s,clf,hl1:req_line1 sep:'\" ' i:res_status sep:' ' i:res_size sep:' \"' s,clf:referrer sep:'\" \"' s,clf:user_agent sep:'\"' X | aq_pp -f,qui,eok - -d ip:ip2 s:rlog X X X X X X X X X | head -q; echo 'RSTOPHERE'" #Rinclude</pre>

Examples 2
~~~~~~~~~~

These next examples work on the diy_workshop purchase data available in the samples folder provided with Essentia or on Auriq's publicly accessible bucket asi_public.
<pre class="toolbar:1 lang:sh decode:true" title="Purchase Data Integration Examples">ess task stream purchase "2014-09-15" "2014-09-15" "aq_pp -f,eok - -d X s:userid X f:price X; echo 'RSTOPHERE'" #Rinclude

ess task stream purchase "2014-09-16" "2014-09-16" "aq_pp -notitle -f,+1,eok - -d X s:userid X f:price X; echo 'RSTOPHERE'" #Rinclude

ess task stream purchase "2014-09-17" "2014-09-17" "aq_pp -notitle -f,+1,eok - -d X s:userid X f:price X; echo 'RSTOPHERE'" #Rinclude

ess task stream purchase "2014-09-15" "2014-09-16" "aq_pp -notitle -f,+1,eok - -d X s:userid X f:price X; echo 'RSTOPHERE'" #Rseparate #Rinclude

ess task stream purchase 2014-09-01 2014-09-03 "aq_pp -notitle -stat -f,eok - -d %cols; echo 'RSTOPHERE'" #Rinclude

ess task exec "echo \"1, 2, 3, 4, 5\"; echo 'RSTOPHERE'" #-notitle

ess task stream purchase "*" "*" \
"head -10 | aq_pp -notitle -f,+1,eok - -d %cols; echo 'RSTOPHERE'" \
#Rinclude</pre>

