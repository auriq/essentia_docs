#!/bin/python
import subprocess as sp
essoutput=(sp.Popen('ess -h',stdout=sp.PIPE,shell=True)).communicate()[0]
print "--------------------------------"
print "**ess**"
print "--------------------------------\n"
if len(essoutput)!=0:
   print "::\n"
print "    "+essoutput.replace("\n","\n    ")
if '{' in essoutput and '}' in essoutput:
    subcommands = essoutput.partition('{')[2].partition('}')[0]
    # print(subcommands)
for subcommand in subcommands.split(','):
    # print subcommand
#    essoutput=subcommand #TEMPORARY, REMOVE   
    essoutput=(sp.Popen('ess {0} -h'.format(subcommand),stdout=sp.PIPE,shell=True)).communicate()[0]
    # print essoutput
    if '{' in essoutput and '}' in essoutput:
        subcommands2 = essoutput.partition('{')[2].partition('}')[0]
        # print(subcommands2)
        print "--------------------------------"
        print "**ess {0}**".format(subcommand)
        print "--------------------------------\n"
        for subcommand2 in subcommands2.split(','):
            # print subcommand2
#            essoutput=subcommand2 #TEMPORARY, REMOVE   
            essoutput=(sp.Popen('ess {0} {1} -h'.format(subcommand,subcommand2),stdout=sp.PIPE,shell=True)).communicate()[0]
            print "+++++++++++++++++++++++++++++++++"
            print "``ess {0} {1}``".format(subcommand,subcommand2)
            print "+++++++++++++++++++++++++++++++++\n"
            if len(essoutput)!=0:
               print "::\n"
            print "    "+essoutput.replace("\n","\n    ")
            if subcommand == "cluster" or subcommand == "server":
               print "**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_\n    "
            elif subcommand == "stream" or subcommand == "exec":
               print "**See Also:** :doc:`../tables/index`\n    "


    else:
      print "--------------------------------"
      print "**ess {0}**".format(subcommand)
      print "--------------------------------\n"
      if len(essoutput)!=0:
         print "::\n"
      print "    "+essoutput.replace("\n","\n    ")
      if subcommand == "cluster" or subcommand == "server":
         print "**See Also:** `Advanced Options <essentia-ref.html#advanced-options>`_\n    "
      elif subcommand == "stream" or subcommand == "exec":
         print "**See Also:** :doc:`../tables/index`\n    "


