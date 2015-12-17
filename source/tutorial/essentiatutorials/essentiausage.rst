*************************
Essentia Usage: ETL
*************************

ess select s3://BUCKET --credentials=PATH/TO/CREDENTIALFILE
#ess select blob://BUCKET --credentials=PATH/TO/CREDENTIALFILE
#ess select local

ess category add CATEGORY_NAME CATEGORY_PATTERN [OPTIONS]

ess stream CATEGORY_NAME "START_DATE" "END_DATE" "COMMAND(s)" [OPTIONS]
#ess stream CATEGORY_NAME "*" "*" "COMMAND(s)" [OPTIONS]

***************************
Essentia Usage: Load Redshift
***************************



*************************
Essentia Usage: Load R
*************************



*****************************
Essentia Usage: Distribute Data
*****************************