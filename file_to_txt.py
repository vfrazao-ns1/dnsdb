"""
Takes a file as input and generate the appropriate TXT rdata string to store it
"""
import argparse
from typing import List


def file_as_bytes(filepath: str) -> List[str]:
    with open(filepath, "rb") as f_in:
        bytes_list = [f"\\{b:03d}" for b in f_in.read()]
    return bytes_list


def write_to_file_raw(filepath: str, bytes_list: List[str]) -> None:
    with open(filepath, "w") as f_out:
        f_out.write("".join(bytes_list))


if __name__ == "__main__":
    help_texts = {
        "main": __doc__,
        "infile": "Name of file to read from",
        "outfile": "Name of file to write output",
    }
    parser = argparse.ArgumentParser(
        description=help_texts["main"], formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("infile", type=str, help=help_texts["infile"])

    parser.add_argument(
        "--outfile",
        "-o",
        type=str,
        default="out.txt",
        required=False,
        help=help_texts["outfile"],
    )

    args = parser.parse_args()

    bytes_list = file_as_bytes(args.infile)
    write_to_file_raw(args.outfile, bytes_list)
