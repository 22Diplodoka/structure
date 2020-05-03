class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        self.klass = klass
        self.kwargs = kwargs

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        if self.klass is not None:
            self.attributes["class"] = " ".join(self.klass)

        for at, value in self.kwargs.items():
            if "_" in at:
                at = at.replace("_", "-")
            self.attributes[at] = value

        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</{tag}>".format(tag=self.tag)
            return str(opening + "\n" + internal + ending) + "\n"
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs) + "\n"
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text) + "\n"


class TopLevelTag(Tag):
    pass


class HTML:

    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __str__(self):
        html = "<html>" + "\n"
        for child in self.children:
            html += str(child)
        html += "</html>"
        return html + "\n"

    def __exit__(self, *args, **kwargs):
        if self.output is None:
            print(self)


def main():
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body


if __name__ == "__main__":
    main()