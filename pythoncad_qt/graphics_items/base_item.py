
class BaseItem(object):
    def __init__(self):
        self.children = []

    def add_child(self, item):
        item.parent = self
        self.children.append(item)
