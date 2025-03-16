from textnode import *

def main():
    temp = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(temp.__repr__())

main()
