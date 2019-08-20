# To update to a new github branch (version), fetch and checkout the new branch and then follow the steps at the bottom of this script.

# Set your github username and password in the following file
source other/gitcred.sh
version=`git branch | grep \* | awk '{printf $2}'`

echo -e "\nRunning $1 for essentia docs version $version\n"

if [ -n "$version" ]
then

 cd ~/essentia_docs
 c1="git pull https://$username:$password@github.com/auriq/essentia_docs.git $version"
 c2="rm -R _build/html/*"
 c3="make html"
 c4="sudo cp -R _build/html/* /var/www/html/documentation/."
 c5="sudo cp source/screenshots/*.png /var/www/html/documentation/source/screenshots/"

 c6="git push https://$username:$password@github.com/auriq/essentia_docs.git $version"
 
 c7="rm -rf source/EssentiaPublic/"
 c8="cp -R ../EssentiaPublic source/"

 if [ "$1" = "echo" ]
 then

  echo "$c1"; echo "$c2"; echo "$c3"; echo "$c4"; #echo "$c5";

 elif [ "$1" = "update" ]
 then

  $c1
  $c2
  $c3
  $c4

 elif [ "$1" = "screenshots" ]
 then

  $c5

 elif [ "$1" = "pull" ]
 then

  $c1

 elif [ "$1" = "push" ]
 then

  $c6

 elif [ "$1" = "sync" ]
 then

  $c1
  $c6

 elif [ "$1" = "make" ]
 then

  $c2
  $c3

 elif [ "$1" = "EssentiaPublic" ]
 then

  $c7
  $c8

 else

  echo "Version: $version"; echo "Argument Options are: echo, update, screenshots, pull, push, sync, and EssentiaPublic";

 fi

fi

### Or switch to previous branch (such as 4.0.0), run lines 1,2,3 with that branch, and then run:
###  sudo mkdir /var/www/html/documentation/4.0.0/
###  sudo cp -R _build/html/* /var/www/html/documentation/4.0.0/.
### Then run this file again with the new branch using the normal method

### For running lines 1,2,3 you can run "bash other/update-commands.sh pull" then "bash other/update-commands.sh make"
