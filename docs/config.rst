Configuration
#############

Configuration keys
==================

================================ ==============================================
COMPASS_PATH                     Path to the compass script. If not specified  
                                 it is assumed that compass is available in the
                                 PATH.

COMPASS_CONFIGS                  Path to config.rb files. If not specified, the     
                                 whole project directory is scanned.                

COMPASS_REQUESTCHECK_DEBUG_ONLY  Check the configs with each request only in
                                 debug mode. Default: True

COMPASS_DEBUG_ONLY               Disable the extension completely if not in
                                 debug mode.

COMPASS_SKIP_MTIME_CHECK         Don't check the mtimes of the source and
                                 target folder of each compass project
                                 but instead just execute compass.
                                 Default: False
================================ ==============================================

