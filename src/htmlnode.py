
# Define HTMLNode class
# tag -> A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
# value -> A string representing the value of the HTML tag
# children ->A list of HTMLNode objects representing the children of this node
# props -> A dictionary of key-value pairs representing the attributes of the HTML tag

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # child classes will override this method
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    # Returns a string that represents the HTML attributes of the node. href="https://www.google.com" target="_blank"
    def props_to_html(self):
        if self.props is None:
            return ""
        url = ""
        for attribute in self.props:
            url += f' {attribute}="{self.props[attribute]}"'
        return url
    
    # Print HTML node tag, value, children, and props.
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

# define LeafNode class
# single HTML tag with no children  
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # call constructor of HTMLNode class
        super().__init__(tag, value, None, props)

    # Render a leaf node as HTML string
    def to_html(self):
        # Raise ValueError is lead node has no value
        if self.value == None:
            raise ValueError("invalid HTML: no value")
        # return value as raw text if there is no tag
        if self.tag == None:
            return self.value
        # render HTML tag
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    # Print leaf node
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

# Define ParentNode class    
# tag and children arguments are not optional
# no value arugment
# props is optional
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # call constructor of HTMLNode class
        super().__init__(tag, None, children, props)

    def to_html(self):
        # Raise ValueError if there is no tag
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        # Raise ValueError if there are no children
        if self.children is None:
            raise ValueError("parent must have children")
        # Return string representing HTML tag of the node and children
        url = f"<{self.tag}>"
        for child in self.children:
            url += f"{child.to_html()}"
        return f"{url}</{self.tag}>"
        
    # Print parent node
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
        