#!/usr/bin/env python
import web
urls = (
    '/', 'index',
)
app = web.application(urls, globals())
render = web.template.render('html/')

class index:        
    def GET(self):
        i = web.input()
        page = Page()
        return render.generic()

class Page(object):
    def __init__(self, **kwargs):
        self.title = getattr(kwargs,'title','')
        self.header = []
        self.content = []
        self.footer = []
    def add(self,item):
        pass

class Link(object):
    def __init__(self, title='',href='',transition='',**kwargs):
        self.title = getattr(kwargs,"title",title)
        self.href = getattr(kwargs,"href",href)
        self.transition = getattr(kwargs,"transition",transition)

if __name__ == "__main__":
    app.run()
