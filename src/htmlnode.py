
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.children:
            children_html = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}>{children_html}</{self.tag}>"
        elif self.value is not None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return ""
        
    @staticmethod
    def props_to_html(props):
        if props is None:
            return ""
        props_str = ""
        for prop_name, prop_value in props.items():
            props_str += f' {prop_name}="{prop_value}"'
        return props_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"