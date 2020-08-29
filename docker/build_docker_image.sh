rm -rf app  &&
mkdir app  &&
cp ../app.py app/app.py   &&
cp -r ../conf  app/conf    &&
cp -r ../conf  ../MyTools/data/mytools/    &&
cp -r ../files  app/files    &&
cp -r ../template  app/template    &&
cp -r ../tools  app/tools    &&
cp -r ../route  app/route    &&
cp ../requirement.txt app/requirement.txt  &&
docker build -t uncleYiba/mytools_jingjian:20190926_121913 .  &&
docker push uncleYiba/mytools_jingjian:20190926_121913  &&
rm -rf app




