#!/bin/bash

# Ensure project name is given
if [ -z "$1" ]; then
    echo "Please provide a project name."
    exit 1
fi

project_name=$1
work_dir=~/projects
project_dir=${work_dir}/${project_name}
template_dir=${work_dir}/Project_Template
env_name=${project_name}_env

cd $work_dir
npx create-react-app $project_name

cd $project_name
cp -r ${template_dir}/react/* .
# Replace project name in package.json
# Filthy hack for OSX compatibility.
sed "s/PROJECT_NAME/${project_name}/g" package.json > new_package.json
sed "s/ENV_NAME/${env_name}/g" new_package.json > temp.json && mv temp.json new_package.json
mv new_package.json package.json
npm install

mkdir backend
cd backend
cp -r ${template_dir}/flask/* .

python3 -m venv "${project_name}_env"
source ./${project_name}_env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
deactivate

cd ..
echo -e "backend/${project_name}_env\nbackend/__pycache__" >> .gitignore