"""
Takes a file as input and uploads it as an NS1 record
"""
import sys
import file_to_txt
import argparse
from typing import List
import requests


RDATA_MAX_LEN = 65535 - (65535 // 255)  # RFC 1035
STRING_LIM = 63 # low limit due to unfortunate bug in NS1
NS1_API_URL = "https://api.nsone.net/v1"


def bytes_list_to_ns1(bytes_list: List[str], root_zone: str, fname: str) -> dict:
    bytes_answers = chunk_bytes(bytes_list)
    num_records = len(bytes_list) // RDATA_MAX_LEN + 1
    domain = f"__{fname}.{root_zone}"
    record_body = {
        "zone": root_zone,
        "domain": domain,
        "ttl": 30,
        "type": "TXT",
        "answers": [
            {
                "answer": ["".join(a) for a in chunk_bytes(ans, STRING_LIM)]
            } for ans in bytes_answers
        ],
    }
    return record_body


def upload_file_to_ns1(request_body: dict, apikey: str) -> None:
    sess = requests.Session()
    sess.headers.update({"X-NSONE-Key": apikey})
    
    zone = request_body["zone"]
    domain = request_body["domain"]
    endpoint = f"{NS1_API_URL}/zones/{zone}/{domain}/TXT"
    get_response = sess.get(endpoint)

    if get_response.status_code == 404:
        response = sess.put(endpoint, json=request_body)
    elif get_response.status_code == 200:
        # sess.delete(endpoint)
        response = sess.post(endpoint, json=request_body)
    else:
        print(f"Error interacting with API: {get_response.text}", file=sys.stderr)
        return None
    if response.status_code != 200:
        print(f"Error uploading file: {response.text}", file=sys.stderr)
    else:
        print("Success", domain)


def chunk_bytes(bytes_list: List[str], n: int = RDATA_MAX_LEN) -> List[List[str]]:
    """
    Returns n size chunks of a list. 
    """
    chunks = []
    i = 0
    while i < len(bytes_list):
        if i + n < len(bytes_list):
            offset = i + n
        else:
            offset = len(bytes_list)
        chunks.append(bytes_list[i:offset])
        i += n
    return chunks


if __name__ == "__main__":
    help_texts = {
        "main": __doc__,
        "apikey": "NS1 API key with appropriate permissions",
        "infile": "Name of file to read from",
        "zone": "Zone designated for file storage",
        "outfile": "Name of record to write output",
    }
    parser = argparse.ArgumentParser(
        description=help_texts["main"], formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("infile", type=str, help=help_texts["infile"])
    parser.add_argument(
        "--apikey", "-k", type=str, required=True, help=help_texts["apikey"]
    )
    parser.add_argument(
        "--zone", "-z", type=str, required=True, help=help_texts["zone"]
    )
    parser.add_argument(
        "--outfile",
        "-o",
        type=str,
        required=False,
        help=help_texts["outfile"],
    )

    args = parser.parse_args()

    outfile = args.infile if args.outfile is None else args.outfile

    bytes_list = file_to_txt.file_as_bytes(args.infile)
    record_body = bytes_list_to_ns1(bytes_list, args.zone, outfile)
    upload_file_to_ns1(record_body, args.apikey)
