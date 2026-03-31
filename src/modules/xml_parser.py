from pydantic import BaseModel
import xml.etree.ElementTree as ET
from loguru import logger

#parse tree
#find all commands

class CommandElement(BaseModel):
    name: str
    unittype: str
    desc: str

    @classmethod
    def fill_from_xml(cls, element: ET.Element):
        return cls(
            name = element.get("name"),
            unittype = element.find('unit').text,
            desc = element.find('description').text)