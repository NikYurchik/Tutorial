import os
import shutil
import sys
import re
"""
rubbish_sort_recursive.py
"""
CIMAGES = ('JPEG', 'PNG', 'JPG', 'SVG', 'BMP')
CDOCUMENTS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPT', 'PPTX')
CAUDIO = ('MP3', 'OGG', 'WAV', 'AMR', 'FLAC')
CVIDEO = ('AVI', 'MP4', 'MOV', 'MKV', 'TS', 'SRT', 'DTS', 'MPG')
CARCHIVES = ('ZIP', 'GZ', 'TAR', 'RAR')

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "ye", "i", "ji", "g")

TRANS = {}
    
def normalize(name, ext = ''):
    global TRANS
    if len(TRANS) == 0:
        for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            TRANS[ord(c)] = l
            TRANS[ord(c.upper())] = l.upper()
    res = ''
    if len(name) > 0:
        for s in name.translate(TRANS):
            if (s >= 'A' and s <= 'Z') or (s >= 'a' and s <= 'z') or (s >= '0' and s <= '9'):
                res = res + s
            else:
                res = res +'_'
        if len(ext) > 0:
            res = res + '.' + ext
    return res

def rename_file(src_file, dst_file, ext):
    dext = '.' + ext if len(ext) > 0 else ''
    cnt = 0
    if src_file != dst_file:
        try:
            os.renames(src_file, dst_file) 
        except FileExistsError:
            cnt += 1
            if len(dext) > 0:
                ix = dst_file.rfind(dext)
                dfname = dst_file[0:ix]
            else:
                dfname = dst_file
            s = re.search("\(\d+\)\Z", dfname, re.IGNORECASE)
            if s:
                t = s.group(0)
                s = re.search("\d+", t, re.IGNORECASE)
                m = int(s.group(0))
                if m >= cnt:
                    cnt = m + 1
                res = re.sub("\(\d+\)\Z", "("+str(cnt)+")", dfname, re.IGNORECASE)
            else:
                res = dfname + "("+str(cnt)+")"

            if len(dext) > 0:
                dfname = dfname + dext
            rename_file(src_file, dfname, ext)
                

def prepare_dir(source_path, destination_path):
    directories = []
    images = []     #('JPEG', 'PNG', 'JPG', 'SVG')
    documents = []  #('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    audio = []      #('MP3', 'OGG', 'WAV', 'AMR')
    video = []      #('AVI', 'MP4', 'MOV', 'MKV')
    archives = []   #('ZIP', 'GZ', 'TAR')
    others = []     #

    def add_file(files, s_path, s_name, s_ext, d_path, d_name):
        files.append({'s_path': s_path, 's_name': s_name, 's_ext': s_ext, 'd_path': d_path, 'd_name': d_name})
        
    with os.scandir(source_path) as it:
        for entry in it:
            ix = entry.name.rfind('.')
            if entry.is_dir():
                directories.append({'s_path': source_path, 's_name': entry.name})
            elif ix < 0:
                add_file(others, source_path, entry.name, '', destination_path, normalize(entry.name))
            else:
                s_name = entry.name[0:ix:]
                ext = entry.name[ix+1:]
                EXT = ext.upper()
                if EXT in CIMAGES:
                    add_file(images, source_path, entry.name, ext, destination_path + '\\images', normalize(s_name, ext))
                elif EXT in CDOCUMENTS:
                    add_file(documents, source_path, entry.name, ext, destination_path + '\\documents', normalize(s_name, ext))
                elif EXT in CAUDIO:
                    add_file(audio, source_path, entry.name, ext, destination_path + '\\audio', normalize(s_name, ext))
                elif EXT in CVIDEO:
                    add_file(video, source_path, entry.name, ext, destination_path + '\\video', normalize(s_name, ext))
                elif EXT in CARCHIVES:
                    add_file(archives, source_path, entry.name, ext, destination_path + '\\archives\\' + s_name, normalize(s_name, ext))
                else:
                    add_file(others, source_path, entry.name, ext, destination_path, normalize(s_name, ext))

    for dir in directories:
        prepare_dir(os.path.join(dir.get('s_path'), dir.get('s_name')), destination_path)

    for file in archives:
        shutil.unpack_archive(os.path.join(file.get('s_path'), file.get('s_name')), file.get('d_path'))
        os.remove(os.path.join(file.get('s_path'), file.get('s_name')))
    for file in images:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name')), file.get('s_ext')) 
    for file in documents:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name')), file.get('s_ext')) 
    for file in audio:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name')), file.get('s_ext')) 
    for file in video:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name')), file.get('s_ext')) 
    for file in others:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name')), file.get('s_ext')) 
    try:
        os.rmdir(source_path)
    except FileNotFoundError:
        None

def sort(source_path, destination_path):
    if len(destination_path) == 0:
        destination_path = source_path
    destination_orig = destination_path
    if destination_path == source_path:
        destination_path = destination_orig + '(dst)'

    prepare_dir(source_path, destination_path)
    if destination_orig == source_path:
        os.rename(destination_path, source_path)


if __name__ == "__main__":             
    if len(sys.argv) >= 3:
        source_path = sys.argv[1]
        destination_path = sys.argv[2]
    elif len(sys.argv) == 2:
        source_path = sys.argv[1]
        destination_path = source_path
    else:
        source_path = '.\\test'
        destination_path = source_path
    sort(source_path, destination_path)
else:
    normalize('')


