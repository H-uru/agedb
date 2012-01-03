import web

forms = web.template.render('forms/')

urls = (
    r'/(\w+)/?', 'showform',
)
app = web.application(urls, locals())

class showform:
    def GET(self, form):
        return forms.__getattr__(form)()
