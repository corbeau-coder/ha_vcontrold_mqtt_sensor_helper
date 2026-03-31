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
    
class TreeElement(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    path: str
    root_elem: ET.Element
    cmd_list: list[CommandElement] = []

    @classmethod
    def fetch_data(cls, path):
        cmd_list: list[CommandElement] = []
        try:
            root_elem = ET.parse(path).getroot()
        except (FileNotFoundError, ET.ParseError) as e:
            logger.error(f"Error parsing xml file {path} - Exception {str(e)}")
            raise e
        for item in root_elem.iterfind('command'):
            cmd_list.append(CommandElement.fill_from_xml(item))
        return cls(path = path,
                   root_elem = root_elem,
                   cmd_list = cmd_list)
