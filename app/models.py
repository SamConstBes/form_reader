from typing import List, Optional

class ProcessData:
    def __init__(self, val1, val2, val3):
        self.val1 = val1
        self.val2 = val2
        self.val3 = val3


class Social:
    def __init__(self, tgLink=None, youlaLink=None, flowLink=None, avitoLink=None, vkLink=None, vkMess=None, phone=None):
        self.tgLink = tgLink
        self.youlaLink = youlaLink 
        self.flowLink = flowLink 
        self.avitoLink = avitoLink
        self.vkLink = vkLink
        self.vkMess = vkMess
        self.phone = phone


class DockPath:
    def __init__(self, docText=None):
        self.docText = docText

class DockPolit:
    def __init__(self, docPolit=None):
        self.docPolit = docPolit