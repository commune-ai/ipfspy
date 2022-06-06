# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_httpapi.ipynb (unless otherwise specified).

__all__ = ['add_items', 'ls_items', 'get_items', 'cat_items', 'dag_export', 'dag_get', 'dag_stat', 'pin_add', 'pin_ls',
           'pin_rm', 'rspin_add', 'rspin_ls', 'rspin_rm', 'rpin_add', 'rpin_ls', 'rpin_rm', 'block_get', 'block_put',
           'block_rm', 'block_stat', 'mfs_chcid', 'mfs_cp', 'mfs_flush', 'mfs_ls', 'mfs_mkdir', 'mfs_mv', 'mfs_read',
           'mfs_rm', 'mfs_stat', 'mfs_write', 'get_peers', 'dht_find_peer', 'dht_value_provider', 'dht_get_value']

# Cell
#hide
from typing import Union, List

import requests
import json
from fastcore.all import *
import pandas as pd
import dag_cbor

from .utils import *

from ipfshttpclient.multipart import stream_files, stream_directory

# Cell
def add_items(
    coreurl:str, # Core URL to use
    filepath:Union[str, List[str]], # Path to the file/directory to be added to IPFS
    directory:bool=False, # Is filepath a directory
    wrap_with_directory:str='false', # True if path is a directory
    recursive:str='false', # Add directory paths recursively
    chunker:str='size-262144', # Chunking algorithm, size-[bytes], rabin-[min]-[avg]-[max] or buzhash
    pin:str='true', # Pin this object when adding
    hash_:str='sha2-256', # Hash function to use. Implies CIDv1 if not sha2-256
    progress:str='true', # Stream progress data
    silent:str='false', # Write no output
    cid_version:int=0, # CID version
    **kwargs,
):
    "add file/directory to ipfs"

    params = {}
    params['wrap-with-directory'] = wrap_with_directory
    params['chunker'] = chunker
    params['pin'] = pin
    params['hash'] = hash_
    params['progress'] = progress
    params['silent'] = silent
    params['cid-version'] = cid_version
    params.update(kwargs)

    if not directory:
        chunk_size = int(chunker.split('-')[1])
        data, headers = stream_files(filepath, chunk_size=chunk_size)

    else:
        chunk_size = int(chunker.split('-')[1])
        data, headers = stream_directory(filepath, chunk_size=chunk_size)

    response = requests.post(f'{coreurl}/add',
                             params=params,
                             data=data,
                             headers=headers)
    try:
        print("Added", filepath, "to IPFS - ","Response", response.status_code)
        return response, parse_response(response)

    except:
        print(response.status_code)
        return response, ""


def ls_items(
    coreurl:str,
    ipfspath:str, # The path to the IPFS object(s) to list links from
    resolve_type:str='true', # Resolve linked objects to find out their types
    size:str='true', # Resolve linked objects to find out their file size
    **kwargs,
):
    'List directory contents for Unix filesystem objects'

    params = {}
    params['arg'] = ipfspath
    params['resolve-type'] = resolve_type
    params['size'] = size
    params.update(kwargs)

    return requests.post(f'{coreurl}/ls', params=params)


# doesnt save the file in the output folder given
def get_items(
    coreurl:str,
    cid:str, # The path to the IPFS object(s) to be outputted
    output:str='', # The path where the output should be stored
    **kwargs
):
    'Download IPFS objects'

    params = {}
    params['arg'] = cid
    params['output'] = output
    params.update(kwargs)

    response = requests.post(f'{coreurl}/get', params=params)

    return response


def cat_items(
    coreurl:str,
    cid:str, # The path to the IPFS object(s) to be outputted
    **kwargs
):
    'Show IPFS object data'

    params = {}
    params['arg'] = cid
    params.update(kwargs)

    return requests.post(f'{coreurl}/cat', params=params)

# Cell
def dag_export(
    coreurl:str,
    path:str,
    **kwargs,
):
    'Streams the selected DAG as a .car stream on stdout.'

    params = {}
    params['arg'] = path
    params.update(kwargs)

    return requests.post(f'{coreurl}/dag/export', params=params)


def dag_get(
    coreurl:str,
    path:str,
    output_codec:str='dag-cbor',
):
    'Get a DAG node from IPFS.'

    params = {}
    params['arg'] = path
    params['output-codec'] = output_codec

    return requests.post(f'{coreurl}/dag/get', params=params)


def dag_stat(
    coreurl:str,
    path:str,
    **kwargs,
):
    'Gets stats for a DAG.'

    params = {}
    params['arg'] = path
    params.update(kwargs)

    return requests.post(f'{coreurl}/dag/stat', params=params)

# Cell
def pin_add(
    coreurl:str,
    ipfspath:str, # Path to IPFS object(s) to be pinned
    recursive:str='true', # Recursively pin the object linked to by the specified object(s)
):
    'Pin objects to local storage.'

    params = {}
    params['arg'] = ipfspath
    params['recursive'] = recursive

    return requests.post(f'{coreurl}/pin/add', params=params)


def pin_ls(
    coreurl:str,
    type_:str='all', # The type of pinned keys to list. Can be "direct", "indirect", "recursive", or "all"
    **kwargs,
):
    'List objects pinned to local storage.'

    params = {}
    params['type'] = type_
    params.update(kwargs)

    return requests.post(f'{coreurl}/pin/ls', params=params)


def pin_rm(
    coreurl:str,
    ipfspath:str, # Path to object(s) to be unpinned
    recursive:str='true', #  Recursively unpin the object linked to by the specified object(s)
    **kwargs,
):
    'List objects pinned to local storage.'

    params = {}
    params['arg'] = ipfspath
    params['recursive'] = recursive
    params.update(kwargs)

    return requests.post(f'{coreurl}/pin/rm', params=params)

# Cell
def rspin_add(
    coreurl:str,
    service_name:str, # Name of the remote pinning service to use
    service_edpt:str, # Service endpoint
    service_key:str, # Service key
):
    'Pin object to remote pinning service.'

    params = {}
    params['arg'] = [service_name, service_edpt, service_key]

    return requests.post(f'{coreurl}/pin/remote/service/add', params=params)


def rspin_ls(
    coreurl:str,
    **kwargs
):
    'List remote pinning services.'

    params = {}
    params.update(kwargs)

    return requests.post(f'{coreurl}/pin/remote/service/ls', params=params)


def rspin_rm(
    coreurl:str,
    service_name:str, # Name of pinning service to remove
):
    'Remove remote pinning service.'

    params = {}
    params['arg'] = service_name

    return requests.post(f'{coreurl}/pin/remote/service/rm', params=params)


# Cell
def rpin_add(
    coreurl,
    ipfspath:str, #  Path to IPFS object(s) to be pinned
    service:str, # Name of the remote pinning service to use
    background:str='false', # Add to the queue on the remote service and return immediately (does not wait for pinned status)
    **kwargs,
):
    'Pin object to remote pinning service.'

    params = {}
    params['arg'] = ipfspath
    params['service'] = service
    params['background'] = background
    params.update(kwargs)

    return requests.post(f'{coreurl}/pin/remote/add', params=params)


def rpin_ls(
    coreurl:str,
    service:str, # Name of the remote pinning service to use
    **kwargs,
):
    'List objects pinned to remote pinning service.'

    params = {}
    params['service'] = service
    params.update(kwargs)

    return requests.post(f'{coreurl}/pin/remote/ls', params=params)


def rpin_rm(
    coreurl:str,
    service:str, # Name of the remote pinning service to use
    **kwargs,
):
    'Remove pins from remote pinning service.'

    params = {}
    params['service'] = service
    params.update(kwargs)

    return requests.post(f'{coreurl}/pin/remote/rm', params=params)


# Cell
def block_get(
    coreurl,
    arg:str, # The base58 multihash of an existing block to get

):
    'Get a raw IPFS block.'

    params = {}
    params['arg'] = arg

    return requests.post(f'{coreurl}/block/get', params=params)


def block_put(
    coreurl,
    filepath:str, # Path to file
    mhtype:str='sha2-256', # multihash hash function.
    mhlen:int=-1, # Multihash hash length
    pin:str='false', #  pin added blocks recursively
    **kwargs,
):
    'Store input as an IPFS block.'

    params = {}
    params['mhtype'] = mhtype
    params['mhlen'] = mhlen
    params['pin'] = pin
    params.update(kwargs)

    return requests.post(f'{coreurl}/block/put', params=params, files={'files':open(filepath, 'rb')})


def block_rm(
    coreurl,
    arg:str, # Bash58 encoded multihash of block(s) to remove
    force:str='false', # Ignore nonexistent blocks.
    quiet:str='false', # Write minimal output.
):
    'Remove IPFS block(s).'

    params = {}
    params['arg'] = arg
    params['force'] = force
    params['quiet'] = quiet

    return requests.post(f'{coreurl}/block/rm', params=params)


def block_stat(
    coreurl,
    arg:str, # Bash58 encoded multihash of block(s) to remove

):
    'Print information of a raw IPFS block.'

    params = {}
    params['arg'] = arg

    return requests.post(f'{coreurl}/block/stat', params=params)

# Cell
def mfs_chcid(
    coreurl:str,
    path:str='/', # Path to change
    cid_version:int=0, # Cid version to use
    **kwargs,
):

    'Change the CID version or hash function of the root node of a given path.'

    params = {}
    params['arg'] = path
    params['cid-version'] = cid_version
    params.update(kwargs)

    return response.post(f"{coreurl}/files/chcid", params=params)


def mfs_cp(
    coreurl:str,
    source_path:str, # Source IPFS or MFS path to copy
    dest_path:str, # Destination within MFS
    **kwargs
):

    'Add references to IPFS files and directories in MFS (or copy within MFS).'

    params = {}
    params['arg'] = [source_path, dest_path]
    params.update(kwargs)

    return requests.post(f'{coreurl}/files/cp', params=params)


def mfs_flush(
    coreurl:str,
    path:str='/', # Path to flush
):
    "Flush a given path's data to disk"

    params['arg'] = path

    return requests.post(f'{coreurl}/files/flush',params=params)


def mfs_ls(
    coreurl:str,
    path:str='/', # Path to show listing for
    **kwargs
):
    "List directories in the local mutable namespace."

    params = {}
    params['arg'] = path
    params.update(kwargs)

    return requests.post(f'{coreurl}/files/ls', params=params)


def mfs_mkdir(
    coreurl:str,
    path:str, # Path to dir to make
    **kwargs,
):
    "Make directories."

    params = {}
    params['arg'] = path
    params.update(kwargs)

    return requests.post(f"{coreurl}/files/mkdir", params=params)


def mfs_mv(
    coreurl:str,
    source_path:str, # Source file to move
    dest_path:str,  # Destination path for file to be moved to
):
    "Move files."

    params = {}
    params['arg'] = [source_path, dest_path]

    return requests.post(f"{coreurl}/files/mv", params=params)


def mfs_read(
    coreurl:str,
    path, # Path to file to be read
    **kwargs,
):
    "Read a file in a given MFS."

    params = {}
    params['arg'] = path
    params.update(kwargs)

    return requests.post(f"{coreurl}/files/read",params=params)


def mfs_rm(
    coreurl:str,
    path, # File to remove
    **kwargs,
):
    "Read a file in a given MFS."

    params = {}
    params['arg'] = path
    params.update(kwargs)

    return requests.post(f"{coreurl}/files/rm", params=params)


def mfs_stat(
    coreurl:str,
    path, # Path to node to stat
    **kwargs,
):
    "Display file status."

    params = {}
    params['arg'] = path
    params.update(kwargs)

    return requests.post(f"{coreurl}/files/stat", params=params)


def mfs_write(
    coreurl:str,
    path, # Path to write to
    filepath, # File to add
    **kwargs,
):
    "Display file status."

    files = {
        'file': open(filepath, 'rb')
    }

    params = {}
    params['arg'] = path
    params.update(kwargs)

    return requests.post(f"{coreurl}/files/write",params=params, files=files)

# Cell
def get_peers(
    coreurl,
    verbose='true', # Display all extra information
    streams='false', # Also list information about open streams for each peer
    latency='false', # Also list information about latency to each peer
    direction='false' # Also list information about the direction of connection
):
    'List peers with open connections.'

    params = {}
    params['verbose'] = verbose
    params['streams'] = streams
    params['latency'] = latency
    params['direction'] = direction

    return requests.post(f"{coreurl}/swarm/peers", params=params).json()

# Cell
def dht_find_peer(
    coreurl:str,
    key:str,  # The ID of the peer to search for
    verbose:str='true', #Print extra information
):
    'Find the multiaddresses associated with a Peer ID.'

    params = {}
    params['arg'] = key
    params['verbose'] = verbose

    return requests.post(f'{coreurl}/dht/findpeer', params=params)

def dht_value_provider(
    coreurl:str,
    key:str,  # The key to find providers for
    verbose:str='true', #Print extra information
):
    'Find peers that can provide a specific value, given a key.'

    params = {}
    params['arg'] = key
    params['verbose'] = verbose

    return requests.post(f'{coreurl}/dht/findpeer', params=params)

def dht_get_value(
    coreurl:str,
    key:str,  # The key to find a value for
    verbose:str='true', #Print extra information
):
    'Given a key, query the routing system for its best value.'

    params = {}
    params['arg'] = key
    params['verbose'] = verbose

    return requests.post(f'{coreurl}/dht/get', params=params).json()