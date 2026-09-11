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
    logger.debug(sys.argv)
    if len(sys.argv) > 1:
        logger.debug(f"file: {sys.argv[1]}")
        return True
    else:
        logger.debug("not context menu")
        return False


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_config_path():
    return path.join(get_base_dir(), "config.json")


def is_folder_selected(_file_path):
    if path.isfile(_file_path):
        logger.debug(f"file: {_file_path}")
        return "file"
    elif path.isdir(_file_path):
        logger.debug(f"dir: {_file_path}")
        return "dir"


def conf_init():
    conf_path = get_config_path()
    if not path.exists(conf_path):
        logger.debug("config.json not found, creating new one")
        _save_loc_ = input(
            "Where do you want to save the files?/Output folder\nYou don't need to create it, just enter name in format ("
            "C:\\Users\\User\\Desktop\\Output): ")
        if not _save_loc_.endswith("\\"):
            _save_loc_ += "\\"
        with open(conf_path, "w", encoding="utf-8") as f:
            json.dump({"saves_location": _save_loc_}, f)

    try:
        with open(conf_path, "r", encoding="utf-8") as f:
            logger.debug("config.json found, loading")
            config = json.load(f)
            _save_loc = config["saves_location"]
            if not path.exists(_save_loc):
                logger.debug("Output folder not found, creating new one")
                mkdir(_save_loc)
            return _save_loc
    except FileNotFoundError:
        logger.error("Invalid Destination")
        if path.exists(conf_path):
            os.remove(conf_path)
        logger.warning("Restart Transcoder and Enter a valid destination")


def parse_time(val):
    if not val:
        return None
    val = val.strip()
    if not val:
        return None
    parts = val.split(':')
    try:
        if len(parts) == 1:
            return float(parts[0])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        else:
            return None
    except ValueError:
        return None


def format_time_val(val):
    if val is None:
        return ''
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)


def build_time_params(start_val, end_val):
    """
    Формирует аргументы обрезки ffmpeg и суффикс для имени файла.
    - Если указано начало и конец: от start_val до end_val
    - Если начало не указано, но указан конец: от 0 до end_val
    - Если указано начало, а конец не указан: от start_val до конца
    - Если не указано ни то, ни другое: не обрезать
    """
    if start_val is not None and end_val is not None:
        s_str = format_time_val(start_val)
        e_str = format_time_val(end_val)
        return f"-ss {s_str} -to {e_str}", f".ss{s_str}.to{e_str}"
    elif start_val is not None and end_val is None:
        s_str = format_time_val(start_val)
        return f"-ss {s_str}", f".ss{s_str}"
    elif start_val is None and end_val is not None:
        e_str = format_time_val(end_val)
        return f"-ss 0 -to {e_str}", f".ss0.to{e_str}"
    else:
        return "", ""


def main_thread(_file_path, context_mode):
    while True:
        save_loc = conf_init()
        if not save_loc:
            break
        # выбор режима: GPU transcode (0), CPU transcode c GPU декодером (1) или copy (2)
        print('Select mode:')
        print('  [0] Transcode on GPU (NVIDIA NVENC) [default]')
        print('  [1] Transcode on CPU with GPU decoding (CUDA -> libx264)')
        print('  [2] Copy video without transcode (stream copy / cut)')
        mode = input('mode [0/1/2]: ').strip()
        if mode == '' or mode == '0':
            mode = '0'
            logger.info('transcode mode: GPU (NVENC)')
            print('GPU transcode (NVENC)')
        elif mode == '1':
            logger.info('transcode mode: CPU with GPU decode')
            print('CPU transcode with GPU decode (CUDA -> libx264)')
        elif mode == '2':
            logger.info('copy / cut mode')
            print('copy mode')
        else:
            logger.warning(f"Unknown mode '{mode}', defaulting to GPU transcode")
            mode = '0'

        bv = 2
        if mode in ('0', '1'):
            bv_input = input('bitrate in M [default 2M]: ').strip()
            if bv_input == '':
                logger.debug('bitrate 2M')
                bv = 2
                print('2M')
            else:
                try:
                    bv = float(bv_input)
                    if bv.is_integer():
                        bv = int(bv)
                    print(f'{bv}M')
                except ValueError:
                    bv = 2
                    print('Invalid bitrate, default 2M')

        # выбор файла или всей папки
        while True:
            logger.debug("file or folder selection")
            file_names = []
            if context_mode:
                file_names.append(_file_path)
            else:
                print('You want to transcode a file or a whole folder?')
                folder = input('file[1] or folder[]: ').strip()
                if folder == '':
                    logger.debug("folder mode")
                    folder = '0'
                    print('folder')
                else:
                    logger.debug("file mode")
                    print('file')
                    print(
                        'Enter the name of the file you want to transcode (without extension if .mkv) or press Enter to return')

                if folder == '1':
                    logger.debug("file selection")
                    print('Name and modified time')
                    for i in os.listdir("..\\"):
                        if len(i.split('.')) > 1:
                            if i.split('.')[-1].lower() in ('mkv', 'mp4'):
                                print(f'{i}     {mtime(i, "..\\\\")}')
                    name = input('-i ').strip()
                    if name == '':
                        break
                    if not path.isabs(name):
                        if not path.exists(f"..\\{name}") and path.exists(f"..\\{name}.mkv"):
                            name = f"..\\{name}.mkv"
                        else:
                            name = f"..\\{name}"
                    file_names.append(name)
                elif folder == '0':
                    logger.debug("folder selected")
                    files = os.listdir("..\\")
                    print("files to transcode:")
                    print('Name and modified time')
                    for i in files:
                        if len(i.split('.')) > 1:
                            if i.split('.')[-1].lower() in ('mkv', 'mp4'):
                                file_names.append(f"..\\{i}")
                                print(f'{i}     {mtime(i, "..\\\\")}')

            # выбор времени обрезки
            logger.debug("time selection")
            print("Time trim settings (hh:mm:ss, mm:ss or seconds):")
            t0_input = input('Start time [empty = from start]: ').strip()
            t1_input = input('End time [empty = to end]: ').strip()
            time0 = parse_time(t0_input)
            time1 = parse_time(t1_input)

            time_args, time_suffix = build_time_params(time0, time1)

            # транскодирование каждого выбранного файла
            for file_entry in file_names:
                logger.info(f"transcoding file {file_entry}...")
                print(f"\n\ntranscoding file {file_entry}...\n\n")

                base_name = path.basename(file_entry)
                fname, ext = path.splitext(base_name)

                # Формирование команды ffmpeg в зависимости от выбранного режима
                if mode == '0':
                    # GPU транскодирование (NVENC)
                    start_command = 'ffmpeg -hide_banner -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 2'
                    add_command = f'-c:a copy -c:v hevc_nvenc -map 0 -preset p7 -strict -2 -b:v {bv}M'
                    out_name = f"{fname}.{bv}M{time_suffix}.mp4"
                elif mode == '1':
                    # CPU транскодирование с декодированием на GPU
                    start_command = 'ffmpeg -hide_banner -hwaccel cuda'
                    add_command = f'-c:a copy -c:v libx264 -map 0 -preset medium -b:v {bv}M'
                    out_name = f"{fname}.cpu.{bv}M{time_suffix}.mp4"
                else:
                    # Режим копирования потоков / обрезка без перекодирования
                    start_command = 'ffmpeg -hide_banner'
                    add_command = '-map 0 -c copy'
                    out_name = f"{fname}{time_suffix}.mp4"

                out_full_path = path.join(save_loc, out_name)

                cmd = f'{start_command} {time_args} -i "{file_entry}" {add_command} -y "{out_full_path}"'
                logger.debug(f"Running command: {cmd}")
                system(cmd)
                print(f'\n{out_full_path}\n')

            logger.info("transcoding completed")
            print("Do you want to delete original files? (y/N)")
            del_ans = input().strip()
            if del_ans.lower() == 'y':
                for file_entry in file_names:
                    logger.debug(f"Deleting original: {file_entry}")
                    try:
                        if path.exists(file_entry):
                            os.remove(file_entry)
                    except Exception as e:
                        logger.error(f"Error removing {file_entry}: {e}")
                logger.warning('Original files deleted')
                if context_mode:
                    sys.exit(0)
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
