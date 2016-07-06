directory="output"
size=70
files=$(find $directory | grep svg | grep -v thumb)
for file in $files; do 
  filename=$(basename $file)
  extension="${filename##*.}"
  filename="${filename%.*}"
  thumbname=$filename"-thumb".$extension
  svg-resize.py --width=$size --height=$size $file $directory/$thumbname
done
