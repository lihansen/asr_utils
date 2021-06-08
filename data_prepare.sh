#clip=./clip_with_marks.py
#python3 $clip


data_dir=/data/dataset/sichuan_aishell_with_marks
cd $data_dir
mkdir dev test
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
	
	file=$line
	if $is_dev
	then 
		mv $file dev/
	else
		mv $file test/
	fi
done

mkdir train
mv S* train

mkdir aishell
mkdir aishell/transcript
mkdir aishell/wav

mv dev aishell/wav
mv train aishell/wav
mv test aishell/wav

mv aishell_transcript*.txt aishell/transcript/

echo All done
