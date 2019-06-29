import argparse

def rdata_to_file(filepath:str):
    with open(filepath, 'rb') as rdata_file:
        rdata = rdata_file.read()
        file_data = []
        len_index = rdata[0] 
        for byte in rdata[1:]:
            if len_index:
                file_data.append(byte)
                len_index -= 1
            else:
                len_index = byte
    with open(filepath, "wb") as data_file:
        data_file.write(bytes(file_data))


if __name__ == "__main__":
    help_texts = {
        "main": __doc__,
        "infile": "Name of file to read from",
    }
    parser = argparse.ArgumentParser(
        description=help_texts["main"], formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("infile", type=str, help=help_texts["infile"])
    args = parser.parse_args()
    rdata_to_file(args.infile)
