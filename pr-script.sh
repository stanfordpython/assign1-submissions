# This script automates the creation of pull requests for students
while read id; do
  git checkout master
  git checkout -b $id
  cd ../
  folderName="$id-assign1"
  cp -rf "assign1/$folderName" "assign1-submissions/$folderName"
  cd assign1-submissions
  git add .
  git commit -m "added submission for $id"
  git push origin $id
  echo "created PR for $id"
  rm -rf "$folderName"
done <sunetids.txt