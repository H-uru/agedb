import web
import mimerender

import common
import config

import agedb
import userdb

urls = (
    r'/?', 'userlist',
    r'/(\d+)/?', 'userinfo'
)

app = web.application(urls, locals())

def render_user_list(*users):
    return common.template.userlist(users)

def render_user_page(**user):
    return common.template.userpage(user)
        
class userinfo():
    @mimerender.mimerender(
        default='html',
        override_input_key=common.input_key,
        html=render_user_page,
        txt=render_user_page,
        json=common.render_json
    )
    @common.enable_cors()
    def GET(self, uid):
        try:
            return userdb.queryUser(uid)
        except IndexError:
            raise web.NotFound("The requested user does not exist")
    
    @common.enable_cors()
    def POST(self, uid):
        raise web.NoMethod

class userlist():
    @mimerender.mimerender(
        default='html',
        override_input_key=common.input_key,
        html=render_user_list,
        txt=render_user_list,
        json=common.render_json_list,
        islist=True
    )
    @common.enable_cors()
    def GET(self):
        users = userdb.listUsers()
        for u in users:
            u['uri'] = config.users_path+'/'+str(u.id)
        return users

