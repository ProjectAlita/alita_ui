#!/usr/bin/python3
# coding=utf-8
# pylint: disable=E1101

""" RPC """

import os
import zipfile
from pathlib import Path
from io import BytesIO

from pylon.core.tools import web, log  # pylint: disable=E0401
import requests  # pylint: disable=E0401


class RPC:  # pylint: disable=R0903
    """ RPC pseudo-class """

    @web.rpc()
    def update_ui(self, release=None):
        """ Download and install UI react app code """
        # Compute URL and path
        if release is None:
            release = self.default_release
        #
        url = self.release_url_template.format(release=release)
        destination_path = Path(self.bp.static_folder).joinpath(self.alita_base_path)
        # Download, clean-up, extract
        response = requests.get(url, verify=self.release_verify)
        #
        if response.ok:
            with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
                # Clean-up here: at least ZIP was downloaded and opened OK
                for root, dirs, files in os.walk(destination_path, topdown=False):
                    for name in files:
                        if name in [".gitkeep"]:
                            continue
                        try:
                            os.remove(os.path.join(root, name))
                        except:  # pylint: disable=W0702
                            log.exception("Failed to remove file: %s, skipping", name)
                    for name in dirs:
                        try:
                            os.rmdir(os.path.join(root, name))
                        except:  # pylint: disable=W0702
                            log.exception("Failed to remove dir: %s, skipping", name)
                # Extract new files
                zip_file.extractall(destination_path)
            #
            log.info(f"Zip file downloaded and extracted to {destination_path}")
        else:
            log.error(f"Failed to download the zip file. Status code: {response.status_code}")
