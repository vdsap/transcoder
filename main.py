import os
import subprocess,json
from os import system
from os import path
from os import mkdir

if not path.exists("config.json"):
    save_loc=input("Where do you want to save the files?/Output folder\nYou don't need to create it, just enter name in format (C:\\Users\\User\\Desktop\\Output): ")
    if save_loc[-1]!="\\": save_loc+="\\"
    with open("config.json", "w") as f:
        json.dump({"saves_location": save_loc}, f)

with open("config.json", "r") as f:
    config = json.load(f)
    save_loc=config["saves_location"]
    if not path.exists(save_loc):
        mkdir(save_loc)
    while True:
        #режим
        mode = input('mode transcode with less bitrate[ ] or copy video[1]: ')
        if mode == '':
            mode = '0'
            print('passcode')
        if mode == '0':
            bv = input('bitrate {}M: ')
            if bv == '':
                bv = 2
                print('2M')

        inp = None
        Sname = None
        time1 = None
        time0 = None
        fileNames = []

        #выбор файла или всей папки
        while True:
            print('You want to transcode a file or a whole folder?')
            folder = input('file[1] or folder[]: ')
            if folder == '':
                folder = '0'
                print('folder')
            else:
                print('file')
                print('Enter the name of the file you want to transcode (without extension if .mkv) or press Enter to return')

            if folder == '1':
                name = input('-i ')
                fileNames.append(name)
                if name == ['']: break
            elif folder == '0':
                files = os.listdir()
                for i in files:
                    if i.split('.')[1] == 'mkv'or i.split('.')[1] == 'mp4':
                        fileNames.append(i)





            #выбор времени
            time0 = input('start seconds {} ')
            time1 = input('time to transcode in mm:ss {}: ')
            if time1 != '':
                time1 = str(int(time.split()[1].split(':')[0])*60+int(time.split()[1].split(':')[1]))
            if time0 == '':
                time = None
            else: time0 = int(time0)
            if time1 == '':
                time1 = None
            else: time1 = int(time1)

            # транскодирование
            for i in fileNames:
                if len(i.split()) > 1:
                    Fname = i[0]
                    Sname = i[1]
                elif len(i.split()) == 1:
                    name = i[0]
                if mode == '0':
                    # если время указано
                    if time != None:
                        if time0>0 and time1:
                            if not Sname:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:v hevc_nvenc -preset slow -b:v {bv}M -ss {time0} -t {time1}  -y "{save_loc}{name}.{bv}M.ss{time0}.t{time1}.mp4" """)
                                print(f'\n{save_loc}\{name}.{bv}M.ss{time0}.t{time1}.mp4\n')

                            else:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c:v hevc_nvenc -preset slow -b:v {bv}M -ss {time0} -t {time1}  -y "{save_loc}{Fname}.{bv}M.ss{time0}.t{time1}.mp4" """)
                                print(f'\ntemp_completed\{Fname}.{bv}M.ss{time0}.t{time1}.mp4\n')

                        elif time0 and not time1:
                                if not Sname:
                                    system(
                                        f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:v hevc_nvenc -preset slow -b:v {bv}M -ss {time0}  -y "{save_loc}{name}.{bv}M.ss{time0}.mp4" """)
                                    print(f'\ntemp_completed\{name}.{bv}M.ss{time0}.mp4\n')

                                else:
                                    system(
                                        f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c:v hevc_nvenc -preset slow -b:v {bv}M -ss {time0}  -y "{save_loc}{Fname}.{bv}M.ss{time0}.mp4" """)
                                    print(f'\ntemp_completed\{Fname}.{bv}M.ss{time0}.mp4\n')

                        elif time1 and time0 == 0:
                            if not Sname:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:v hevc_nvenc -preset slow -b:v {bv}M -t {time1}  -y "{save_loc}{name}.{bv}M.t{time1}.mp4" """)
                                print(f'\ntemp_completed\{name}.{bv}M.t{time1}.mp4\n')

                            else:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c:v hevc_nvenc -preset slow -b:v {bv}M -t {time1}  -y "{save_loc}{Fname}.{bv}M.t{time1}.mp4" """)
                                print(f'\ntemp_completed\{Fname}.{bv}M.t{time1}.mp4\n')

                    # если не указано время
                    else:
                        if not Sname:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:v hevc_nvenc -preset slow -b:v {bv}M  -y "{save_loc}{name}.{bv}M.mp4" """)
                            print(f'\ntemp_completed\{name}.{bv}M.mp4\n')

                        else:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Fname+'.'+Sname}" -c:v hevc_nvenc -preset slow -b:v {bv}M  -y "{save_loc}{Fname}.{bv}M.mp4" """)
                            print(f'\ntemp_completed\{Fname}.{bv}M.mp4\n')

                # обрезка
                if mode == '1':
                    if time != None:
                        if time0>0 and time1:
                            if not Sname:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c copy -ss {time0} -t {time1}  -y "{save_loc}{name}.ss{time0}.t{time1}.mp4" """)
                                print(f'\ntemp_completed\{name}.ss{time0}.t{time1}.mp4\n')

                            else:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c copy -ss {time0} -t {time1}  -y "{save_loc}{Fname}.ss{time0}.t{time1}.mp4" """)
                                print('f\ntemp_completed\{Fname}.ss{time0}.t{time1}.mp4\n')

                        elif time0 and not time1:
                                if not Sname:
                                    system(
                                        f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c copy -ss {time0}  -y "{save_loc}{name}.ss{time0}.mp4" """)
                                    print('f\ntemp_completed\{name}.ss{time0}.mp4\n')

                                else:
                                    system(
                                        f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c copy -ss {time0}  -y "{save_loc}{Fname}.ss{time0}.mp4" """)
                                    print('f\ntemp_completed\{Fname}.ss{time0}.mp4\n')

                        elif time1 and time0 == 0:
                            if not Sname:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c copy -t {time1}  -y "{save_loc}{name}.t{time1}.mp4" """)
                                print('f\ntemp_completed\{name}.t{time1}.mp4\n')

                            else:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c copy -t {time1}  -y "{save_loc}{Fname}.t{time1}.mp4" """)
                                print('f\ntemp_completed\{Fname}.t{time1}.mp\n')

            print("Do you want to delete original files? (Y/n)")
            del_ans = input()
            if del_ans == 'y' or del_ans == '':
                for i in fileNames:
                    if len(i.split(".")) ==1:
                        i = i + '.mkv'
                    os.remove(i)
                print('Original files deleted')
            else: prinf('Transcoding completed')