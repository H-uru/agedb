import re
import web
import zipfile

class ZipError(web.BadRequest):
    def __init__(self, msg):
        web.BadRequest.__init__(self)
        self.data=msg

def validate_agefile(agefile, seqprefix):
    for l in agefile.readlines():
        l = l.strip()
        bits = l.split('=')
        if len(bits) != 2:
            raise ZipError('The provided age has an error in its .age descriptor')
        if bits[0] == 'SequencePrefix':
            if seqprefix:
                if bits[1] != str(seqprefix):
                    raise ZipError('The provided age has an incorrect sequence prefix')
            else:
                try:
                    intpref = int(bits[1])
                    if not intpref in range(100,200):
                        raise ZipError('The provided age has an incorrect sequence prefix')
                except:
                    raise ZipEror('The provided age has an error in its .age descriptor')

def validate_zip(agefile, agename, seqprefix=None):
    ogg_re = re.compile(r'sfx/\w+\.ogg')
    prp_re = re.compile(r'dat/'+agename+'_\w+\.prp')
    age_re = re.compile(r'dat/'+agename+'\.age')
    misc_re = re.compile(r'dat/[\w ]+\.((csv)|(p2f))')
    py_re = re.compile(r'python/\w+\.py')
    sdl_re = re.compile(r'SDL/'+agename+'\.sdl')
    dir_re = re.compile(r'((sfx)|(dat)|(python)|(SDL))/')

    zfile = zipfile.ZipFile(agefile)
    has_age = False
    has_prp = False
    for i in zfile.infolist():
        f = i.filename
        if prp_re.match(f):
            has_prp = True
            continue
        if age_re.match(f):
            has_age = True
            continue
        if ogg_re.match(f):
            continue
        if misc_re.match(f):
            continue
        if sdl_re.match(f):
            continue
        if py_re.match(f):
            continue
        if dir_re.match(f):
            continue
        raise ZipError(i.filename+' does not appear to be a normal age file, or belongs to a different age')
    if not (has_age and has_prp):
        raise ZipError('The provided archive does not contain required age files (.age and .prp)')
    age = zfile.open('dat/'+agename+'.age')
    validate_agefile(age, seqprefix)

def update_seqprefix(zippath, new_prefix):
    pass
