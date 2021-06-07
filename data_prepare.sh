clip=./clip_with_marks.py
python3 $clip

mkdir dev test

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

mkdir $data_dir/train
mv $data_dir/S* ./train

mkdir $data_dir/aishell
mkdir $data_dir/aishell/transcript
mkdir $data_dir/aishell/wav

mv $data_dir/dev $data_dir/aishell/wav
mv $data_dir/train $data_dir/aishell/wav
mv $data_dir/test $data_dir/aishell/wav

mv $data_dir/aishell_transcript*.txt $data_dir/aishell/transcript/

echo aishell-shape dataset prepared
echo All done
