"""
rubbish_sort.py
"""
import os
import shutil
import sys

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
    for s in name.translate(TRANS):
        if (s >= 'A' and s <= 'Z') or (s >= 'a' and s <= 'z') or (s >= '0' and s <= '9'):
            res = res + s
        else:
            res = res +'_'
    if len(ext) > 0:
        res = res + '.' + ext
    return res

def add_file(files, s_path, s_name, s_ext, d_path, d_name):
    dfname = d_name
    dext = '.' + s_ext if len(s_ext) > 0 else ''
    cnt = 0
    for im in files:
        if im.get('d_path') == d_path and im.get('d_name') == d_name:   # dublicate filename
            cnt += 1
            if len(dext) > 0:
                ix = d_name.rfind(dext)
                dfname = d_name[0:ix] + '(' + str(cnt) + ')' + dext
            else:
                dfname = d_name + '(' + str(cnt) + ')'
    files.append({'s_path': s_path, 's_name': s_name, 's_ext': s_ext, 'd_path': d_path, 'd_name': dfname})
    
def rename_file(src_file, dst_file):
    if src_file != dst_file:
        os.renames(src_file, dst_file) 

def sort(source_path, destination_path):
    directories = []
    images = []     #('JPEG', 'PNG', 'JPG', 'SVG')
    documents = []  #('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    audio = []      #('MP3', 'OGG', 'WAV', 'AMR')
    video = []      #('AVI', 'MP4', 'MOV', 'MKV')
    archives = []   #('ZIP', 'GZ', 'TAR')
    others = []     #
 
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
                EXT = ext.upper()
                if EXT in ('JPEG', 'PNG', 'JPG', 'SVG'):
                    add_file(images, root, fname, ext, destination_path + '\\images', normalize(s_name, ext))
                elif EXT in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
                    add_file(documents, root, fname, ext, destination_path + '\\documents', normalize(s_name, ext))
                elif EXT in ('MP3', 'OGG', 'WAV', 'AMR'):
                    add_file(audio, root, fname, ext, destination_path + '\\audio', normalize(s_name, ext))
                elif EXT in ('AVI', 'MP4', 'MOV', 'MKV'):
                    add_file(video, root, fname, ext, destination_path + '\\video', normalize(s_name, ext))
                elif EXT in ('ZIP', 'GZ', 'TAR', 'RAR'):
                    add_file(archives, root, fname, ext, destination_path + '\\archives\\' + s_name, normalize(s_name, ext))
                else:
                    add_file(others, root, fname, ext, destination_path, normalize(s_name, ext))

    for file in archives:
        shutil.unpack_archive(os.path.join(file.get('s_path'), file.get('s_name')), file.get('d_path'))
        os.remove(os.path.join(file.get('s_path'), file.get('s_name')))
    for file in images:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name'))) 
    for file in documents:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name'))) 
    for file in audio:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name'))) 
    for file in video:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name'))) 
    for file in others:
        rename_file(os.path.join(file.get('s_path'), file.get('s_name')), os.path.join(file.get('d_path'), file.get('d_name'))) 
    
    directories.append({'s_path': '', 's_name': source_path})
    for dir in directories:
        shutil.rmtree(os.path.join(dir.get('s_path'), dir.get('s_name')), ignore_errors=True)

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
