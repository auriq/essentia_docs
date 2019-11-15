# make sure to stop and clear existing database and schema if any
ess udbd stop
ess server reset

ess drop database totalwinnings
ess create database totalwinnings # create database

# create schema for vector
ess create vector myvector s,pkey:user i,+max:bet f,+add:winnings

# start udb server
ess udbd start

# set local as datastore
ess select local

# define category
ess category add casino "$HOME/EssentiaPublic/*onlinecasino*" --dateregex none

# display the datastore's summary
ess summary

ess stream casino "*" "*" "aq_pp -f,+1,eok - -d s:user X i:bet f:winnings X -imp totalwinnings:myvector" --debug

ess exec "aq_udb -exp totalwinnings:myvector -o totalwinnings.csv" --debug
