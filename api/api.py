import web

import ages
import users
import files
import forms

import common
import config
import userdb

urls = (
    '/', 'index',
    config.ages_path, ages.app,
    config.users_path, users.app,
    config.files_path, files.app,
    config.forms_path, forms.app,
    '/authcheck/?', 'authcheck',
    '/admincheck/?', 'admincheck',
    '/maintcheck/?', 'maintcheck',
)

app = web.application(urls, locals())

# This handles the _method hack to allow browsers that don't support PUT and DELETE
# requests to still use the API semi-correctly
def override_method(handler):
    web.ctx.method = web.input().get("_method", web.ctx.method)
    return handler()
app.add_processor(override_method)

class index:
    def GET(self):
        return "Index page. There's nothing useful here"


# These simple APIs allow an application to determine if its credentials are good
# before trying to make a request. Since we're RESTfully sessionless, there is no actual
# login process. Most users will expect some sort of login, though, and this lets your app
# do that.
class authcheck:
    @userdb.user_auth
    @common.enable_cors()
    def GET(self):
        return "Authenticated"
    
    @common.enable_cors()
    def OPTIONS(self):
        pass

class admincheck:
    @userdb.admin_auth
    @common.enable_cors()
    def GET(self):
        return "Authenticated"
    
    @common.enable_cors()
    def OPTIONS(self):
        pass

class maintcheck:
    @userdb.maintainer_auth
    @common.enable_cors()
    def GET(self):
        return "Authenticated"
    
    @common.enable_cors()
    def OPTIONS(self):
        pass

if __name__ == "__main__":
    app.run()
