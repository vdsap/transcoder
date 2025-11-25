import os
import json
from os import system
from os import path
from os import mkdir
import datetime
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO")

logger.info("Convertor started")


def mtime(_path, _up_folder_path) -> str:
    _mtime = os.path.getmtime(f"{_up_folder_path}{_path}")
    _time = str(datetime.datetime.fromtimestamp(_mtime))
    return _time.split('.')[0]


def is_context_menu():
    if len(sys.argv) > 1 and path.exists(sys.argv[1]):
        return True
    else:
        return False


if not path.exists(f"{os.path.dirname(sys.executable)}\\config.json"):
    logger.debug("config.json not found, creating new one")
    _save_loc_ = input(
        "Where do you want to save the files?/Output folder\nYou don't need to create it, just enter name in format ("
        "C:\\Users\\User\\Desktop\\Output): ")
    if _save_loc_[-1] != "\\":
        _save_loc_ += "\\"
    with open(f"{os.path.dirname(sys.executable)}\\config.json", "w") as f:
        json.dump({"saves_location": _save_loc_}, f)


def is_folder_selected(_file_path):
    if path.isfile(_file_path):
        logger.debug(f"file: {_file_path}")
        return "file"
    elif path.isdir(_file_path):
        logger.debug(f"dir: {_file_path}")
        return "dir"


def conf_init():
    try:
        with open(f"{os.path.dirname(sys.executable)}\\config.json", "r") as f:
            logger.debug("config.json found, loading")
            config = json.load(f)
            _save_loc = config["saves_location"]
            if not path.exists(_save_loc):
                logger.debug("Output folder not found, creating new one")
                mkdir(_save_loc)
            return _save_loc
    except FileNotFoundError:
        logger.error("Invalid Destination")
        os.remove(f"{os.path.dirname(sys.executable)}\\config.json")
        logger.warning("Restart Transcoder and Enter a valid destination")


def main_thread(_file_path, context_mode):
    while True:
        save_loc = conf_init()
        if not save_loc:
            break
        # режим
        mode = input('mode transcode with less bitrate[ ] or copy video[1]: ')
        if mode == '':
            mode = '0'
            logger.info('transcode mode')
            print('transcode')
        if mode == '0':
            bv = input('bitrate {}M: ')
            if bv == '':
                logger.debug('bitrate 2M')
                bv = 2
                print('2M')

        inp = None
        sname = None
        time1 = None
        time0 = None

        # выбор файла или всей папки
        while True:
            logger.debug("file or folder selection")
            file_names = []
            if context_mode:
                up_folder_path = ""
                if is_folder_selected(_file_path) == "file":
                    file_names.append(_file_path)
                else:
                    files = os.listdir(_file_path)
                    print("files to transcode:")
                    print('Name and modified time')
                    for i in files:
                        if len(i.split('.')) > 1:
                            if i.split('.')[1] == 'mkv' or i.split('.')[1] == 'mp4':
                                file_names.append(i)
                                print(f'{i}     {mtime(_file_path+"\\"+i, up_folder_path)}')

            else:
                up_folder_path = "..\\"
                print('You want to transcode a file or a whole folder?')
                folder = input('file[1] or folder[]: ')
                if folder == '':
                    logger.debug("folder mode")
                    folder = '0'
                    print('folder')
                else:
                    logger.debug("file mode")
                    print('file')
                    print(
                        'Enter the name of the file you want to transcode (without extension if .mkv) or press Enter to '
                        'return')

                if folder == '1':
                    logger.debug("file selection")
                    print('Name and modified time')
                    for i in os.listdir("..\\"):
                        if len(i.split('.')) > 1:
                            if i.split('.')[1] == 'mkv' or i.split('.')[1] == 'mp4':
                                print(f'{i}     {mtime(i, up_folder_path)}')
                    name = input('-i ')
                    file_names.append(name)
                    if name == ['']:
                        break
                elif folder == '0':
                    logger.debug("folder selected")
                    files = os.listdir("..\\")
                    print("files to transcode:")
                    print('Name and modified time')
                    for i in files:
                        if len(i.split('.')) > 1:
                            if i.split('.')[1] == 'mkv' or i.split('.')[1] == 'mp4':
                                file_names.append(i)
                                print(f'{i}     {mtime(i, up_folder_path)}')

            # выбор времени
            logger.debug("time selection")
            time0 = input('start seconds {}: ')
            time1 = input('time to transcode in mm:ss {}: ')
            if time1 != '':
                time1 = int(time1.split(':')[0]) * 60 + int(time1.split(':')[1])
            else:
                time1 = None
            if time0 == '':
                time = None
            else:
                time0 = int(time0)

            # транскодирование
            for i in file_names:
                logger.info(f"transcoding file {i}...")
                start_command = 'ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 2'
                add_command = '-c:a copy -c:v hevc_nvenc -map 0 -preset p7 -strict -2'
                if context_mode:
                    i = i.split("\\")[-1]
                    if len(i.split(".")) > 1:
                        fname = i.split(".")[0]
                        sname = i.split(".")[1]
                    elif len(i.split(".")) == 1:
                        name = i
                    if is_folder_selected(_file_path) == "dir":
                        full_file_path = _file_path+"\\"
                    else:
                        full_file_path = ''
                else:
                    if len(i.split(".")) > 1:
                        fname = i.split(".")[0]
                        sname = i.split(".")[1]
                    elif len(i.split(".")) == 1:
                        name = i
                    full_file_path = ''
                print(f"\n\ntranscoding file {i}...\n\n")
                if mode == '0':
                    logger.debug("transcoding with less bitrate")

                    # если время указано
                    if time0 and time1:
                        logger.debug("both times specified")
                        if not sname:
                            logger.debug('mkv file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{name}.mkv" {add_command} -b:v {bv}M -ss {time0} -t {time1}  -y "{save_loc}{name}.{bv}M.ss{time0}.t{time1}.mp4" """)
                            print(f'\n{save_loc}{name}.{bv}M.ss{time0}.t{time1}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{fname}.{sname}" {add_command} -b:v {bv}M -ss {time0} -t {time1}  -y "{save_loc}{fname}.{bv}M.ss{time0}.t{time1}.mp4" """)
                            print(f'\n{save_loc}{fname}.{bv}M.ss{time0}.t{time1}.mp4\n')

                    elif time0 and not time1:
                        logger.debug("start time specified")
                        if not sname:
                            logger.debug('mkv file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{name}.mkv" {add_command} -b:v {bv}M -ss {time0} -y "{save_loc}{name}.{bv}M.ss{time0}.mp4" """)
                            print(f'\n{save_loc}{name}.{bv}M.ss{time0}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{fname}.{sname}" {add_command} -b:v {bv}M -ss {time0}  -y "{save_loc}{fname}.{bv}M.ss{time0}.mp4" """)
                            print(f'\n{save_loc}{fname}.{bv}M.ss{time0}.mp4\n')

                    elif time1 and not time0:
                        logger.debug("duration specified")
                        if not sname:
                            logger.debug('mkv file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{name}.mkv" {add_command} -b:v {bv}M -t {time1}  -y "{save_loc}{name}.{bv}M.t{time1}.mp4" """)
                            print(f'\n{save_loc}{name}.{bv}M.t{time1}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{fname}.{sname}" {add_command} -b:v {bv}M -t {time1}  -y "{save_loc}{fname}.{bv}M.t{time1}.mp4" """)
                            print(f'\n{save_loc}{fname}.{bv}M.t{time1}.mp4\n')

                    # если не указано время
                    elif not time0 and not time1:
                        logger.debug("no time specified")
                        if not sname:
                            logger.debug('mkv file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{name}.mkv" {add_command} -b:v {bv}M  -y "{save_loc}{name}.{bv}M.mp4" """)
                            print(f'\n{save_loc}{name}.{bv}M.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{fname}.{sname}" {add_command} -b:v {bv}M  -y "{save_loc}{fname}.{bv}M.mp4" """)
                            print(f'\n{save_loc}{fname}.{bv}M.mp4\n')

                # обрезка
                if mode == '1':
                    logger.info("cutting mode")
                    if time0 and time1:
                        logger.debug("both times specified")
                        if not sname:
                            logger.debug('mkv file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{name}.mkv" -map 0 -c copy -ss {time0} -t {time1}  -y "{save_loc}{name}.ss{time0}.t{time1}.mp4" """)
                            print(f'\n{save_loc}{name}.ss{time0}.t{time1}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{fname}.{sname}" -map 0 -c copy -ss {time0} -t {time1}  -y "{save_loc}{fname}.ss{time0}.t{time1}.mp4" """)
                            print(f'\n{save_loc}{fname}.ss{time0}.t{time1}.mp4\n')

                    elif time0 and not time1:
                        logger.debug("start time specified")
                        if not sname:
                            logger.debug('mkv file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{name}.mkv" -map 0 -c copy -ss {time0}  -y "{save_loc}{name}.ss{time0}.mp4" """)
                            print(f'\n{save_loc}{name}.ss{time0}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{fname}.{sname}" -map 0 -c copy -ss {time0}  -y "{save_loc}{fname}.ss{time0}.mp4" """)
                            print(f'\n{save_loc}{fname}.ss{time0}.mp4\n')

                    elif time1 and not time0:
                        logger.debug("duration specified")
                        if not sname:
                            logger.debug('mkv file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{name}.mkv" -map 0 -c copy -t {time1}  -y "{save_loc}{name}.t{time1}.mp4" """)
                            print(f'\n{save_loc}{name}.t{time1}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" {start_command} -i "{full_file_path}{up_folder_path}{fname}.{sname}" -map 0 -c copy -t {time1}  -y "{save_loc}{fname}.t{time1}.mp4" """)
                            print(f'\n{save_loc}{fname}.t{time1}.mp\n')

            logger.info("transcoding completed")
            print("Do you want to delete original files? (y/N)")
            del_ans = input()
            if del_ans == 'y' or del_ans == 'Y':
                for i in file_names:
                    if context_mode and is_folder_selected(_file_path) == "dir":
                        if len(i.split(".")) == 1:
                            i = i + '.mkv'
                        os.remove(_file_path+ "\\" + i)
                    else:
                        if len(i.split(".")) == 1:
                            i = i + '.mkv'
                        os.remove("..\\" + i)
                logger.warning('Original files deleted')
            else:
                logger.info('Original files not deleted')
                print('Transcoding completed')


if __name__ == "__main__":
    if is_context_menu():
        logger.debug("context mode")
        file_path = sys.argv[1]
        logger.debug(file_path)
        main_thread(file_path, context_mode=True)
    else:
        logger.debug("exe mode")
        file_path = None
        main_thread(file_path, context_mode=False)
    os.system("pause")
    logger.info("exit")
