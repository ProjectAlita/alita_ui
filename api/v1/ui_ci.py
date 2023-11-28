import requests
import zipfile
from io import BytesIO
from datetime import datetime
from pathlib import Path

from flask import g, request, jsonify
from pylon.core.tools import log

from tools import api_tools, auth, config as c


def download_and_unzip(url: str, destination_path: str | Path) -> None:
    response = requests.get(url)
    if response.ok:
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(destination_path)
        log.info(f"Zip file downloaded and extracted to {destination_path}")
    else:
        log.error(f"Failed to download the zip file. Status code: {response.status_code}")


class API(api_tools.APIBase):
    url_params = ['']

    def get(self):
        return jsonify(self.module.build_meta)

    def post(self):
        release = request.json.get('release', 'latest')
        d = dict()
        download_and_unzip(
            self.module.release_url_template.format(release=release),
            Path(self.module.bp.static_folder).joinpath(self.module.alita_base_path)
        )
        self.module.build_meta['release'] = release
        self.module.build_meta['updated_at'] = datetime.now()
        return jsonify(d)
