import subprocess
from os import system
from os import path
from os import mkdir

if not path.exists("..\\temp_completed"):
    mkdir("..\\temp_completed")

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
        elif len(name)==1: name = name[0]
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
                            f""" ffmpeg -hide_banner -i "..\{name}.mkv" -c:v hevc_nvenc -b:v {bv}M -ss {time0} -t {time1} -y "..\\temp_completed\{name}.{bv}M.ss{time0}.t{time1}.mp4" """)
                        print(f'\ntemp_completed\{name}.{bv}M.ss{time0}.t{time1}.mp4\n')
                        subprocess.Popen(f'explorer /select,"..\\temp_completed\{name}.{bv}M.ss{time0}.t{time1}.mp4"')
                    else:
                        system(
                            f""" ffmpeg -hide_banner -i "..\{Sname}" -c:v hevc_nvenc -b:v {bv}M -ss {time0} -t {time1} -y "..\\temp_completed\{Fname}.{bv}M.ss{time0}.t{time1}.mp4" """)
                        print(f'\ntemp_completed\{Fname}.{bv}M.ss{time0}.t{time1}.mp4\n')
                        subprocess.Popen(f'explorer /select,"..\\temp_completed\{Fname}.{bv}M.ss{time0}.t{time1}.mp4"')
                elif time0 and not time1:
                        if not Sname:
                            system(
                                f""" ffmpeg -hide_banner -i "..\{name}.mkv" -c:v hevc_nvenc -b:v {bv}M -ss {time0} -y "..\\temp_completed\{name}.{bv}M.ss{time0}.mp4" """)
                            print(f'\ntemp_completed\{name}.{bv}M.ss{time0}.mp4\n')
                            subprocess.Popen(f'explorer /select,"..\\temp_completed\{name}.{bv}M.ss{time0}.mp4"')
                        else:
                            system(
                                f""" ffmpeg -hide_banner -i "..\{Sname}" -c:v hevc_nvenc -b:v {bv}M -ss {time0} -y "..\\temp_completed\{Fname}.{bv}M.ss{time0}.mp4" """)
                            print(f'\ntemp_completed\{Fname}.{bv}M.ss{time0}.mp4\n')
                            subprocess.Popen(f'explorer /select,"..\\temp_completed\{Fname}.{bv}M.ss{time0}.mp4"')
                elif time1 and time0 == 0:
                    if not Sname:
                        system(
                            f""" ffmpeg -hide_banner -i "..\{name}.mkv" -c:v hevc_nvenc -b:v {bv}M -t {time1} -y "..\\temp_completed\{name}.{bv}M.t{time1}.mp4" """)
                        print(f'\ntemp_completed\{name}.{bv}M.t{time1}.mp4\n')
                        subprocess.Popen(f'explorer /select,"..\\temp_completed\{name}.{bv}M.t{time1}.mp4"')
                    else:
                        system(
                            f""" ffmpeg -hide_banner -i "..\{Sname}" -c:v hevc_nvenc -b:v {bv}M -t {time1} -y "..\\temp_completed\{fname}.{bv}M.t{time1}.mp4" """)
                        print(f'\ntemp_completed\{fname}.{bv}M.t{time1}.mp4\n')
                        subprocess.Popen(f'explorer /select,"..\\temp_completed\{fname}.{bv}M.t{time1}.mp4"')
            # если не указано время
            else:
                if not Sname:
                    system(
                        f""" ffmpeg -hide_banner -i "..\{name}.mkv" -c:v hevc_nvenc -b:v {bv}M -y "..\\temp_completed\{name}.{bv}M.mp4" """)
                    print(f'\ntemp_completed\{name}.{bv}M.mp4\n')
                    subprocess.Popen(f'explorer /select,"..\\temp_completed\{name}.{bv}M.mp4"')
                else:
                    system(
                        f""" ffmpeg -hide_banner -i "..\{Sname}" -c:v hevc_nvenc -b:v {bv}M -y "..\\temp_completed\{fname}.{bv}M.mp4" """)
                    print(f'\ntemp_completed\{fname}.{bv}M.mp4\n')
                    subprocess.Popen(f'explorer /select,"..\\temp_completed\{fname}.{bv}M.mp4"')
        # обрезка
        if mode == '1':
            if time != None:
                if time0>0 and time1:
                    if not Sname:
                        system(
                            f""" ffmpeg -hide_banner -i "..\{name}.mkv" -c copy -ss {time0} -t {time1} -y "..\\temp_completed\{name}.ss{time0}.t{time1}.mp4" """)
                        print(f'\ntemp_completed\{name}.ss{time0}.t{time1}.mp4\n')
                        subprocess.Popen(f'explorer /select,"..\\temp_completed\{name}.ss{time0}.t{time1}.mp4"')
                    else:
                        system(
                            f""" ffmpeg -hide_banner -i "..\{Sname}" -c copy -ss {time0} -t {time1} -y "..\\temp_completed\{Fname}.ss{time0}.t{time1}.mp4" """)
                        print('f\ntemp_completed\{Fname}.ss{time0}.t{time1}.mp4\n')
                        subprocess.Popen(f'explorer /select,"..\\temp_completed\{Fname}.ss{time0}.t{time1}.mp4"')
                elif time0 and not time1:
                        if not Sname:
                            system(
                                f""" ffmpeg -hide_banner -i "..\{name}.mkv" -c copy -ss {time0}-y "..\\temp_completed\{name}.ss{time0}.mp4" """)
                            print('f\ntemp_completed\{name}.ss{time0}.mp4\n')
                            subprocess.Popen(f'explorer /select,"..\\temp_completed\{name}.ss{time0}.mp4"')
                        else:
                            system(
                                f""" ffmpeg -hide_banner -i "..\{Sname}" -c copy -ss {time0} -y "..\\temp_completed\{Fname}.ss{time0}.mp4" """)
                            print('f\ntemp_completed\{Fname}.ss{time0}.mp4\n')
                            subprocess.Popen(f'explorer /select,"..\\temp_completed\{Fname}.ss{time0}.mp4"')
                elif time1 and time0 == 0:
                    if not Sname:
                        system(
                            f""" ffmpeg -hide_banner -i "..\{name}.mkv" -c copy -t {time1} -y "..\\temp_completed\{name}.t{time1}.mp4" """)
                        print('f\ntemp_completed\{name}.t{time1}.mp4\n')
                        subprocess.Popen(f'explorer /select,"..\\temp_completed\{name}.t{time1}.mp4"')
                    else:
                        system(
                            f""" ffmpeg -hide_banner -i "..\{Sname}" -c copy -t {time1} -y "..\\temp_completed\{fname}.t{time1}.mp4" """)
                        print('f\ntemp_completed\{fname}.t{time1}.mp\n')
                        subprocess.Popen(f'explorer /select,"..\\temp_completed\{fname}.t{time1}.mp4"')
