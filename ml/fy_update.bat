@echo off

echo "--------update gamecommon------------"
cd GameCommon
svn update
cd ..

echo "--------update server bin------------"
cd server
svn update
cd ..

echo "--------update scheme doc------------"
cd plan
svn update
cd ..

echo "--------update client bin------------"
cd Client
svn update
cd ..

echo "--------update client src------------"
cd Client_Src
svn update
cd ..

echo "--------update client editor ------------"
cd Client_Editor
svn update
cd ..

pause