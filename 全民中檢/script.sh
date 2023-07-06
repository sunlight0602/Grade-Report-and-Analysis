pyinstaller --onefile main_windows.py
mkdir ./dist/output_files
cp -R ./input_files ./dist/input_files

cp -R ./output_files/assets ./dist/output_files/assets
mkdir ./dist/output_files/static

cp ./README_client.txt ./dist/README_client.txt

# Change .exe file name
cp ./dist/combine ./dist/start.exe
rm ./dist/combine