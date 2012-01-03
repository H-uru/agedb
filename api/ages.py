import web
import mimerender
import re

import common
import config

import userdb
import agedb

import plasma_utils

urls = (
    r'/?', 'agelist',
    r'/(\w+)/?', 'ageinfo',
    r'/(\w+)/files/?', 'agefiles',
    r'/(\w+)/files/(latest|verified)/?', 'agefiles_tagged',
    r'/(\w+)/files/(\d+\.\d+)/?', 'agefiles_version',
    r'/(\w+)/files/(\d+\.\d+)/(latest|verified)/?', 'agefile_specific'
)

app = web.application(urls, locals())

age_name_re = re.compile('\w+')
age_fullname_re = re.compile('[\w ]+')

def render_age_list(*ages):
    return common.template.agelist(ages)

def render_age_page(**age):
    return common.template.agepage(age)

def render_file_list(*files):
    return common.template.filelist(files)

class ageinfo:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=render_age_page,
        txt=render_age_page,
        json=common.render_json,
    )
    @common.enable_cors('DELETE, PUT')
    def GET(self, ageid):
        return agedb.queryAge(ageid)

    @userdb.user_auth
    @common.enable_cors('DELETE, PUT')
    def DELETE(self, ageid):
        agedb.removeAge(ageid)

    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=render_age_page,
        txt=render_age_page,
        json=common.render_json,
    )
    @userdb.admin_auth
    @common.enable_cors('DELETE, PUT')
    def PUT(self, ageid):
        agedb.insertAge(ageid)
        return agedb.queryAge(ageid)
        
    @common.enable_cors('DELETE, PUT')
    def OPTIONS(self):
        pass

class agelist:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=render_age_list,
        txt=render_age_list,
        json=common.render_json_list,
        islist=True
    )
    @common.enable_cors()
    def GET(self):
        ages = agedb.listAges();
        for a in ages:
            a['uri'] = config.ages_path+'/'+str(a['id'])
        return ages

    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=render_age_page,
        txt=render_age_page,
        json=common.render_json,
    )
    @userdb.user_auth
    @common.enable_cors()
    def POST(self):
        x = web.input(agedata={})
        agebits = {}
        try:
            description = x['description']
            shortname = x['shortname']
            fullname = x['fullname']
            agefile = x['agedata'].file
            gamever = x['gameversion']
            agever = x['version']
        except KeyError:
            raise common.MissingParam()

        # Confirm that the zip file looks like a real age     
        plasma_utils.validate_zip(agefile, shortname)

        if not age_name_re.match(shortname):
            raise common.BadParam('shortname')
        if not age_fullname_re.match(fullname):
            raise common.BadParam('fullname')
        if not gamever in config.acceptable_game_versions:
            raise common.BadParam('gameversion')
        new_id = agedb.createAge(shortname=shortname, fullname=fullname, description=description, creator=userdb.ctx.uid)
        # Now that we have an age, we need to stash the file
        fileid = agedb.createFile(age=new_id, gamever=gamever, version=agever, status='NEW')
        filename = config.agefiles_path+str(fileid)+'.zip'
        out = open(filename, 'wb')
        agefile.seek(0)
        out.write(agefile.read())
        out.close()
        plasma_utils.update_seqprefix(filename, new_id)
        raise web.redirect(config.ages_path+'/'+str(new_id));
        
    @common.enable_cors()
    def OPTIONS(self):
        pass

class agefiles:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=render_file_list,
        txt=render_file_list,
        json=common.render_json,
        islist=True
    )
    @common.enable_cors()
    def GET(self, ageid):
        return agedb.listFiles(age=ageid)
    
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=render_age_page,
        txt=render_age_page,
        json=common.render_json,
    )
    @userdb.user_auth
    @common.enable_cors()
    def POST(self, ageid):
        creator = agedb.ageCreator(ageid)
        if userdb.ctx.uid != creator:
            raise web.Forbidden()
        x = web.input(agedata={})
        agebits = {}
        try:
            agefile = x['agedata'].file
            gamever = x['gameversion']
            agever = x['version']
        except KeyError:
            raise common.MissingParam()
        # Confirm that the zip file looks like a real age     
        plasma_utils.validate_zip(agefile, shortname, ageid)
        if not gamever in config.acceptable_game_versions:
            raise common.BadParam('gameversion')
        fileid = agedb.createFile(age=new_id, gamever=gamever, version=agever, status='NEW')
        filename = config.agefiles_path+str(fileid)+'.zip'
        out = open(filename, 'wb')
        agefile.seek(0)
        out.write(agefile.read())
        out.close()
        raise web.redirect(config.ages_path+'/'+str(ageid));

class agefiles_version:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=common.render_file_list,
        txt=common.render_file_list,
        json=common.render_json_list,
        islist = True
    )
    @common.enable_cors()
    def GET(self, ageid, version):
        if not version in config.acceptable_game_versions:
            raise web.notfound()
        try:
            intid = int(ageid)
            intid = ageid
        except:
            intid = agedb.ageFromName(ageid)
        return agedb.listFiles(gamever=version, age=intid)

class agefiles_tagged:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=common.render_file_list,
        txt=common.render_file_list,
        json=common.render_json_list,
        islist = True
    )
    @common.enable_cors()
    def GET(self, ageid, tag):
        try:
            intid = int(ageid)
            intid = ageid
        except:
            intid = agedb.ageFromName(ageid)
        if tag == 'verified':
            return agedb.listLatestFiles(status='VERIFIED', age=intid)
        else:
            return agedb.listLatestFiles(age=intid)

class agefile_specific:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=common.render_file_info,
        txt=common.render_file_info,
        json=common.render_json,
    )
    @common.enable_cors()
    def GET(self, ageid, version, tag):
        if not version in config.acceptable_game_versions:
            raise web.notfound()
        try:
            intid = int(ageid)
            intid = ageid
        except:
            intid = agedb.ageFromName(ageid)
        if tag == 'verified':
            return agedb.latestFile(status='VERIFIED', gamever=version, age=intid)
        else:
            return agedb.latestFile(gamever=version, age=intid)

if __name__ == "__main__":
    app.run()
