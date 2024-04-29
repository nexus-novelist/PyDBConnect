cd ../../data
echo Running this script will generate a basic project
echo "Project Name: "
read project_name
mkdir $project_name

cd $project_name

echo '{
    "1": [{
        "Name": "Document 1"
    }],
    "2": [{
        "Name": "Document 2"
    }]
}' > "collection.json"