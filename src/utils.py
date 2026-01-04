from textnode import TextNode, TextType
# hmm ok so if I have delimeter, I need to make sure that there...
# 1. is a closing tag for delimiter type, else raise exception
def split_nodes_delimiter(old_nodes, delimiter, text_type):
  split_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      split_nodes.append(node)
      continue
    # how do I detect if a delimiter is missing a closing tag? 
    # ohh if there are even number of items in the list after splitting, you know that there is a missing closing tag!!
    parts = node.text.split(delimiter)
    if len(parts) % 2 == 0:
      raise ValueError(f"Invalid markdown: Missing closing delimiter for {delimiter} in text")
    for i, part in enumerate(parts):
      if i % 2 == 0:
        split_nodes.append(TextNode(part, TextType.PLAIN))
      else:
        split_nodes.append(TextNode(part, text_type))
  
  return split_nodes


if __name__ == "__main__":
    # This only runs if you execute this file directly,
    # not when you import it elsewhere.
    print("Running utility script...")
