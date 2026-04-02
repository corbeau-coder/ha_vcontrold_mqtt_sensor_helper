from jinja2 import Environment, FileSystemLoader
from src.modules.xml_parser.xml_parser import CommandElement
from pathlib import Path


class YamlRenderer():
    def aggregate_yaml(self, list_tmpl_renderer: list[str]) -> str:
        todo
        pass

    def generate_template_yaml(self, list_cmdelem: list[CommandElement], tmpl_path: str) -> str:
        p = Path(tmpl_path)
        env = Environment(loader=FileSystemLoader(p.parent, encoding="utf-8"))
        output_template = env.get_template(p.name)
        return output_template.render(sensor_list=list_cmdelem)
    
    def write_yaml_file(self, input_string: str, yaml_file: str="configuration.yaml"):
        pass