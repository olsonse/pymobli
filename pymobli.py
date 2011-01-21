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
        l  = List(inset="true")
        ## Link definitions
        l.add(Link("OHIO STATE","http://osu.edu"))
        l.add(Link(title="Google",href="http://www.google.com"))
        d = {"title":"My Blog", "href":"http://patrickshuff.com"}
        l.add(Link("Broken Link"))
        l.add(Link(**d))
        page.content.append(l)

        l  = List(inset="true")
        l.add(Link("OHIO STATE","http://osu.edu"))
        l.add(Link(title="Google",href="http://www.google.com"))
        d = {"title":"My Blog", "href":"http://patrickshuff.com"}
        l.add(Link("Broken Link"))
        l.add(Link(**d))
        page.content.append(l)

        page.content.append(Button("This is a button","http://jquery.com"))
        
        b = ButtonGroup()
        b.add(Button("This is a button group","http://jquery.com"))
        b.add(Button("Boom","http://boom.com"))

        page.content.append(b)

        b = ButtonGroup(style="horizontal")
        b.add(Button("Yes"))
        b.add(Button("No"))
        b.add(Button("Maybe"))

        page.content.append(b)

        return render.generic(page)

class Page(object):
    def __init__(self, title=""):
        self.title = title
        self.header = []
        self.content = []
        self.footer = []

#List types == nested,numbered,read-only,splitbutton

class List(DictObj):
    def __init__(self, style="", filter="false", inset="false"):
        self.style = style
        self.items = []
        self.filter = filter
        self.inset = inset
    def add(self,li):
        self.items.append(li)
    def __repr__(self):
        if self.style == "numbered": self.style = "ol"
        else: self.style = "ul"
        self.items = "\n".join(["<li>%s</li>" % a for a in self.items])
        return '''
<%(style)s data-role="listview" data-filter="%(filter)s" data-inset="%(inset)s">
%(items)s
</%(style)s>''' % self

class ButtonGroup(List):
    def __init__(self, style=""):
        self.style = style
        self.items = []
    def __repr__(self):
        self.items = "\n".join(["%s" % a for a in self.items])
        return '''
<div data-role="controlgroup" data-type="%(style)s">
%(items)s
</div>''' % self
    

class Link(DictObj):
    def __init__(self, title='',href='',transition='slide'):
        self.title = title
        self.href = href
        self.transition = transition
        self.type = "link"
    def __repr__(self):
        if self.href:
            return '<a href="%(href)s" data-transition="%(transition)s">%(title)s</a>' % self
        else:
            return '<a data-transition="%(transition)s">%(title)s</a>' % self

class Button(Link):
    def __repr__(self):
        return '<a href="%(href)s" data-role="button" data-transition="%(transition)s">%(title)s</a>' % self

if __name__ == "__main__":
    app.run()
