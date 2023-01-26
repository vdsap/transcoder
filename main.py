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
        mode = input('mode passcode[ ] or copy[1]: ')
        if mode == '':
            mode = '0'
            print('passcode')
        if mode == '0':
            bv = input('-b:v {}M: ')
            if bv == '':
                bv = 5
                print('5M')

        inp = None
        Sname = None
        time1 = None
        time0 = None

        #имя и время
        while True:
            name = input('-i ').split('.')
            if len(name)>1:
                Fname = name[0]
                Sname = name[1]
            elif len(name)==1 and name[0]!="": name = name[0]
            else:
                break
            time = input('-ss {} -t {}: ')
            if time == '':
                time = None
            else:
                time = time.split()
                time0 = int(time[0])
                if len(time)>1:
                    time1 = int(time[1])

            # транскодирование
            if mode == '0':
                # если время указано
                if time != None:
                    if time0>0 and time1:
                        if not Sname:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:v hevc_nvenc -preset slow -b:v {bv}M -ss {time0} -t {time1}  -y "{save_loc}{name}.{bv}M.ss{time0}.t{time1}.mp4" """)
                            print(f'\ntemp_completed\{name}.{bv}M.ss{time0}.t{time1}.mp4\n')
                            subprocess.Popen(f'explorer /select,"{save_loc}{name}.{bv}M.ss{time0}.t{time1}.mp4"')
                        else:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c:v hevc_nvenc -preset slow -b:v {bv}M -ss {time0} -t {time1}  -y "{save_loc}{Fname}.{bv}M.ss{time0}.t{time1}.mp4" """)
                            print(f'\ntemp_completed\{Fname}.{bv}M.ss{time0}.t{time1}.mp4\n')
                            subprocess.Popen(f'explorer /select,"{save_loc}{Fname}.{bv}M.ss{time0}.t{time1}.mp4"')
                    elif time0 and not time1:
                            if not Sname:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:v hevc_nvenc -preset slow -b:v {bv}M -ss {time0}  -y "{save_loc}{name}.{bv}M.ss{time0}.mp4" """)
                                print(f'\ntemp_completed\{name}.{bv}M.ss{time0}.mp4\n')
                                subprocess.Popen(f'explorer /select,"{save_loc}{name}.{bv}M.ss{time0}.mp4"')
                            else:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c:v hevc_nvenc -preset slow -b:v {bv}M -ss {time0}  -y "{save_loc}{Fname}.{bv}M.ss{time0}.mp4" """)
                                print(f'\ntemp_completed\{Fname}.{bv}M.ss{time0}.mp4\n')
                                subprocess.Popen(f'explorer /select,"{save_loc}{Fname}.{bv}M.ss{time0}.mp4"')
                    elif time1 and time0 == 0:
                        if not Sname:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:v hevc_nvenc -preset slow -b:v {bv}M -t {time1}  -y "{save_loc}{name}.{bv}M.t{time1}.mp4" """)
                            print(f'\ntemp_completed\{name}.{bv}M.t{time1}.mp4\n')
                            subprocess.Popen(f'explorer /select,"{save_loc}{name}.{bv}M.t{time1}.mp4"')
                        else:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c:v hevc_nvenc -preset slow -b:v {bv}M -t {time1}  -y "{save_loc}{Fname}.{bv}M.t{time1}.mp4" """)
                            print(f'\ntemp_completed\{Fname}.{bv}M.t{time1}.mp4\n')
                            subprocess.Popen(f'explorer /select,"{save_loc}{Fname}.{bv}M.t{time1}.mp4"')
                # если не указано время
                else:
                    if not Sname:
                        system(
                            f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c:v hevc_nvenc -preset slow -b:v {bv}M  -y "{save_loc}{name}.{bv}M.mp4" """)
                        print(f'\ntemp_completed\{name}.{bv}M.mp4\n')
                        subprocess.Popen(f'explorer /select,"{save_loc}{name}.{bv}M.mp4"')
                    else:
                        system(
                            f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Fname+'.'+Sname}" -c:v hevc_nvenc -preset slow -b:v {bv}M  -y "{save_loc}{Fname}.{bv}M.mp4" """)
                        print(f'\ntemp_completed\{Fname}.{bv}M.mp4\n')
                        subprocess.Popen(f'explorer /select,"{save_loc}{Fname}.{bv}M.mp4"')
            # обрезка
            if mode == '1':
                if time != None:
                    if time0>0 and time1:
                        if not Sname:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c copy -ss {time0} -t {time1}  -y "{save_loc}{name}.ss{time0}.t{time1}.mp4" """)
                            print(f'\ntemp_completed\{name}.ss{time0}.t{time1}.mp4\n')
                            subprocess.Popen(f'explorer /select,"{save_loc}{name}.ss{time0}.t{time1}.mp4"')
                        else:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c copy -ss {time0} -t {time1}  -y "{save_loc}{Fname}.ss{time0}.t{time1}.mp4" """)
                            print('f\ntemp_completed\{Fname}.ss{time0}.t{time1}.mp4\n')
                            subprocess.Popen(f'explorer /select,"{save_loc}{Fname}.ss{time0}.t{time1}.mp4"')
                    elif time0 and not time1:
                            if not Sname:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c copy -ss {time0}  -y "{save_loc}{name}.ss{time0}.mp4" """)
                                print('f\ntemp_completed\{name}.ss{time0}.mp4\n')
                                subprocess.Popen(f'explorer /select,"{save_loc}{name}.ss{time0}.mp4"')
                            else:
                                system(
                                    f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c copy -ss {time0}  -y "{save_loc}{Fname}.ss{time0}.mp4" """)
                                print('f\ntemp_completed\{Fname}.ss{time0}.mp4\n')
                                subprocess.Popen(f'explorer /select,"{save_loc}{Fname}.ss{time0}.mp4"')
                    elif time1 and time0 == 0:
                        if not Sname:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{name}.mkv" -c copy -t {time1}  -y "{save_loc}{name}.t{time1}.mp4" """)
                            print('f\ntemp_completed\{name}.t{time1}.mp4\n')
                            subprocess.Popen(f'explorer /select,"{save_loc}{name}.t{time1}.mp4"')
                        else:
                            system(
                                f""" ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 3 -i "..\{Sname}" -c copy -t {time1}  -y "{save_loc}{Fname}.t{time1}.mp4" """)
                            print('f\ntemp_completed\{Fname}.t{time1}.mp\n')
                            subprocess.Popen(f'explorer /select,"{save_loc}{Fname}.t{time1}.mp4"')
