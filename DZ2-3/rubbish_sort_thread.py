"""
rubbish_sort.py
"""
import os
import shutil
import sys
import logging
from threading import Thread

CIMAGES = ('JPEG', 'PNG', 'JPG', 'SVG', 'BMP')
CDOCUMENTS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPT', 'PPTX')
CAUDIO = ('MP3', 'OGG', 'WAV', 'AMR', 'FLAC')
CVIDEO = ('AVI', 'MP4', 'MOV', 'MKV', 'TS', 'SRT', 'DTS', 'MPG')
CARCHIVES = ('ZIP', 'GZ', 'TAR', 'RAR')

CYRILLIC_SYMBOLS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЄІЇҐабвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("A", "B", "V", "G", "D", "E", "E", "Zh", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U",
               "F", "H", "Ts", "Ch", "Sh", "Sch", "", "Y", "", "E", "Yu", "Ya", "Ye", "I", "Ji", "G",
               "a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "ye", "i", "ji", "g")
TRANSLATION_UKR = ("A", "B", "V", "H", "D", "E", "E", "Zh", "Z", "Y", "Y", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U",
                   "F", "Kh", "Ts", "Ch", "Sh", "Shch", "", "Y", "", "E", "Yu", "Ya", "Ye", "I", "Yi", "G",
                   "a", "b", "v", "h", "d", "e", "e", "zh", "z", "y", "i", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "iu", "ia", "ie", "i", "i", "g")
TRANS = {}
TRANSU = {}
    
def transliteration(text, is_ukr = False):
    global TRANS
    global TRANSU
    if is_ukr:
        if len(TRANSU) == 0:
            for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION_UKR):
                TRANSU[ord(c)] = l
        return(text.translate(TRANSU))
    else:
        if len(TRANS) == 0:
            for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
                TRANS[ord(c)] = l
        return(text.translate(TRANS))


def normalize(name, ext = ''):
    res = ''
    if len(name) > 0:
        for s in transliteration(name):
            if (s >= 'A' and s <= 'Z') or (s >= 'a' and s <= 'z') or (s >= '0' and s <= '9'):
                res = res + s
            else:
                res = res +'_'
        if len(ext) > 0:
            res = res + '.' + ext
    return res

def rename_file(src_file, dst_file):
    if src_file != dst_file:
        os.renames(src_file, dst_file) 

def work_rename_files(files, is_arc=False):
    for file in files:
        if is_arc:
            shutil.unpack_archive(os.path.join(file.get('s_path'), file.get('s_name')), file.get('d_path'))
            os.remove(os.path.join(file.get('s_path'), file.get('s_name')))
        else:
            rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name'))) 


def sort(source_path, destination_path = ''):
    directories = []
    images = []     #('JPEG', 'PNG', 'JPG', 'SVG')
    documents = []  #('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    audio = []      #('MP3', 'OGG', 'WAV', 'AMR')
    video = []      #('AVI', 'MP4', 'MOV', 'MKV', 'TS')
    archives = []   #('ZIP', 'GZ', 'TAR')
    others = []     #
 
    def normalize_path(pname):
        if pname[0] == '"':
            pname = pname[1:]
        while pname[-1] in ('\\', '"'):
            pname = pname[0:len(pname)-1]
        return pname
    
    def add_file(files, s_path, s_name, s_ext, d_path, d_name):
        dfname = d_name
        dext = '.' + s_ext if len(s_ext) > 0 else ''
        cnt = 0
        for im in files:
            if im.get('d_path') == d_path and im.get('d_name') == dfname:   # dublicate filename
                cnt += 1
                if len(dext) > 0:
                    ix = d_name.rfind(dext)
                    dfname = d_name[0:ix] + '(' + str(cnt) + ')' + dext
                else:
                    dfname = d_name + '(' + str(cnt) + ')'
        files.append({'s_path': s_path, 's_name': s_name, 's_ext': s_ext, 'd_path': d_path, 'd_name': dfname})
        
    if len(destination_path) == 0:
        destination_path = source_path
    source_path = normalize_path(source_path)
    destination_path = normalize_path(destination_path)
    destination_orig = destination_path
    if destination_path == source_path:
        destination_path = destination_orig + '(dst)'
    
    for root, dirs, files in os.walk( source_path):
        for dname in dirs:
            directories.append({'s_path': root, 's_name': dname})
        for fname in files:
            ix = fname.rfind('.')
            if ix < 0:
                add_file(others, root, fname, '', destination_path, normalize(fname))
            else:
                s_name = fname[0:ix:]
                ext = fname[ix+1:]
                if not s_name:
                    s_name = fname
                    ext = ''
                EXT = ext.upper()
                if EXT in CIMAGES:
                    add_file(images, root, fname, ext, destination_path + '\\images', normalize(s_name, ext))
                elif EXT in CDOCUMENTS:
                    add_file(documents, root, fname, ext, destination_path + '\\documents', normalize(s_name, ext))
                elif EXT in CAUDIO:
                    add_file(audio, root, fname, ext, destination_path + '\\audio', normalize(s_name, ext))
                elif EXT in CVIDEO:
                    add_file(video, root, fname, ext, destination_path + '\\video', normalize(s_name, ext))
                elif EXT in CARCHIVES:
                    add_file(archives, root, fname, ext, destination_path + '\\archives\\' + normalize(s_name), normalize(s_name, ext))
                else:
                    add_file(others, root, fname, ext, destination_path, normalize(s_name, ext))

    threads = []
    tf = Thread(target=work_rename_files, args=(archives, True))
    tf.start()
    threads.append(tf)
    tf = Thread(target=work_rename_files, args=(images, False))
    tf.start()
    threads.append(tf)
    tf = Thread(target=work_rename_files, args=(documents, False))
    tf.start()
    threads.append(tf)
    tf = Thread(target=work_rename_files, args=(audio, False))
    tf.start()
    threads.append(tf)
    tf = Thread(target=work_rename_files, args=(video, False))
    tf.start()
    threads.append(tf)
    tf = Thread(target=work_rename_files, args=(others, False))
    tf.start()
    threads.append(tf)

    [el.join() for el in threads]

    directories.append({'s_path': '', 's_name': source_path})
    for dir in directories:
        shutil.rmtree(os.path.join(dir.get('s_path'), dir.get('s_name')), ignore_errors=True)

    if destination_orig == source_path:
        try:
            os.rename(destination_path, source_path)
        except Exception as e:
            logging.debug(str(e))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(threadName)s %(message)s',
        handlers=[
            logging.FileHandler("rubbish_sort_thread.log"),
            logging.StreamHandler()
        ]
    )
    if len(sys.argv) >= 3:
        source_path = sys.argv[1]
        destination_path = sys.argv[2]
    elif len(sys.argv) == 2:
        source_path = sys.argv[1]
        destination_path = source_path
    else:
        source_path = '.\\test'
        destination_path = source_path

    logging.debug('Start')
    sort(source_path, destination_path)
    logging.debug('Finish')
else:
    transliteration('')
    transliteration('', True)
