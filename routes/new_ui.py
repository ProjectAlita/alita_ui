import json
import flask
from pathlib import Path

from pylon.core.tools import web, log
from tools import theme, VaultClient

from werkzeug.exceptions import NotFound


class Route:
    @web.route('/', defaults={'sub_path': ''}, endpoint='route_alita_ui')
    @web.route('/<path:sub_path>', endpoint='route_alita_ui_sub_path')
    def alita_ui_react(self, sub_path: str):
        base_path = self.alita_base_path
        try:
            return self.bp.send_static_file(base_path.joinpath(sub_path))
        except NotFound:
            log.info(
                "Route route_alita_ui_sub_path: %s; serving: %s",
                sub_path, base_path.joinpath('index.html')
            )
            #
            secrets = VaultClient().get_all_secrets()
            #
            vite_server_url = flask.url_for(
                "api.v1.alita_ui.ui_ci", _external=True
            ).replace("api/v1/alita_ui/ui_ci/", "api/v1")
            #
            vite_base_uri = flask.url_for("alita_ui.route_alita_ui").rstrip("/")
            vite_public_project_id = int(secrets.get("ai_project_id", "1"))
            vite_socket_path = flask.url_for("theme.socketio")
            #
            alita_ui_config_data = {
                "vite_server_url": vite_server_url,
                "vite_base_uri": vite_base_uri,
                "vite_public_project_id": vite_public_project_id,
                "vite_socket_path": vite_socket_path,
                "vite_socket_server": self.descriptor.config.get('vite_socket_server', '/')
            }
            #
            additional_config_keys = ["vite_gaid"]
            #
            for key in additional_config_keys:
                if key in secrets:
                    alita_ui_config_data[key] = secrets.get(key)
                elif key in self.descriptor.config:
                    alita_ui_config_data[key] = self.descriptor.config.get(key)
            #
            alita_ui_config = json.dumps(alita_ui_config_data)
            #
            idx_path = Path(self.bp.static_folder).joinpath(base_path, "index.html")
            #
            with open(idx_path, "r", encoding="utf-8") as idx_file:
                idx_data = idx_file.read()
            #
            idx_data = idx_data.replace(
                'src="./assets', f'src="{vite_base_uri}/assets'
            )
            idx_data = idx_data.replace(
                '<!-- alita_ui_config -->',
                f"<script>window.alita_ui_config = JSON.parse('{alita_ui_config}');</script>"
            )
            #
            response = flask.make_response(idx_data, 200)
            return response
