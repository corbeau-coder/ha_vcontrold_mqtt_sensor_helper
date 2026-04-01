from pydantic import BaseModel
import xml.etree.ElementTree as ET
from loguru import logger
from abc import ABC, abstractmethod

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


class XmlLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> ET.Element: ...

class FileXmlLoader(XmlLoader):
    def load(self, path: str) -> ET.Element:
        return ET.parse(path).getroot()


class TreeElement(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    path: str
    root_elem: ET.Element
    cmd_list: list[CommandElement] = []

    @classmethod
    def fetch_data(cls, path: str, loader: XmlLoader = FileXmlLoader()):
        cmd_list: list[CommandElement] = []
        try:
            root_elem = loader.load(path)
        except (FileNotFoundError, ET.ParseError) as e:
            logger.error(f"Error parsing xml file {path} - Exception {str(e)}")
            raise
        cmd_list = [CommandElement.fill_from_xml(item) for item in root_elem.iterfind('commands/command')]
        return cls(path = path,
                   root_elem = root_elem,
                   cmd_list = cmd_list)
    
    def remove_dev_refs(self):
        devices = self.root_elem.find('devices')
        if devices is not None:
            self.root_elem.remove(devices)

        for parent in self.root_elem.iter():
            for child in list(parent):
                if child.tag == 'device':
                    parent.remove(child)
