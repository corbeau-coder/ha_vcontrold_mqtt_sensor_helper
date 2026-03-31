from pydantic import BaseModel
import xml.etree.ElementTree as ET

#parse tree
#find all commands

class CommandElement(BaseModel):
    def __init__(self, element: ET.Element):
        self.name = element.attrib['name']
        self.unittype = element.find('unit').text
        self.desc = element.find('description').text