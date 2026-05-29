from pymonad.tools import curry

# 2.3.1.
@curry(2)
def concat(str1, str2):
    return str1 + str2

hello = concat("Hello, ")
print(hello("Max"))

# 2.3.2.
@curry(4)
def template(str1, str2, str3, str4):
    return str1 + str2 + str4 + str3

prefilledTemplate = template("Hello")(", ")("!")
print(prefilledTemplate("Petya"))