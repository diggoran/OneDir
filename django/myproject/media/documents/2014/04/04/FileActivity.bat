# assume testFile.txt is in the parent directory

# move testFile from parent directory to current directory 
cp ../testFile.txt .
sleep 5

# rename testFile to file2
mv testFile.txt file2.txt
sleep 5

# make folder subdir and copy file2 into it?
mkdir subdir
cp file2.txt subdir
sleep 5