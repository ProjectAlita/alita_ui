import flask
from pathlib import Path

from pylon.core.tools import web, log
from tools import theme

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
            log.info(
                "[----- DEBUG -----] %s",
                flask.url_for("api.v1", _external=True),
            )
            #
            idx_path = Path(self.bp.static_folder).joinpath(base_path, "index.html")
            #
            with open(idx_path, "r", encoding="utf-8") as idx_file:
                idx_data = idx_file.read()
            #
            idx_data = idx_data.replace('<!-- alita_ui_config -->', '')
            #
            vite_base_uri = flask.url_for("alita_ui.route_alita_ui").rstrip("/")
            idx_data = idx_data.replace('src="./assets', f'src="{vite_base_uri}/assets')
            #
            response = flask.make_response(idx_data, 200)
            return response
