#!/usr/bin/env python
import web
urls = (
    '/', 'index',
)
app = web.application(urls, globals())
render = web.template.render('html/')

class DictObj(object):
    def __getitem__(self, attr):
        return getattr(self,attr,"")

class index:        
    def GET(self):
        i = web.input()
        page = Page("My PAGE")
        l  = List()
        l.items.append(Link(title="Google",href="http://www.google.com"))
        l.items.append(Link(title="My Blog",href="http://patrickshuff.com"))
        l.items.append(Link(title="OHIO STATE",href="http://osu.edu"))
        page.content.append(l)
        return render.generic(page)

class Base(object):
    items = []

class Page(object):
    def __init__(self, title="", **kwargs):
        self.title = getattr(kwargs,'title','')
        self.header = getattr(kwargs,"header",[])
        self.content = getattr(kwargs,"content",[])
        self.footer = getattr(kwargs,"footer",[])

#List types == nested,numbered,read-only,splitbutton

class List(DictObj):
    def __init__(self, style="basic", filter="false", inset="false"):
        self.type = "list"
        self.style = style
        self.items = []
        self.filter = filter
        self.inset = inset
    def __unicode__(self):
        if self.style == "numbered": self.style = "ol"
        else: self.style = "ul"
        self.items = "\n".join(["<li>%s</li>" % a for a in self.items])
        return '''
<%(style)s data-role="listview" data-filter="%(filter)s" data-inset="%(inset)s">
%(items)s
</%(style)s>''' % self


class Link(DictObj):
    def __init__(self, title='',href='',transition='slide',**kwargs):
        self.title = getattr(kwargs,"title",title)
        self.href = getattr(kwargs,"href",href)
        self.transition = getattr(kwargs,"transition",transition)
        self.type = "link"
    def __repr__(self):
        return str('<a href="%s" data-transition="%s">%s</a>' % (self.href, self.transition, self.title))


if __name__ == "__main__":
    app.run()
