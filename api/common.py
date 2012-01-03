import web
import json

input_key = '_accept'

default_encoding = 'html'

render_json = lambda **arg: json.dumps(arg)
render_json_list = lambda *arg: json.dumps(arg)

template = web.template.render('templates/')

def render_file_info(**finfo):
    return template.filepage(finfo)
def render_file_list(*files):
    return template.filelist(files)

class MissingParam(web.BadRequest):
    def __init__(self):
        web.BadRequest.__init__(self)
        self.data = 'A required paramater was not provided'

class BadParam(web.BadRequest):
    def __init__(self, param):
        web.BadRequest.__init__(self)
        self.data = 'Paramater contains an invalid value: '+param

def enable_cors(methods = None):
    def enable_cors(method):
        def wrap(*args, **kwds):
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Expose-Headers', 'Content-Type')
            web.header('Access-Control-Allow-Headers', 'Accept')
            if methods:
                web.header('Access-Control-Allow-Methods', methods)
            return method(*args, **kwds)
        return wrap
    return enable_cors
