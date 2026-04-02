import argparse
from loguru import logger
import sys
from src.modules.xml_parser.xml_parser import TreeElement
from src.modules.template_engine.template_engine import YamlRenderer

def main(path):
    #switch case argparse
    parser = argparse.ArgumentParser(
        prog="yaml_mqtt_vcontrold_helper",
        description="small helper creating a configuration yaml for home assistant out of all commands of an vito.xml",
        epilog="as always written for fun",
    )
    
    parser.add_argument(
        "-c",
        help="create configuration.yaml of all commands according to vito.xml.",
        action="store_true"
    )

    parser.add_argument(
        "-d",
        help="removes all <devices> and <device> elements in the vito.xml.",
        action="store_true"
    )

    parser.add_argument(
        "-v",
        help="verbose output",
        action="store_true"
    )

    args = parser.parse_args()

    if args.v:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
        logger.info("verbose output enabled")
    else:
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    if args.c:
        logger.info("Creating yaml configuration ...")
        root_elem = TreeElement.fetch_data(path)
        #business logic deviding cmds into groups for sensors and other templates
        
        
        logger.info("done. Created configuration.yaml sucessfully")
        

    if args.d:
        logger.info("Removing all device-specific elements ...")

        root_elem = TreeElement.fetch_data(path)
        root_elem.remove_dev_refs()
        root_elem.write_xml_file(path)


        logger.info("done. Removed all device elements in vito.xml")
        

    sys.exit(0)


    #write configuration.yaml
    

if __name__ == "__main__":
    path = "vito.xml"
    main(path)
