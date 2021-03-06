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
    D = super(DictBase,self).copy()
    D['attrib'] = self.attrib
    D.update(kw)
    return D
  def copy(self):
    return DictBase( super(DictBase,self).copy() )

def is_list(a):
  # for the context of tags and content here, str types are not iterable
  if type(a) in [list, tuple]: return True
  return False

#List types == nested,numbered,read-only,splitbutton
class GroupBase(DictBase):
  def __init__(self, style="", filter="false", inset="false", title="",
               content='', *args, **kwargs):
    super(GroupBase,self).__init__(*args,**kwargs)
    self.style = style
    self.title = title
    self.items = (content == '' and []) or \
                 (is_list(content) and content) or [content]
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

class Video(GroupBase):
  class Source(object):
    def __init__(self, src, type):
      self.src = src
      self.type = type
    def __repr__(self):
      return '<source src="{src}" type="{type}">' \
        .format(src=self.src, type=self.type)
  def __init__(self, autoplay=False, controls=True, loop=False, muted=False,
               *args, **kwargs):
    super(Video,self).__init__(*args, **kwargs)
    self._autoplay = autoplay
    self._controls = controls
    self._loop = loop
    self._muted = muted
  def __repr__(self):
    return \
    '<video {attrib} {autoplay} {controls} {loop} {muted}> {items}\n</video>' \
      .format(autoplay = self._autoplay and 'autoplay' or '',
              controls = self._controls and 'controls' or '',
              loop     = self._loop     and 'loop '    or '',
              muted    = self._muted    and 'muted '   or '',
              **self.dict())

class Form(GroupBase):
    def __repr__(self):
        return '<form %(attrib)s> %(items)s </form>' % self.dict()

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
        return '<a %(attrib)s %(href)s %(transition)s %(theme)s>%(title)s</a>' \
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

# some stuff useful for forms
# TODO:  move this into a subpackage for forms
class Label(GroupBase):
  def __init__(self, _for='', hidden=False, *args, **kwargs):
    super(Label,self).__init__(*args, **kwargs)
    self._for = _for
    if hidden:
      self.attributes['class']='ui-hidden-accessible'
  def __repr__(self):
    return '<label for={_for} {attrib}>{title}{items}</label>' \
           .format(**self.dict())

class Input(DictBase):
    def __init__(self, theme='a', autofocus=False, *args, **kwargs):
        super(Input,self).__init__(*args,**kwargs)
        self.theme = (theme and 'data-theme="{}"'.format(theme)) or ''
        self._autofocus = autofocus
    def __repr__(self):
        return '<input {attrib} {theme} {autofocus}/>' \
          .format( autofocus = self._autofocus and 'autofocus' or '',
                   **self.dict() )

class FormInput(object):
  def __init__(self, type, name, value='', placeholder='', theme='a',
               label='', autofocus=False,
               label_attrib=dict(), input_attrib=dict() ):
    self.label = Label( _for=name, title=label, attrib=input_attrib )
    self.input = Input(
      type=type, name=name, id=name, value=value, autofocus=autofocus,
      placeholder=placeholder, theme=theme, attrib=input_attrib,
    )
  def __repr__(self):
     return '{} {}'.format(self.label, self.input)

class FormButton(ItemBase):
    def __repr__(self):
        return '<button {attrib} {inline} {icon} ' \
               '{transition} {theme}>{title}</button>' \
               .format( **self.dict() )


class FormSelectOption(GroupBase):
  def __init__(self, *args, **kwargs):
    selected = (kwargs.pop('selected',False) and 'selected') or ''
    super(FormSelectOption,self).__init__(*args, **kwargs)
    self.selected = selected

  def __repr__(self):
    D = self.dict()
    return '<option {attrib} {selected}>{title}{items}</option>'.format(**D)

class FormSelect(list):
  def __init__(self, name, label='Select:', *args, **kwargs):
    super(FormSelect,self).__init__(*args, **kwargs)
    self.name = name
    self.label=label

  def add(self, value, content=None, selected=False):
    self.append(FormSelectOption(
      value=value, content=(content or value), selected=selected,
    ))

  def __repr__(self):
    return \
      '<div class="ui-field-contain">\n' \
      '  <label for="{name}">{label}</label>\n' \
      '  <select name="{name}" id="{name}">\n' \
      '    {options}\n' \
      '  </select>\n' \
      '</div>' \
      .format(
        name=self.name, label=self.label,
        options='\n'.join([ repr(i) for i in self ]),
      )
