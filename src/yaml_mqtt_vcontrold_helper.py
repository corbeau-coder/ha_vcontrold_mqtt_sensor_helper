import argparse
from loguru import logger
import sys
from src.modules.xml_parser import TreeElement

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
        logger.level("DEBUG")
        logger.info("verbose output enabled")
    else:
        logger.level("INFO")

    if args.c:
        logger.info("Creating yaml configuration ...")

        logger.info("done. Created configuration.yaml sucessfully")
        

    if args.d:
        logger.info("Removing all device-specific elements ...")

        root_elem = TreeElement.fetch_data(path)
        root_elem.remove_dev_refs()
        root_elem.write_xml_file(path)


        logger.info("done. Removed all device elements in vito.xml")
        

    sys.exit(0)



"""  parser.add_argument(
        "-i",
        type=str,
        help="input path used for vito.xml, if empty, vito.xml in actual directory will be used",
        default="vito.xml"
    )

    parser.add_argument(
        "-o",
        type=str,
        help="output path where yaml content should be written to - has to be a file, not a directory. actual directory with filename configuration.yaml will be used by default",
        default="configuration.yaml"
    )
"""

    



    #parse tree #xml
    #extrude items into models #jinja2
    #write configuration.yaml
    

if __name__ == "__main__":
    path = "vito.xml"
    main(path)
