import requests
from datetime import datetime

from flask import g, request, jsonify
from pylon.core.tools import log

from tools import api_tools, auth, config as c


class AdminAPI(api_tools.APIModeHandler):
    # @auth.decorators.check_api({
    #     "permissions": ["models.prompts.ui.detail"],
    #     "recommended_roles": {
    #         c.ADMINISTRATION_MODE: {"admin": True, "editor": False, "viewer": False},
    #     }})
    def get(self, **kwargs):
        return jsonify(self.module.build_meta)

    @auth.decorators.check_api({
        "permissions": ["models.prompts.ui.update"],
        "recommended_roles": {
            c.ADMINISTRATION_MODE: {"admin": True, "editor": False, "viewer": False},
        }})
    def post(self, **kwargs):
        release = request.json.get('release', self.module.default_release)
        #
        self.module.update_ui(release)
        #
        self.module.build_meta['release'] = release
        self.module.build_meta['updated_at'] = datetime.now()
        self.module.build_meta['commit_sha'] = request.json.get('commit_sha', '')
        self.module.build_meta['commit_ref'] = request.json.get('commit_ref', '')
        #
        return jsonify(self.module.build_meta)


class API(api_tools.APIBase):
    url_params = ['', '<string:mode>']
    mode_handlers = {
        c.ADMINISTRATION_MODE: AdminAPI,
    }
