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

        b = ButtonGroup(style="horizontal")
        b.add(Button("Up", icon="arrow-u"))
        b.add(Button("Down", icon="arrow-d"))
        b.add(Button("X", icon="delete"))
        page.content.append(b)

        b = ButtonGroup(style="horizontal")
        b.add(Button(icon="arrow-u"))
        b.add(Button(icon="arrow-d"))
        b.add(Button(icon="delete"))
        page.content.append(b)

        return render.generic(page)

class Page(object):
    def __init__(self, title=""):
        self.title = title
        self.header = []
        self.content = []
        self.footer = []

#List types == nested,numbered,read-only,splitbutton

class GroupBase(DictObj):
    def __init__(self, style="", filter="false", inset="false"):
        self.style = style
        self.items = []
        self.filter = filter
        self.inset = inset
    def add(self,li):
        self.items.append(li)
    
class List(GroupBase):
    def __repr__(self):
        if self.style == "numbered": self.style = "ol"
        else: self.style = "ul"
        self.items = "\n".join(["<li>%s</li>" % a for a in self.items])
        return '''
<%(style)s data-role="listview" data-filter="%(filter)s" data-inset="%(inset)s">
%(items)s
</%(style)s>''' % self


class ButtonGroup(GroupBase):
    def __repr__(self):
        self.items = "\n".join(["%s" % a for a in self.items])
        return '''
<div data-role="controlgroup" data-type="%(style)s">
%(items)s
</div>''' % self
    

class ItemBase(DictObj):
    def __init__(self, title='',href='',transition='slide', icon=""):
        self.title = title
        self.href = 'href="%s"' % href
        self.transition = 'data-transition="%s"' % transition
        self.icon = 'data-icon="%s"' % icon

class Link(ItemBase):
    def __repr__(self):
        if self.href:
            return '<a %(attributes)s">%(title)s</a>' % self
        else:
            return '<a %(transition)s>%(title)s</a>' % self

class Button(ItemBase):
    def __repr__(self):
        self.role = 'data-role="button"'
        if self.icon:
            if not self.title:
                return '<a href="%(href)s" %(role)s  %(icon)s data-iconpos="notext" %(transition)s></a>' % self
            return '<a %(href)s %(role)s %(icon)s %(transition)s">%(title)s</a>' % self
        return '<a %(href)s %(role)s %(transition)s>%(title)s</a>' % self
if __name__ == "__main__":
    app.run()
