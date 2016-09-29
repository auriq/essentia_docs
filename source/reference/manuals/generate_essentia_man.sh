essmain=""
#echo -e $essmain
confman="man_pages = [\n
    ('ess', 'ess', u'',\n
     [u'AuriQ Systems Inc.'], 1),\n"
#echo -e $confman
#'generate_essentia_ref'
for file in `ls ess-*.rst | sed 's/.rst//g'`
do
 addtoess="\n:manpage:\`${file}(1)\`\n"
 addtoconf="    ('$file', '$file', u'',\n
     [u'AuriQ Systems Inc.'], 1),\n"
 essmain="${essmain}${addtoess}"
 confman="${confman}${addtoconf}"
 # echo -e $file $confman
done

confman="$confman
]\n
\n
# If true, show URL addresses after external links.\n
#man_show_urls = False\n"
echo -e $essmain >> ess.rst
echo -e $confman



# remove old form of this from conf.py then run this script and copy the output to the end of conf.py
# make man
#ll /usr/share/man/man1/ | grep ess
#sudo cp _build/man/ess* /usr/share/man/man1/.
#man ess

