*********************
Log Format Conversion
*********************

Raw data, particularly log data, is often not delimited cleanly but can be made to be so using some simple pattern
matching rules.  ``logcnv`` was developed to help with this process, with the intent that the parsed output be fed
directly into ``aq_pp`` for further processing.

In this tutorial, we will use an Apache web log as an example, since they are among the most common type of logs we
work with.  You will need the file :download:`apache.log<data/apache.log>`, the first line of which is::

    54.248.98.72 - - [23/Nov/2014:03:07:23 -0800] "GET / HTTP/1.0" 301 - "-" "Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"

Parsing Apache Logs
===================

``logcnv`` is similar to ``aq_pp`` in that it defines the column spec using type:name notation, except here we add a
new option 'sep' which specifies the substring that separates a given column from the one next to it.  The apache log
for example can be parsed using::

  logcnv -f,eok apache.log -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] "' s,clf,hl1:req_line1
  sep:'" ' i:res_status sep:' ' i:res_size sep:' "' s,clf:referrer sep:'" "' s,clf:user_agent sep:'"'``


As in other AQ tools, attributes are used to augment the processing.  Here, we use the 'hl1' attribute with the
column 'req_line1'.  This attribute parses HTTP request strings such as ``GET /index.html?query HTTP/1.0``.

Similar to ``aq_pp`` you can specify the columns to output using the ``-c`` option and a list of column names.

You can limit which columns are output in the final result by using the '-c' option. i.e. run::

  logcnv -f,eok apache.log -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] "' \
                              s,clf,hl1:req_line1 sep:'" ' i:res_status sep:' ' i:res_size sep:' "' s,clf:referrer \
                              sep:'" "' s,clf:user_agent sep:'"' \
                              -c ip time req_line1_f2 res_status res_size``

  "ip","time","req_line1_f2","res_status","res_size"
  54.248.98.72,1416740843,"/",301,0
  46.23.67.107,1416740853,"/",301,0
  85.17.156.99,1416740863,"/",200,30003
  173.193.219.173,1416740885,"/",301,0
  54.248.98.72,1416740903,"/",301,0
  93.174.93.117,1416740904,"/xmlrpc.php",200,370
  46.23.67.107,1416740913,"/",301,0
  93.174.93.117,1416740919,"/xmlrpc.php",200,370
  174.34.156.130,1416740923,"/",200,30003
  173.193.219.173,1416740945,"/",301,0


