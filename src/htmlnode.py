from typing import Dict


class HTMLNode:
  def __init__(self, tag = None, value = None, children = None, props = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError

  def props_to_html(self):
    html_string = ""
    if not self.props:
      return html_string
    for prop in self.props:
      html_string += f' {prop}="{self.props[prop]}"'

    return html_string

  def __repr__(self):
    return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
  def __init__(self, tag, value, props = None):
    super().__init__(tag=tag, value=value, children=None, props=props)

  def to_html(self):
    if not self.value:
      raise ValueError("LeafNode must have a value to convert to HTML")
    if not self.tag:
      return self.value

    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
  def __init__(self, tag, children, props = None):
    super().__init__(tag = tag, children = children, props = props)

  def to_html(self):
    if not self.tag: 
      raise ValueError("ParentNode must have a tag to convert to HTML")
    if not self.children:
      raise ValueError("ParentNode must have children to convert to HTML")

    inner_html = ""
    for child in self.children:
      inner_html += child.to_html()

    return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"
