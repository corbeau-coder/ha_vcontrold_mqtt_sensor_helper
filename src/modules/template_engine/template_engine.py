from jinja2 import Template, Environment, FileSystemLoader
from src.modules.xml_parser.xml_parser import CommandElement
from pathlib import Path


class YamlRenderer():

    def generate_yaml(self, list_cmdelem: list[CommandElement], tmpl_path: str) -> str:
        p = Path(tmpl_path)
        env = Environment(loader=FileSystemLoader(p.parent, encoding="utf-8"))
        output_template = env.get_template(p.name)
        return output_template.render(sensor_list=list_cmdelem)
    
    def write_yaml_file(yaml_file: str="configuration.yaml"):
        pass