import web
import threading

import agedb
import config

cfg = config.userdb

ctx = threading.local()

db = web.database(**cfg)

def do_auth(admin, maintainer, username, password):
    print "Doing dummy authentication"
    # TODO: implement this
    ctx.uid = 1
    ctx.admin = 1
    ctx.maintainer = 1
    return True


def user_auth(method, admin=False, maintainer=False):
    def wrap(*args, **kwds):
        username = web.input().get('_auth_user', None)
        password = web.input().get('_auth_pass', None)
        if(do_auth(admin, maintainer, username, password)):
            return method(*args, **kwds)
        else:
            raise web.Forbidden()
    return wrap

def admin_auth(method):
    return user_auth(method, admin=True)

def maintainer_auth(method):
    return user_auth(method, maintainer=True)

def listUsers():
    users = list(db.select(config.usertable, what='user_id,username'))
    print 'listUsers'
    for u in users:
        u['id'] = u['user_id']
        del u['user_id']
    return users

def insertUser(username, password):
    return db.insert(config.usertable, username=username, password=password)

def queryUser(uid):
    result = db.where(config.usertable, what='user_id,username', user_id=uid)[0]
    result['id'] = result['user_id']
    del result['user_id']
    ages = agedb.listWhere(creator=uid)
    for a in ages:
        a['uri'] = config.ages_path+'/'+str(a.id)
    result['ages'] = ages
    return dict(result)
