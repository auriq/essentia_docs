version=`git branch | grep \* | awk '{printf $2}'`

if [ "$1" = "update" ]
then

git pull https://bwaxer:dragon911@github.com/auriq/essentia_docs.git $version
rm -R _build/html/*
make html
sudo cp -R _build/html/* /var/www/html/documentation/.
#sudo cp source/screenshots/*.png /var/www/html/documentation/source/screenshots/

fi

### Or switch to previous branch, run lines 1,2,3 with that branch, and then run:
###  sudo mkdir /var/www/html/documentation/3.1.1/
###  sudo cp -R _build/html/* /var/www/html/documentation/3.1.1/.
### Then run this file again with the new branch using the normal method
