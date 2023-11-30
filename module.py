from pathlib import Path

from pylon.core.tools import module, log

from tools import theme
from werkzeug.exceptions import NotFound


class Module(module.ModuleModel):
    def __init__(self, context, descriptor):
        self.context = context
        self.descriptor = descriptor
        self.bp = None
        self.alita_base_path = Path('ui', 'dist')
        self.build_meta = {
            'release': None,
            'updated_at': None,
            'commit_sha': '',
            'commit_ref': '',
        }
        self.release_url_template = 'https://github.com/ProjectAlita/AlitaUI/releases/download/{release}/dist.zip'

    def init(self):
        log.info('Init')
        self.bp = self.descriptor.init_all()
        # bp = self.descriptor.make_blueprint(
        #     url_prefix='alita_ui',
        # )
        # bp.add_url_rule('/', 'route_alita_ui', self.alita_ui_react)
        # theme.bp.add_url_rule('/alita_ui/', 'route_alita_ui', self.alita_ui_react)
        # theme.bp.add_url_rule('/alita_ui/<path:sub_path>', 'route_alita_ui_sub_path', self.alita_ui_react)

    def deinit(self):
        log.info('De-initializing')

    # def alita_ui_react(self, sub_path: str):
    #     base_path = Path('ui', 'dist')
    #     try:
    #         return self.bp.send_static_file(base_path.joinpath(sub_path))
    #     except NotFound:
    #         log.info("Route route_alita_ui_sub_path: %s; serving: %s", sub_path, base_path.joinpath('index.html'))
    #         return self.bp.send_static_file(base_path.joinpath('index.html'))
