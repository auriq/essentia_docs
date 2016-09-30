#!/bin/python
import subprocess as sp
essoutput=(sp.Popen('ess -h',stdout=sp.PIPE,shell=True)).communicate()[0]
# print "--------------------------------"
# print "**ess**"
# print "--------------------------------\n"
# if len(essoutput)!=0:
#    print "::\n"
# print "    "+essoutput.replace("\n","\n    ")
def grablines(input,startstring,endstring,replace=False,file=False):
 myreplace = ""; myreplace2 = ""; myreplace3 = "{0} |".format(input); myreplace4 = "!d"
 if replace == True:
  myreplace = "-i"
  myreplace2 = file
  myreplace = "d"
 if file == True:
  myreplace3 = ""
 mystartend="""{0} | aq_pp -d s:all -var i:start 0 -var i:end 0 -if -filt 'PatCmp(all,"{1}")' -eval start '$RowNum' \
-elif -filt 'PatCmp(all,"{2}")' -eval end "\$RowNum" -endif -ovar,notitle - | aq_pp -d s:start s:end -eval s:command "\\\"{5} sed {3} -e '\\\"+start+\\\",\\\"+end+\\\"{6}' {4}\\\"" -o,notitle - -c command | tr -d '"' """.format(input,startstring,endstring,myreplace,myreplace2,myreplace3,myreplace4)
# print mystartend
 startend=(sp.Popen(mystartend,stdout=sp.PIPE,shell=True)).communicate()[0]
# print startend
 confreplace=(sp.Popen(startend,stdout=sp.PIPE,shell=True)).communicate()[0] 
 return confreplace

with open('{0}.rst'.format("ess"), 'w+') as f:
  f.write("--------------------------------\n")
  f.write("**ess**\n")
  f.write("--------------------------------\n\n")
  f.write("Synopsis\n========\n\n")
  if len(essoutput)!=0:
   f.write("::\n\n")
  f.write(grablines("ess -h","usage*","*...*"))
  f.write("\nDescription\n===========\n\n")
  f.write(grablines("ess -h","The*","The*"))
  f.write("\n")
  f.write("Command Summary\n==============\n\n")
  if len(essoutput)!=0:
   f.write("::\n\n")
  corelastline=(sp.Popen("ess -h | tail -1 | tr -d '\n'",stdout=sp.PIPE,shell=True)).communicate()[0]
  lastline = "*" + corelastline + "*"
#  print lastline
  f.write(grablines("ess -h","optional*",lastline))
#  f.write("    "+essoutput.replace("\n","\n    "))
  f.write("\nSee Also\n=========\n\n")

mystartend="""cat conf.py | aq_pp -d s:all -var i:start 0 -var i:end 0 -if -filt 'PatCmp(all,"man_pages*")' -eval start '$RowNum' \
-elif -filt 'PatCmp(all,"*man_show_urls*")' -eval end "\$RowNum" -endif -ovar,notitle - | aq_pp -d s:start s:end -eval s:command \
"\\\"sed -i -e '\\\"+start+\\\",\\\"+end+\\\"d' conf.py\\\"" -o,notitle - -c command | tr -d '"' """
print mystartend
startend=(sp.Popen(mystartend,stdout=sp.PIPE,shell=True)).communicate()[0]
print startend
confreplace=(sp.Popen(startend,stdout=sp.PIPE,shell=True)).communicate()[0]

essmain = ""
confman = """man_pages = [
    ('ess', 'ess', u'',
    [u'AuriQ Systems Inc.'], 1),\n"""
#    ('essfull', 'essfull', u'',
#    [u'AuriQ Systems Inc.'], 1),\n"""

if '{' in essoutput and '}' in essoutput:
    subcommands = essoutput.partition('{')[2].partition('}')[0]
    # print(subcommands)
for subcommand in subcommands.split(','):
  with open('{0}-{1}.rst'.format("ess",subcommand), 'w+') as f:
    # print subcommand
#    essoutput=subcommand #TEMPORARY, REMOVE   
    essoutput=(sp.Popen('ess {0} -h'.format(subcommand),stdout=sp.PIPE,shell=True)).communicate()[0]
    # print essoutput
    file="ess-{0}".format(subcommand)
    addtoess="* :manpage:`{0}(1)`\n".format(file)
    addtoconf="""    ('{0}', {1}', u'',
    [u'AuriQ Systems Inc.'], 1),\n""".format(file,file)
    essmain="{0}{1}".format(essmain,addtoess)
    confman="{0}{1}".format(confman,addtoconf)

    if '{' in essoutput and '}' in essoutput:
        subcommands2 = essoutput.partition('{')[2].partition('}')[0]
        # print(subcommands2)
        f.write("--------------------------------\n")
        f.write("**ess {0}**\n".format(subcommand))
        f.write("--------------------------------\n\n")
        for subcommand2 in subcommands2.split(','):
            # print subcommand2
#            essoutput=subcommand2 #TEMPORARY, REMOVE   
            essoutput=(sp.Popen('ess {0} {1} -h'.format(subcommand,subcommand2),stdout=sp.PIPE,shell=True)).communicate()[0]
            f.write("+++++++++++++++++++++++++++++++++\n")
            f.write("``ess {0} {1}``\n".format(subcommand,subcommand2))
            f.write("+++++++++++++++++++++++++++++++++\n\n")
            if len(essoutput)!=0:
               f.write("::\n\n")
            f.write("    "+essoutput.replace("\n","\n    "))
	    f.write("\n")
#            if subcommand == "cluster" or subcommand == "server":
#               f.write("**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_\n    ")
#            elif subcommand == "stream" or subcommand == "exec":
#               f.write("**See Also:** :doc:`../tables/index`\n    ")


    else:
      print "writing ess {0} \n".format(subcommand)
      f.write("--------------------------------\n")
      f.write("**ess {0}**\n".format(subcommand))
      f.write("--------------------------------\n\n")
      if len(essoutput)!=0:
         f.write("::\n\n")
      f.write("    "+essoutput.replace("\n","\n    "))
#      if subcommand == "cluster" or subcommand == "server":
#         f.write("**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_\n    ")
#      elif subcommand == "stream" or subcommand == "exec":
#         f.write("**See Also:** :doc:`../tables/index`\n    ")

confman="""{0}]

# If true, show URL addresses after external links.
#man_show_urls = False\n""".format(confman)
with open('{0}.rst'.format("ess"), 'a') as f:
  f.write(""+essmain)

with open('conf.py', 'a') as f:
  f.write(confman)

geness=(sp.Popen('cat generate_essentia_ref.rst',stdout=sp.PIPE,shell=True)).communicate()[0]

with open('{0}.rst'.format("essfull"), 'w+') as f:
   essfull="""********************************
**ess**
********************************\n\n"""
   f.write(essfull)
   f.write(geness)



#[bwaxer@docdev manuals]$ ll /usr/share/man/man1/ | grep ess
#[bwaxer@docdev manuals]$ sudo cp _build/man/ess.1 /usr/share/man/man1/.
#[bwaxer@docdev manuals]$ man ess

