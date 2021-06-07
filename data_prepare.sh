clip=./clip_with_marks.py
python3 $clip

mdir dev test

data_dir=/data/dataset/sichuan_aishell_with_marks
file_list=$(python3 file_list.py)
is_dev=true
for line in $file_list
do
	if test $line = test
	then
		echo "start processing test data!"
		is_dev=false
		continue

	fi
	
	file=$data_dir/$line
	if $is_dev
	then 
		echo mv $file $data_dir/dev/
	else
		echo mv $file $data_dir/test/
	fi
done


mkdir train
mv S* ./train

mkdir aishell
mkdir aishell/transcript
mkdir aishell/wav

mv dev aishell/wav
mv train aishell/wav
mv test aishell/wav

mv *.txt aishell/transcript
echo aishell-shape dataset prepared
echo All done
