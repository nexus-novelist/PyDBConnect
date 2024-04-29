cd ../../data/
echo Running this script will generate a basic project 
set /p projectName=Project Name: 
mkdir %projectName%

cd %projectName%
(
echo {
echo     "1": [{
echo         "Name": "Document 1"
echo     }],
echo     "2": [{
echo         "Name": "Document 2"
echo     }]
echo }
) > collection.json
echo Project generated