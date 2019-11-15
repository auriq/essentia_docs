*********************
Log Format Conversion
*********************

Raw data, particularly log data, is often not delimited cleanly but can be made to be so using some simple pattern
matching rules. ``aq_pp`` was designed to help with this process.

In this tutorial, we will use an Apache web log as an example, since they are among the most common type of logs we
work with.  You will need the file ``apache.log``, which can be found under ``tutorials/etl-engine`` in the git repository.
Also have the following documentations open by your side for reference if you'd like. 

* :doc:`../../reference/manpages/aq-input`
* :ref:`Column Spec for Arbitrary Separators <col spec arbitrary>`

Its first line of the data is::

    54.248.98.72 - - [23/Nov/2014:03:07:23 -0800] "GET / HTTP/1.0" 301 - "-" "Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"


We'd like to parse data into format below (only subset of the entire columns are displayed here.)
Note the difference with the original data, especially the separators.

.. csv-table:: weblog parsed
   :header: "ip", "rlog", "rusr", "time_s", "req_line1", "req_line2", "req_line3", "res_status", "res_size"
   
   54.248.98.72, "-", "-", "23/Nov/2014:03:07:23 -0800", "GET", "/", "HTTP/1.0", 301, 0
   46.23.67.107, "-", "-", "23/Nov/2014:03:07:33 -0800", "GET", "/", "HTTP/1.0", 301, 0
   85.17.156.99, "-", "-", "23/Nov/2014:03:07:43 -0800", "GET", "/", "HTTP/1.1", 200, 30003



Parsing Apache Logs
===================

For singly-delimited files, ``aq_pp`` defines the column specification using type:name notation. To allow more complex format conversion such as we have here, 
we make use of the additional option 'sep' which specifies the substring that separates a given column from the one next to it.  The apache log
for example can be parsed using::

  aq_pp -f,eok,div apache.log -d ip:ip sep:' ' s:rlog sep:' ' \
  s:rusr sep:' [' s:time_s sep:'] "' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 \
  sep:'" ' i:res_status sep:' ' i:res_size sep:' "' \
  s,clf:referrer sep:'" "' s,clf:user_agent sep:'"' 



Additionally, in ``aq_pp`` you can specify the columns to output using the :ref:`-c option <-c>` and a list of column names.

You can limit which columns are output in the final result by using the '-c' option. i.e. run::

  aq_pp -f,eok,div apache.log -d ip:ip sep:' ' s:rlog sep:' ' \
  s:rusr sep:' [' s:time_s sep:'] "' s,clf:req_line1 sep:' ' s,clf:req_line2 sep:' ' s,clf:req_line3 \
  sep:'" ' i:res_status sep:' ' i:res_size sep:' "' \
  s,clf:referrer sep:'" "' s,clf:user_agent sep:'"' -eval i:time 'DateToTime(time_s, "d.b.Y.H.M.S.z")' \
  -c ip time req_line2 res_status res_size

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


