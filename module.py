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
        self.release_url_template = self.descriptor.config.get(
            "release_url_template",
            'https://github.com/ProjectAlita/AlitaUI/releases/download/{release}/dist.zip',
        )
        self.default_release = self.descriptor.config.get("default_release", "latest")
        self.release_verify = self.descriptor.config.get("release_verify", True)

    def init(self):
        log.info('Init')
        self.bp = self.descriptor.init_all()
        #
        # Download UI if needed for first time
        #
        idx_test_path = Path(self.bp.static_folder).joinpath(self.alita_base_path, "index.html")
        if not idx_test_path.exists():
            log.info("Downloading and installing initial release: %s", self.default_release)
            self.update_ui()
        #
        # Register a mode (for admin UI switch-back)
        #
        theme.register_mode(
            "alita", "Alita",
            public=True,
        )
        theme.register_mode_landing(
            mode="alita",
            kind="route",
            route="alita_ui.route_alita_ui",
        )

    def deinit(self):
        log.info('De-initializing')
        self.descriptor.deinit_all()
