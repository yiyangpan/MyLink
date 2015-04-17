git pull
git add --all
git commit -m "`curl -s http://whatthecommit.com/index.txt`"
echo "`curl -s http://whatthecommit.com/index.txt`" > msg.txt
git push
