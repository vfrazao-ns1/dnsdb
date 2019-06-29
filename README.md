# DNSDB

## Overview

DNSDB is a small proof of concept of keeping binary data stored and transmitted via DNS. 

Per RFC 1035 arbirtary binary data can be encoded in character strings (such as the rdata of TXT records) using a special annotation:

```text
\DDD            where each D is a digit is the octet corresponding to
                the decimal number described by DDD.  The resulting
                octet is assumed to be text and is not checked for
                special meaning.
```

So for this experiment I created a Python script that reads a file, uses the NS1 api to store it in this special encoding in the rdata of a txt record, and another script to take the DNS rdata from a DNS response and re-piece it into the original file -- therefore providing a method to upload and download files from authoritative DNS servers.

## Usage

1. Upload file to authoritative DNS provider

To upload the fie run the `file_to_ns1.py` script. To run the script you need to provide it with a filepath to the file to be uploaded, an NS1 API key, and the name of the DNS zone that will house the data records.

Example:

```shell
$ py ./file_to_ns1.py pic.jpg -k $API_KEY --zone files.frazao.ca
Success __pic.jpg.files.frazao.ca
```

2. Download file from DNS server

The records where the file are stored must now be queried, and the binary DNS rdata dumped to a new file on disk. The binary DNS rdata could be obtained by doing packet capture. I have created a small DNS client [not-dig](https://github.com/vfrazao-ns1/dns-server-implementation) that can write the DNS rdata to a binary file.

Example:

```shell
$ ls
README.md  __pycache__  file_to_ns1.py  file_to_txt.py  image.png  packet_to_file.py  pic.jpg
$ not-dig __pic.jpg.files.frazao.ca. txt --server 198.51.44.1 --bin > new.jpg
$ ls
README.md  __pycache__  file_to_ns1.py  file_to_txt.py  image.png  new.jpg  packet_to_file.py  pic.jpg
```

3. Reconstruct the binary file

Lastly run the `packet_to_file.py` on your pcap of the DNS rdata to reconstruct the original file.

```shell
$ py ./packet_to_file.py new.jpg
$
```
