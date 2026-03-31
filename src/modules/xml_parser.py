from pydantic import BaseModel
import xml.etree.ElementTree as ET
from loguru import logger

#parse tree
#find all commands

class CommandElement(BaseModel):
    def __init__(self, element: ET.Element):
        self.name = element.get("name")
        self.unittype = element.find('unit').text
        self.desc = element.find('description').text