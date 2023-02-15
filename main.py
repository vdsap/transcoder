import os
import subprocess,json
from os import system
from os import path
from os import mkdir
from loguru import logger

logger.info("Convertor started")

if not path.exists("config.json"):
    logger.debug("config.json not found, creating new one")
    save_loc=input("Where do you want to save the files?/Output folder\nYou don't need to create it, just enter name in format (C:\\Users\\User\\Desktop\\Output): ")
    if save_loc[-1]!="\\": save_loc+="\\"
    with open("config.json", "w") as f:
        json.dump({"saves_location": save_loc}, f)

with open("config.json", "r") as f:
    logger.debug("config.json found, loading")
    config = json.load(f)
    save_loc=config["saves_location"]
    if not path.exists(save_loc):
        logger.debug("Output folder not found, creating new one")
        mkdir(save_loc)
    while True:
        #режим
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
        Sname = None
        time1 = None
        time0 = None

        #выбор файла или всей папки
        while True:
            logger.debug("file or folder selection")
            fileNames = []
            print('You want to transcode a file or a whole folder?')
            folder = input('file[1] or folder[]: ')
            if folder == '':
                logger.debug("folder mode")
                folder = '0'
                print('folder')
            else:
                logger.debug("file mode")
                print('file')
                print('Enter the name of the file you want to transcode (without extension if .mkv) or press Enter to return')

            if folder == '1':
                logger.debug("file selection")
                for i in os.listdir("..\\"):
                    if len(i.split('.'))> 1:
                        if i.split('.')[1] == 'mkv'or i.split('.')[1] == 'mp4':
                            print(i)
                name = input('-i ')
                fileNames.append(name)
                if name == ['']: break
            elif folder == '0':
                logger.debug("folder selected")
                files = os.listdir("..\\")
                print("files to trancode:")
                for i in files:
                    if len(i.split('.'))> 1:
                        if i.split('.')[1] == 'mkv'or i.split('.')[1] == 'mp4':
                            fileNames.append(i)
                            print(i)

            #выбор времени
            logger.debug("time selection")
            time0 = input('start seconds {}: ')
            time1 = input('time to transcode in mm:ss {}: ')
            if time1 != '':
                time1 = int(time1.split(':')[0])*60+int(time1.split(':')[1])
            else: time1 = None
            if time0 == '':
                time = None
            else: time0 = int(time0)

            # транскодирование
            for i in fileNames:
                logger.info(f"transcoding file {i}...")
                if len(i.split(".")) > 1:
                    Fname = i.split(".")[0]
                    Sname = i.split(".")[1]
                elif len(i.split(".")) == 1:
                    name = i
                print(f"\n\ntranscoding file {i}...\n\n")
                if mode == '0':
                    logger.debug("transcoding with less bitrate")
                    # если время указано
                    if time0 and time1:
                        logger.debug("both times specified")
                        if not Sname:
                            logger.debug('mkv file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:a copy -c:v hevc_nvenc -map 0 -preset p7 -b:v {bv}M -ss {time0} -t {time1}  -y "{save_loc}{name}.{bv}M.ss{time0}.t{time1}.mp4" """)
                            print(f'\n{save_loc}{name}.{bv}M.ss{time0}.t{time1}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Fname}.{Sname}" -c:a copy -c:v hevc_nvenc -map 0 -preset p7 -b:v {bv}M -ss {time0} -t {time1}  -y "{save_loc}{Fname}.{bv}M.ss{time0}.t{time1}.mp4" """)
                            print(f'\n{save_loc}{Fname}.{bv}M.ss{time0}.t{time1}.mp4\n')

                    elif time0 and not time1:
                            logger.debug("start time specified")
                            if not Sname:
                                logger.debug('mkv file')
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:a copy -c:v hevc_nvenc -map 0 -preset p7 -b:v {bv}M -ss {time0}  -y "{save_loc}{name}.{bv}M.ss{time0}.mp4" """)
                                print(f'\n{save_loc}{name}.{bv}M.ss{time0}.mp4\n')

                            else:
                                logger.debug('other type file')
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Fname}.{Sname}" -c:a copy -c:v hevc_nvenc -map 0 -preset p7 -b:v {bv}M -ss {time0}  -y "{save_loc}{Fname}.{bv}M.ss{time0}.mp4" """)
                                print(f'\n{save_loc}{Fname}.{bv}M.ss{time0}.mp4\n')

                    elif time1 and not time0:
                        logger.debug("duration specified")
                        if not Sname:
                            logger.debug('mkv file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:a copy -c:v hevc_nvenc -map 0 -preset p7 -b:v {bv}M -t {time1}  -y "{save_loc}{name}.{bv}M.t{time1}.mp4" """)
                            print(f'\n{save_loc}{name}.{bv}M.t{time1}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Fname}.{Sname}" -c:a copy -c:v hevc_nvenc -map 0 -preset p7 -b:v {bv}M -t {time1}  -y "{save_loc}{Fname}.{bv}M.t{time1}.mp4" """)
                            print(f'\n{save_loc}{Fname}.{bv}M.t{time1}.mp4\n')

                # если не указано время
                    elif not time0 and not time1:
                        logger.debug("no time specified")
                        if not Sname:
                            logger.debug('mkv file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:a copy -c:v hevc_nvenc -map 0 -preset p7 -b:v {bv}M  -y "{save_loc}{name}.{bv}M.mp4" """)
                            print(f'\n{save_loc}{name}.{bv}M.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Fname}.{Sname}" -c:a copy -c:v hevc_nvenc -map 0 -preset p7 -b:v {bv}M  -y "{save_loc}{Fname}.{bv}M.mp4" """)
                            print(f'\n{save_loc}{Fname}.{bv}M.mp4\n')

                # обрезка
                if mode == '1':
                    logger.info("cutting mode")
                    if time0 and time1:
                        logger.debug("both times specified")
                        if not Sname:
                            logger.debug('mkv file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -map 0 -c copy -ss {time0} -t {time1}  -y "{save_loc}{name}.ss{time0}.t{time1}.mp4" """)
                            print(f'\n{save_loc}{name}.ss{time0}.t{time1}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Fname}.{Sname}" -map 0 -c copy -ss {time0} -t {time1}  -y "{save_loc}{Fname}.ss{time0}.t{time1}.mp4" """)
                            print('f\n{save_loc}{Fname}.ss{time0}.t{time1}.mp4\n')

                    elif time0 and not time1:
                        logger.debug("start time specified")
                        if not Sname:
                            logger.debug('mkv file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -map 0 -c copy -ss {time0}  -y "{save_loc}{name}.ss{time0}.mp4" """)
                            print('f\n{save_loc}{name}.ss{time0}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Fname}.{Sname}" -map 0 -c copy -ss {time0}  -y "{save_loc}{Fname}.ss{time0}.mp4" """)
                            print('f\n{save_loc}{Fname}.ss{time0}.mp4\n')

                    elif time1 and not time0:
                        logger.debug("duration specified")
                        if not Sname:
                            logger.debug('mkv file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -map 0 -c copy -t {time1}  -y "{save_loc}{name}.t{time1}.mp4" """)
                            print('f\n{save_loc}{name}.t{time1}.mp4\n')

                        else:
                            logger.debug('other type file')
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Fname}.{Sname}" -map 0 -c copy -t {time1}  -y "{save_loc}{Fname}.t{time1}.mp4" """)
                            print('f\n{save_loc}{Fname}.t{time1}.mp\n')

            logger.info("transcoding completed")
            print("Do you want to delete original files? (y/N)")
            del_ans = input()
            if del_ans == 'y' or del_ans == 'Y':
                for i in fileNames:
                    if len(i.split(".")) ==1:
                        i = i + '.mkv'
                    os.remove("..\\"+i)
                print('Original files deleted')
            else:
                print('Original files not deleted')
                print('Transcoding completed')
