import web

import config
import userdb

cfg = config.agedb

db = web.database(**cfg)

def listAges():
    return list(db.select('ages', what='id,shortname,fullname,creator'))

def listWhere(**args):
    return list(db.where('ages', what='id,shortname,fullname,creator', **args))

def queryAge(aid):
    try:
        intid = int(aid)
        age = dict(db.where('ages', id=aid)[0])
    except:
        age = dict(db.where('ages', shortname=aid)[0])
    age['author'] = userdb.queryUser(age['creator'])
    age['author']['uri'] = config.users_path+'/'+str(age['creator'])
    # Once the author dict is filled, creator is redundant, and not part of
    # the public API
    del age['creator']
    return age

def ageName(ageid):
    return db.where('ages', what='shortname', id=ageid)[0].shortname

def ageFromName(agename):
    return db.where('ages', what='id', shortname=agename)[0].id

def ageLongName(ageid):
    return db.where('ages', what='fullname', id=ageid)[0].fullname

def createAge(shortname, fullname, creator, description):
    return db.insert('ages', creator=creator, shortname=shortname, fullname=fullname, description=description)

def listFiles(**kwargs):
    where = []
    for k, v in kwargs.iteritems():
        where.append(k + ' = ' + web.sqlquote(v))
    if not 'status' in kwargs:
        where.append("status IN ('NEW', 'VERIFIED')")
    files = list(db.select('files', where=web.SQLQuery.join(where, ' AND ')))
    for f in files:
        ageid = f['age']
        f['age'] = {}
        f['age']['fullname'] = ageLongName(ageid)
        f['age']['id'] = ageid
        f['age']['uri'] = config.ages_path+'/'+str(ageid)
        f['uri'] = config.files_path+'/'+str(f['id'])
        f['fetch_uri'] = f['uri']+'/download'
    return files

def listLatestFiles(**kwargs):
    where = []
    for k, v in kwargs.iteritems():
        where.append(k + ' = ' + web.sqlquote(v))
    if not 'status' in kwargs:
        where.append("status IN ('NEW', 'VERIFIED')")
    files = list(db.select('files', what='timestamp, gamever, age, MAX(id) as id, status, version', where=web.SQLQuery.join(where, ' AND '), group='age, gamever'))
    for f in files:
        ageid = f['age']
        f['age'] = {}
        f['age']['fullname'] = ageLongName(ageid)
        f['age']['id'] = ageid
        f['age']['uri'] = config.ages_path+'/'+str(ageid)
        f['uri'] = config.files_path+'/'+str(f['id'])
        f['fetch_uri'] = f['uri']+'/download'
    return files

def latestFile(**kwargs):
    where = []
    for k, v in kwargs.iteritems():
        where.append(k + ' = ' + web.sqlquote(v))
    if not 'status' in kwargs:
        where.append("status IN ('NEW', 'VERIFIED')")
    f = dict(db.select('files', what='timestamp, gamever, age, MAX(id) as id, status, version', where=web.SQLQuery.join(where, ' AND '), group='age, gamever')[0])
    ageid = f['age']
    f['age'] = {}
    f['age']['fullname'] = ageLongName(ageid)
    f['age']['id'] = ageid
    f['age']['uri'] = config.ages_path+'/'+str(ageid)
    f['uri'] = config.files_path+'/'+str(f['id'])
    f['fetch_uri'] = f['uri']+'/download'
    return f

def queryFile(fid):
    info = dict(db.where('files', id=fid)[0])
    ageid = info['age']
    info['age'] = {'uri':config.ages_path+'/'+str(ageid)}
    info['age']['id'] = ageid
    info['age']['fullname'] = ageLongName(ageid)
    info['fetch_uri'] = config.files_path+'/'+str(info['id'])+'/download'
    return info

def createFile(age, gamever, version, status):
    return db.insert('files', age=age, gamever=gamever, version=version, status=status)

def ageFromFile(fileid):
    return db.where('files', what='age', id=fileid)[0].age
