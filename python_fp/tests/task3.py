from pymonad.tools import curry

# 3.1.
@curry(2)
def tag(tag_name, value):
    return '<' + tag_name + '>' + value + '</' + tag_name + '>'

bold = tag('b')
italic = tag('i')

print(italic("Petya"))
print(bold("Petya"))


# 3.2.
@curry(3)
def tag_ext(tag_name, attr, value):
    if attr is None or len(attr) == 0:
        return tag(tag_name, value)

    attrs = ' '.join(
        key + '="' + val + '"'
        for key, val in attr.items()
    )

    return '<' + tag_name + ' ' + attrs + '>' + value + '</' + tag_name + '>'

print(tag_ext('li', None,'item 23'))
print(tag_ext('li', {'class': 'list-group'}, 'item 23'))
print(tag_ext('li', {'class': 'list-group', 'class1': 'list-group1'}, 'item 23'))