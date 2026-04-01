import argparse
from loguru import logger
import sys

def main(path):
    #switch case argparse
    parser = argparse.ArgumentParser(
        prog="yaml_mqtt_vcontrold_helper",
        description="small helper creating a configuration yaml for home assistant out of all commands of an vito.xml",
        epilog="as always written for fun",
    )
    
    parser.add_argument(
        "-c",
        type=str,
        help="create configuration.yaml of all commands according to vito.xml.",
        nargs="?"
    )

    parser.add_argument(
        "-d",
        type=str,
        help="removes all <devices> and <device> elements in the vito.xml.",
        nargs="?"
    )

    parser.add_argument(
        "-v",
        type=str,
        help="verbose output",
        nargs="?"
    )

    args = parser.parse_args()


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
