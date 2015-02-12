logcnv
======

This tutorial uses Apache Log data in Extended Apache Log Format from the 125-access_log files included in the local install and on asi-public. The top 10 lines of the data are given below for reference::

    54.248.98.72 - - [23/Nov/2014:03:07:23 -0800] "GET / HTTP/1.0" 301 - "-" "Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    
    46.23.67.107 - - [23/Nov/2014:03:07:33 -0800] "GET / HTTP/1.0" 301 - "-" "Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    
    85.17.156.99 - - [23/Nov/2014:03:07:43 -0800] "GET / HTTP/1.1" 200 30003 "-" "Pingdom.com_bot_version_1.4_(http://www.pingdom.com)"
    
    173.193.219.173 - - [23/Nov/2014:03:08:05 -0800] "GET / HTTP/1.0" 301 - "-" "Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    
    54.248.98.72 - - [23/Nov/2014:03:08:23 -0800] "GET / HTTP/1.0" 301 - "-" "Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    
    93.174.93.117 - - [23/Nov/2014:03:08:24 -0800] "POST /xmlrpc.php HTTP/1.0" 200 370 "-" "Mozilla/4.0 (compatible: MSIE 7.0; Windows NT 6.0)"
    
    46.23.67.107 - - [23/Nov/2014:03:08:33 -0800] "GET / HTTP/1.0" 301 - "-" "Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    
    93.174.93.117 - - [23/Nov/2014:03:08:39 -0800] "POST /xmlrpc.php HTTP/1.0" 200 370 "-" "Mozilla/4.0 (compatible: MSIE 7.0; Windows NT 6.0)"
    
    174.34.156.130 - - [23/Nov/2014:03:08:43 -0800] "GET / HTTP/1.1" 200 30003 "-" "Pingdom.com_bot_version_1.4_(http://www.pingdom.com)"
    
    173.193.219.173 - - [23/Nov/2014:03:09:05 -0800] "GET / HTTP/1.0" 301 - "-" "Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"

**Example Command:**

``logcnv -f,eok apachelogs -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] "' s,clf,hl1:req_line1 sep:'" ' i:res_status sep:' ' i:res_size sep:' "' s,clf:referrer sep:'" "' s,clf:user_agent sep:'"'``
    
This statement tells logcnv to convert the file apachelogs, ignoring errors, according to the following column specification.

Everything after the '-d' is telling logcnv how to parse the file; what the types of the columns are, what to name them, and how to separate them. 

The sep:'**separation**' statements contain the literal specification of what the separation is between each successive column. Thus the separations are, in order:

* ``' '`` **= space**
* ``' '`` **= space**
* ``' ['`` **= space then left handed square bracket**
* ``'] "'`` **= right-handed square bracket then space then double quotation mark**
* ``'" '`` **= double quotation mark then space**
* ``' '`` **= space**
* ``' "'`` **= space then double quotation work**
* ``'" "'`` **= double quotation mark then sppace then double quotation mark**
* ``'"'`` **= double quotation mark**

Essentia's log converter parses the file according to this specification and outputs it in csv format to standard output. The top 11 lines of the output are::

    "ip","rlog","rusr","time","req_line1_f1","req_line1_f2","req_line1_f3","res_status","res_size","referrer","user_agent"
    54.248.98.72,"-","-",1416740843,"GET","/","HTTP/1.0",301,0,"-","Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    46.23.67.107,"-","-",1416740853,"GET","/","HTTP/1.0",301,0,"-","Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    85.17.156.99,"-","-",1416740863,"GET","/","HTTP/1.1",200,30003,"-","Pingdom.com_bot_version_1.4_(http://www.pingdom.com)"
    173.193.219.173,"-","-",1416740885,"GET","/","HTTP/1.0",301,0,"-","Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    54.248.98.72,"-","-",1416740903,"GET","/","HTTP/1.0",301,0,"-","Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    93.174.93.117,"-","-",1416740904,"POST","/xmlrpc.php","HTTP/1.0",200,370,"-","Mozilla/4.0 (compatible: MSIE 7.0; Windows NT 6.0)"
    46.23.67.107,"-","-",1416740913,"GET","/","HTTP/1.0",301,0,"-","Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"
    93.174.93.117,"-","-",1416740919,"POST","/xmlrpc.php","HTTP/1.0",200,370,"-","Mozilla/4.0 (compatible: MSIE 7.0; Windows NT 6.0)"
    174.34.156.130,"-","-",1416740923,"GET","/","HTTP/1.1",200,30003,"-","Pingdom.com_bot_version_1.4_(http://www.pingdom.com)"
    173.193.219.173,"-","-",1416740945,"GET","/","HTTP/1.0",301,0,"-","Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"

\ 

**Note:** Notice that req_line1 was separated into three columns (req_line1_f1, req_line1_f2, req_line1_f3). This was because we used the ``,hl1`` attribute when we defined it as a column since it contains the action, file, and protocol involved in that record and we wanted to separate these into different columns.

\ 

You can limit which columns are output in the final result by using the '-c' option. I.e. run:

``logcnv -f,eok apachelogs -d ip:ip sep:' ' s:rlog sep:' ' s:rusr sep:' [' i,tim:time sep:'] "' s,clf,hl1:req_line1 sep:'" ' i:res_status sep:' ' i:res_size sep:' "' s,clf:referrer sep:'" "' s,clf:user_agent sep:'"' -c time req_line1_f2 res_status res_size``

This will limit the output columns to just time, req_line1_f2, res_status, and res_size; which are the only columns necessary for the time (daily counts) part of apache analysis. The top 11 lines of the output are::

    "time","req_line1_f2","res_status","res_size"
    1416740843,"/",301,0
    1416740853,"/",301,0
    1416740863,"/",200,30003
    1416740885,"/",301,0
    1416740903,"/",301,0
    1416740904,"/xmlrpc.php",200,370
    1416740913,"/",301,0
    1416740919,"/xmlrpc.php",200,370
    1416740923,"/",200,30003
    1416740945,"/",301,0

\ 

See our sample Apache Analysis and R Integration scripts to see how to put this to use analyzing apache logs.