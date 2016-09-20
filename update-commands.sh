version=`git branch | grep \* | awk '{printf $2}'`

if [ -n "$version" ]
then

 c1="git pull https://bwaxer:dragon911@github.com/auriq/essentia_docs.git $version"
 c2="rm -R _build/html/*"
 c3="make html"
 c4="sudo cp -R _build/html/* /var/www/html/documentation/."
 c5="sudo cp source/screenshots/*.png /var/www/html/documentation/source/screenshots/"

 c6="git push https://bwaxer:dragon911@github.com/auriq/essentia_docs.git $version"

 if [ "$1" = "echo" ]
 then

  echo "$c1"; echo "$c2"; echo "$c3"; echo "$c4"; #echo "$c5";

 elif [ "$1" = "update" ]
 then

  $c1
  $c2
  $c3
  $c4
  # $c5

 elif [ "$1" = "sync" ]
 then

  $c1
  $c6

 fi

else

 echo "Version: $version"; echo "Argument Options are: echo, update, and sync";

fi

### Or switch to previous branch, run lines 1,2,3 with that branch, and then run:
###  sudo mkdir /var/www/html/documentation/3.1.1/
###  sudo cp -R _build/html/* /var/www/html/documentation/3.1.1/.
### Then run this file again with the new branch using the normal method
