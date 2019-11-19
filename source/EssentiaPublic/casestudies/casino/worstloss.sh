# setting essentia's cluster platform to local (master node only)
ess cluster set local

# stopping database and deleting the schema if already exist
ess udbd stop
ess server reset

ess drop database worstloss

# create database and table, with schema and attributes for each colunm
ess create database worstloss
ess create table grouping s,pkey:country s,+key:user s,+first:time i,+last:bet f,+min:winnings

# start the udb
ess udbd start

ess select local

ess category add casino "$HOME/EssentiaPublic/*onlinecasino*" --dateregex none

ess summary

# stream the data from category into worstloss database
ess stream casino "*" "*" "aq_pp -f,+1,eok - -d s:user s:time i:bet f:winnings s:country -udb -imp worstloss:grouping" --debug

# order the data based on winnings column
ess exec "aq_udb -ord worstloss:grouping winnings" --debug
# output to csv file
ess exec "aq_udb -exp worstloss:grouping -o worstloss.csv" --debug
