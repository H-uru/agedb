import web
import mimerender

import agedb

import common
import config

urls = (
    r'/?', 'listfiles',
    r'/(latest|verified)/?', 'taggedfiles',
    r'/(\d+\.\d+)/?', 'versionfiles',
    r'/(\d+\.\d+)/(latest|verified)/?', 'taggedversionfiles',
    r'/(\d+)/?', 'showfile',
    r'/(\d+)/download', 'getfile'
)
app = web.application(urls, locals())

class showfile:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=common.render_file_info,
        txt=common.render_file_info,
        json=common.render_json,
    )
    @common.enable_cors()
    def GET(self, fileid):
        return agedb.queryFile(fileid)

class getfile:
    def GET(self, fileid):
        ageid = agedb.ageFromFile(fileid);
        agename = agedb.ageName(ageid);
        web.header('Content-type', 'application/zip')
        web.header('Content-Disposition', 'attachment; filename='+agename+'.zip')
        file = open(config.agefiles_path+str(fileid)+'.zip')
        return file.read();

class listfiles:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=common.render_file_list,
        txt=common.render_file_list,
        json=common.render_json_list,
        islist = True
    )
    @common.enable_cors()
    def GET(self):
        return agedb.listFiles()
        
class taggedfiles:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=common.render_file_list,
        txt=common.render_file_list,
        json=common.render_json_list,
        islist = True
    )
    @common.enable_cors()
    def GET(self, tag):
        if tag == "verified":
            return agedb.listLatestFiles(status='VERIFIED')
        else:
            return agedb.listLatestFiles()

class versionfiles:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=common.render_file_list,
        txt=common.render_file_list,
        json=common.render_json_list,
        islist = True
    )
    @common.enable_cors()
    def GET(self, version):
        if not version in config.acceptable_game_versions:
            raise web.notfound()
        return agedb.listFiles(gamever=version)

class taggedversionfiles:
    @mimerender.mimerender(
        default=common.default_encoding,
        override_input_key=common.input_key,
        html=common.render_file_list,
        txt=common.render_file_list,
        json=common.render_json_list,
        islist = True
    )
    @common.enable_cors()
    def GET(self, version, tag):
        if not version in config.acceptable_game_versions:
            raise web.notfound()
        if tag == 'verified':
            return agedb.listLatestFiles(status='VERIFIED', gamever=version)
        else:
            return agedb.listLatestFiles(gamever=version)

