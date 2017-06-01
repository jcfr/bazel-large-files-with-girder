#!/usr/bin/env python

"""This script allows to upload data file revisoned based on a canonical path.
"""

import girder_client
import json
import os
import sys
import textwrap

from datetime import datetime


def upload(server, api_key, folder_id, project_root, filepath):
    api_url = "%s/api/v1" % server
    filepath = os.path.abspath(filepath)
    versioned_filepath = os.path.relpath(filepath, project_root)
    item_name = "%s %s" % (os.path.basename(filepath), datetime.utcnow().isoformat())

    print("api_url ............: %s" % api_url)
    print("folder_id ..........: %s" % folder_id)
    print("filepath ...........: %s" % filepath)
    print("item_name ..........: %s" % item_name)
    print("project_root .......: %s" % folder_id)
    print("versioned_filepath .: %s" % versioned_filepath)

    gc = girder_client.GirderClient(apiUrl=api_url)
    gc.authenticate(apiKey=api_key)

    ref = json.dumps({'versionedFilePath': versioned_filepath})

    size = os.stat(filepath).st_size
    with open(filepath, 'rb') as fd:
        gc.uploadFile(folder_id, fd, name=item_name, size=size, parentType='folder', reference=ref) 


def display_usage():
    print(textwrap.dedent(
        """
        usage:

          %s /path/to/filename

        expected environment variables:

          GIRDER_SERVER .....: Url of the Girder server (e.g https://example.com)
          GIRDER_API_KEY ....: key used to authenticate to Girder server
          GIRDER_FOLDER_ID ..: Id of the folder to upload the file into
        """ % os.path.basename(__file__)))


def display_error(text):
    print("\nerror: %s" % text)
    display_usage()


def main():
    folder_id = os.environ.get('GIRDER_FOLDER_ID', '59307411739ba619e0eaa82e')
    if folder_id is None:
        display_error("GIRDER_FOLDER_ID environment variable is expected")
        sys.exit(1)

    server = os.environ.get(
        'GIRDER_SERVER', 'http://ec2-184-72-193-101.compute-1.amazonaws.com')
    if server is None:
        display_error("GIRDER_SERVER environment variable is expected")
        sys.exit(1)

    api_key = os.environ.get('GIRDER_API_KEY', None)
    if api_key is None:
        display_error("GIRDER_API_KEY environment variable is expected")
        sys.exit(1)

    if len(sys.argv) != 2:
        display_error("'/path/to/filename' is not specified")
        sys.exit(1)

    project_root = os.path.join(os.path.dirname(__file__), "..")
    filepath = sys.argv[1]

    upload(server, api_key, folder_id, project_root, filepath)


if __name__ == '__main__':
    main()
