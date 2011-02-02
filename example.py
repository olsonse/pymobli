#!/usr/bin/env python
from pymobli import Page, Button, Title, Link, Button, ButtonGroup, Inline, List
import web
urls = (
    '/', 'index',
)
app = web.application(urls, globals())
render = web.template.render('html/')

class index:        
    def GET(self):
        i = web.input()
        
        #Browser Title
        page = Page("Example Page Title")

        #Header Title
        #page.header.title = "Example Page"

        page.header.add(Button(title="Back",href="#", icon="arrow-l", theme="e"))
        page.header.add(Title(title="Example Page"))
        page.header.add(Link(title="Yahoo",href="http://www.yahoo.com"))

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

        page.content.append(Button('This is an "a" themed button',"http://jquery.com", theme="a"))
        page.content.append(Button('This is a "b" themed button',"http://jquery.com", theme="b"))
        
        b = ButtonGroup()
        b.add(Button("This is a button group","http://jquery.com"))
        b.add(Button("Boom","http://boom.com"))

        page.content.append(b)

        b = ButtonGroup(style="horizontal")
        b.add(Button("Yes", theme="e"))
        b.add(Button("No"))
        b.add(Button("Maybe"))
        page.content.append(b)

        b = ButtonGroup(style="horizontal")
        b.add(Button("Up", icon="arrow-u"))
        b.add(Button("Down", icon="arrow-d"))
        b.add(Button("X", icon="delete"))
        page.content.append(b)

        #page.content.append(Text(content="Horizontal buttons", type="code"))

        b = ButtonGroup(style="horizontal")
        b.add(Button(icon="arrow-u"))
        b.add(Button(icon="arrow-d"))
        b.add(Button(icon="delete"))
        page.content.append(b)

        #page.content.append(Text(content="Inline buttons"))
        i = Inline()
        i.add(Button("Cancel", inline="true"))
        i.add(Button("Save", theme="b",inline="true"))

        page.content.append(i)

        return render.generic(page)
if __name__ == "__main__":
    app.run()
