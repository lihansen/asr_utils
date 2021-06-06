import shutil
import wave
import textgrid
import os
import re

max_sentence_length = 100


def clipping(wavepath, out_dir, file_num):
    """
    clip dialect wave into multiple clips based on intervals,
    each clips may contain several intervals,
    the total length of clip sentences will be no more than @max_sentence_length

    :param wavepath: sichuan dialect wave path
    :param out_dir: dir to out put
    :param file_num: wave file number of sichuan dialect
    :return:
    """
    tg_path = wavepath.replace(".wav", ".TextGrid")

    try:
        tg = textgrid.TextGrid().fromFile(tg_path)
    except BaseException as e:
        print_error(tg_path, str(e))
    else:
        transcript_lines = []
        clip_num = 121

        clip_sentence = ""
        clip_wavedata = []

        with wave.open(wavepath, "rb") as wave_file:
            nchannels, sampwidth, framerate, nframes = wave_file.getparams()[:4]

            for intervals in tg:
                for interval in intervals:
                    # clear bad chars
                    interval_sentence = re.sub(r"[^\u4e00-\u9fa5！。，？]", "", interval.mark)
                    # skip bad cases, such as: "", "重叠", "嗯。".
                    if len(interval.mark) > 2:

                        # save previous short intervals as a single clip
                        # if the total length of the clip sentence is going to above 100
                        if len(clip_sentence) + len(interval_sentence) >= max_sentence_length:
                            clip_name = save_clip(out_dir, file_num, clip_num, b"".join(clip_wavedata))
                            transcript_lines.append("".join([clip_name, " ", clip_sentence, "\n"]))
                            clip_num += 1
                            clip_sentence = ""
                            clip_wavedata.clear()

                        # cache this short interval wave data and sentence.
                        start = round(interval.minTime * framerate)
                        end = round(interval.maxTime * framerate)
                        wave_file.setpos(start)
                        interval_wavedata = wave_file.readframes(end - start)

                        clip_wavedata.append(interval_wavedata)
                        clip_sentence += interval_sentence

                if clip_sentence > "":
                    clip_name = save_clip(out_dir, file_num, clip_num, b"".join(clip_wavedata))
                    transcript_lines.append("".join([clip_name, " ", clip_sentence, "\n"]))
                    clip_num += 1
                    clip_sentence = ""
                    clip_wavedata.clear()

        return transcript_lines


def save_clip(root_dir, file_num, clip_num, wave_data):
    """
    1. construct the clip file name, shape as: BAC009S0000W0000
    2. save clip
    :param root_dir: where to save all these generating clips
    :param file_num:
    :param clip_num:
    :param wave_data: bytes
    :return: None
    """
    folder_code = "S" + ("0000" + str(file_num))[-4:]
    clip_code = "W" + ("0000" + str(clip_num))[-4:]
    clip_name = "BAC009" + folder_code + clip_code
    folder_path = os.path.join(root_dir, folder_code)
    clip_path = os.path.join(folder_path, clip_name) + ".wav"

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with wave.open(clip_path, "wb") as clip_file:
        clip_file.setnchannels(1)
        clip_file.setsampwidth(2)
        clip_file.setframerate(16000)
        clip_file.writeframes(wave_data)

    print(clip_path)
    return clip_name


def walk(path, output_dir):
    file_num = 2
    transcript_path = os.path.join(output_dir, "aishell_transcript_v0.8.txt")

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".wav"):
                wavepath = os.path.join(root, file)
                try:
                    transcript_lines = clipping(wavepath, output_dir, file_num)

                    with open(transcript_path, "a+", encoding="utf8") as transcript:
                        transcript.writelines(transcript_lines)

                    file_num += 1
                except BaseException as e:
                    print_error(wavepath, str(e))


def creat_dir_trees(root_dir):
    aishell = os.path.join(root_dir, "aishell")
    transcript = os.path.join(aishell, "transcript")
    wav = os.path.join(aishell, "wav")
    dev = os.path.join(wav, "dev")
    test = os.path.join(wav, "test")
    train = os.path.join(wav, "train")
    for item in [aishell, transcript, wav, dev, test, train]:
        if not os.path.exists(item):
            os.mkdir(item)

    return aishell, transcript, wav, dev, test, train


def print_error(filepath, error_msg):
    with open("errors.txt", "a+", encoding="utf8") as error_file:
        print(filepath, error_msg)
        errors = [filepath, error_msg, "\n"]
        error_file.writelines(errors)


if __name__ == "__main__":
    # error output
    err_file = "error.txt"
    if os.path.exists(err_file):
        shutil.rmtree("error.txt")
    if os.path.exists("output"):
        shutil.rmtree("output")
        os.mkdir("output")
    walk("dataset", "output")

