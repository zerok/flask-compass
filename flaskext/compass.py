import os, os.path, subprocess, re, time, warnings, datetime
from flask import request


CONFIG_LINE_RE = re.compile(ur'^\s*?(\S+)\s*?=\s*(.*)\s*$')


class Compass(object):
    """
    This is a very basic extension for Flask that searches for compass projects
    within an application's directory and compiles it.

    By default this is only done when the application is in debug mode since 
    with each request the extension has to check all relevant files to see if 
    there even *is* something to compile.
    """

    def __init__(self, app=None):
        self.app = app
        self.configs = {}
        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        self.app = app
        self.log = app.logger.getChild('compass')
        self.log.debug("Initializing compass integration")
        self.compass_path = self.app.config.get('COMPASS_PATH', 'compass')
        self.config_files = self.app.config.get('COMPASS_CONFIGS', None)
        self.debug_only= self.app.config.get('COMPASS_REQUESTCHECK_DEBUG_ONLY', True)
        self.compile()
        if not self.debug_only or self.app.debug:
            self.app.after_request(self.compile)

    def compile(self, response=None):
        """
        Main entry point that compiles all the specified or found compass
        projects.
        """
        if response is not None and request is not None:
            # When used as response processor, only run if we are requesting anything
            # but a static resource.
            if request.endpoint in [None, "static"]:
                return response
        self._check_configs()
        for cfgfile, cfg in self.configs.iteritems():
            cfg.parse()
            if cfg.changes_found():
                self.log.debug("Changes found for " + cfg.path + ". Compiling...")
                cfg.compile(self)
        return response

    def _check_configs(self):
        configs = set(self._find_configs())
        known_configs = set(self.configs.keys())
        new_configs = configs - known_configs
        for cfg in (known_configs - configs):
            self.log.debug("Compass configuration has been removed: " + cfg)
            del self.configs[cfg]
        for cfg in new_configs:
            self.log.debug("Found new compass configuration: " + cfg)
            self.configs[cfg] = CompassConfig(cfg)

    def _find_configs(self):
        if self.config_files is not None:
            return self.config_files

        # Walk the whole project tree and look for "config.rb" files
        result = []
        for path, dirs, files in os.walk(self.app.root_path):
            if "config.rb" in files:
                result.append(os.path.join(path, "config.rb"))
        return result


class CompassConfig(object):
    def __init__(self, path):
        self.path = path
        self.base_dir = os.path.dirname(path)
        self.last_parsed = None
        self.src = None
        self.dest = None

    def parse(self, replace=False):
        """
        Parse the given compass config file
        """
        if self.last_parsed is not None \
                and self.last_parsed > os.path.getmtime(self.path) \
                and not replace:
            return
        self.last_parsed = time.time()
        with open(self.path, 'r') as fp:
            for line in fp:
                mo = CONFIG_LINE_RE.match(line.rstrip())
                if mo:
                    if mo.group(1) == 'sass_dir':
                        self.src = os.path.join(self.base_dir, mo.group(2)[1:-1])
                    elif mo.group(1) == 'css_dir':
                        self.dest = os.path.join(self.base_dir, mo.group(2)[1:-1])

    def changes_found(self):
        if self.dest is None:
            warnings.warn("dest directory not found!")
        if self.src is None:
            warnings.warn("src directory not found!")
        if self.src is None or self.dest is None:
            return False
        return os.path.getmtime(self.src) > os.path.getmtime(self.dest)

    def compile(self, compass):
        subprocess.call([compass.compass_path, 'compile'], cwd=self.base_dir)
        os.utime(self.dest, None)

