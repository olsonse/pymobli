#!/usr/bin/env python
import re

class Page(dict):
    def __init__(self, title=""):
        super(Page,self).__init__()
        self.__dict__ = self
        self.title = title
        self.header = Header(title="")
        self.content = []
        self.footer = []

class DictBase(dict):
  def __init__(self, attrib=dict(), **attrib_kwargs):
    super(DictBase,self).__init__()
    self.__dict__ = self
    self.attributes = attrib.copy()
    self.attributes.update( attrib_kwargs )
  @property
  def attrib(self):
    return ' '.join([
      '{}={}'.format(i[0],repr(i[1]))
      for i in self.attributes.items()
    ])
  def dict(self, **kw):
    D = self.copy()
    D['attrib'] = self.attrib
    D.update(kw)
    return D

#List types == nested,numbered,read-only,splitbutton
class GroupBase(DictBase):
  def __init__(self, style="", filter="false", inset="false", title="",
               content='', *args, **kwargs):
    super(GroupBase,self).__init__(*args,**kwargs)
    self.style = style
    self.title = title
    self.items = (content == '' and []) or [content]
    self.filter = filter
    self.inset = inset
  def add(self,li):
    self.items.append(li)
  def dict(self, tag='', **kw):
    D = super(GroupBase,self).dict(**kw)
    m = re.match('<([^>]*)>', tag)
    if m:
      ti,tf = '<{}>'.format(m.group(1)), '</{}>'.format(m.group(1))
    else: ti,tf = '', ''
    D['items'] = "\n".join(['{}{}{}'.format(ti,a,tf) for a in self.items])
    return D


class Header(GroupBase):
    def __repr__(self):
        return '''
<div data-role="header" %(attrib)s>
%(items)s
</div>
''' % self.dict()

class Title(GroupBase):
  def __init__(self, level=1, *args, **kwargs):
    super(Title,self).__init__(*args, **kwargs)
    self.level = level
  def __repr__(self):
    return '<h{level} {attrib}>{title}{items}</h{level}>'.format(**self.dict())

    
class List(GroupBase):
    def __repr__(self):
        style = "ul"
        if self.style == "numbered": style = "ol"
        return '''
<%(style)s data-role="listview" data-filter="%(filter)s"
 data-inset="%(inset)s" %(attrib)s>
%(items)s
</%(style)s>''' % self.dict(tag='<li>', style=style)

class Text(DictBase):
    def __init__(self,content="", type="", *args, **kwargs):
        super(Text,self).__init__(*args,**kwargs)
        self.content = content
        if type == "code": self.tag = "code"
        else:              self.tag = "p"
    def __repr__(self):
        return "<%(tag)s %(attrib)s>%(content)s</%(tag)s>" % self.dict()

class ButtonGroup(GroupBase):
    def __repr__(self):
        return '''
<div data-role="controlgroup" data-type="%(style)s" %(attrib)s>
%(items)s
</div>''' % self.dict()
    
class Inline(GroupBase):
    def __repr__(self):
        return '''
<div data-inline="true" %(attrib)s>
%(items)s
</div>''' % self.dict()

class Div(GroupBase):
    def __repr__(self):
        return '<div %(attrib)s> %(items)s </div>' % self.dict()

class ItemBase(DictBase):
    def __init__(self, title='', href='', transition='slide', icon="",
                 theme="c", inline="", *args, **kwargs):
        super(ItemBase,self).__init__(*args, **kwargs)
        self.title = title
        self.href = href and 'href="%s"' % href or ""
        self.transition = transition and 'data-transition="%s"' % transition or ""
        self.icon = icon and 'data-icon="%s"' % icon or ""
        self.theme = theme and 'data-theme="%s"' % theme or ""
        self.inline = inline and 'data-inline="%s"' % inline or ""
        if not title and icon:
            self.icon = 'data-icon="%s" data-iconpos="notext"' % icon
        self.quickattrs = '{} {}'.format(self.href, self.transition)

class Link(ItemBase):
    def __repr__(self):
        return '<a %(attrib)s %(href)s %(transition)s>%(title)s</a>' \
                % self.dict()

class Button(ItemBase):
    def __repr__(self):
        return '<a data-role="button" %(attrib)s %(inline)s %(icon)s ' \
               '%(href)s %(transition)s %(theme)s>%(title)s</a>' % self.dict()

class Image(ItemBase):
    def __init__(self, src='', width='', height='', *args, **kwargs):
      ItemBase.__init__(self, *args, **kwargs)
      self.src = src and 'src="%s"' % src or ""
      self.width = width and 'width="%s"' % width or ""
      self.height = height and 'height="%s"' % height or ""

    def __repr__(self):
        return '<img data-role="image" %(attrib)s %(inline)s %(icon)s ' \
               '%(src)s %(width)s %(height)s %(transition)s %(theme)s ' \
               'alt="%(title)s"/>' % self.dict()
