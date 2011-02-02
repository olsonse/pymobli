#!/usr/bin/env python
class DictObj(object):
    def __getitem__(self, attr):
        return getattr(self,attr,"")

class Page(object):
    def __init__(self, title=""):
        self.title = title
        self.header = Header(title="")
        self.content = []
        self.footer = []

#List types == nested,numbered,read-only,splitbutton
class GroupBase(DictObj):
    def __init__(self, style="", filter="false", inset="false", title=""):
        self.style = style
        self.title = title
        self.items = []
        self.filter = filter
        self.inset = inset
    def add(self,li):
        self.items.append(li)

class Header(GroupBase):
    def __repr__(self):
        self.items = "\n".join(["%s" % a for a in self.items])
        return '''
<div data-role="header">
%(items)s
</div>
''' % self

class Title(GroupBase):
    def __repr__(self):
        return '<h1>%(title)s</h1>' % self

    
class List(GroupBase):
    def __repr__(self):
        if self.style == "numbered": self.style = "ol"
        else: self.style = "ul"
        self.items = "\n".join(["<li>%s</li>" % a for a in self.items])
        return '''
<%(style)s data-role="listview" data-filter="%(filter)s" data-inset="%(inset)s">
%(items)s
</%(style)s>''' % self

class Text(DictObj):
    def __init__(self,content="", type=""):
        self.content = content
        if type == "code": self.tag = "code"
        else: self.tag = "p"
    def __repr__(self):
        return "<%(tag)s>%(content)s</%(code)s>" % self

class ButtonGroup(GroupBase):
    def __repr__(self):
        self.items = "\n".join(["%s" % a for a in self.items])
        return '''
<div data-role="controlgroup" data-type="%(style)s">
%(items)s
</div>''' % self
    
class Inline(GroupBase):
    def __repr__(self):
        self.items = "\n".join(["%s" % a for a in self.items])
        return '''
<div data-inline="true">
%(items)s
</div>''' % self

class ItemBase(DictObj):
    def __init__(self, title='',href='',transition='slide', icon="", theme="c", inline=""):
        self.title = title
        self.href = href and 'href="%s"' % href or ""
        self.transition = transition and 'data-transition="%s"' % transition or ""
        self.icon = icon and 'data-icon="%s"' % icon or ""
        self.theme = theme and 'data-theme="%s"' % theme or ""
        self.inline = inline and 'data-inline="%s"' % inline or ""
        if not title and icon:
            self.icon = 'data-icon="%s" data-iconpos="notext"' % icon
        self.quickattrs = '%(href)s %(transition)s' % self

class Link(ItemBase):
    def __repr__(self):
        return '<a %(href)s %(transition)s>%(title)s</a>' % self

class Button(ItemBase):
    def __repr__(self):
        return '<a data-role="button" %(inline)s %(icon)s %(href)s %(transition)s %(theme)s>%(title)s</a>' % self
