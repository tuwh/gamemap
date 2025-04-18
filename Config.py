# PROJECT_ROOT=None
BLENDER_ADDON_PATH=None
BLENDER_EXE_PATH=None
IS_EXTENSION=False
TEST_RELEASE_DIR=""
DEFAULT_RELEASE_DIR=""

import os
from configparser import ConfigParser

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

CONFIG_FILEPATH = os.path.join(PROJECT_ROOT, 'config.ini')

configParser = ConfigParser()
configParser.read(CONFIG_FILEPATH, encoding='utf-8')
if configParser.has_option('blender', 'exe_path'):
    BLENDER_EXE_PATH = configParser.get('blender', 'exe_path')
if configParser.has_option('blender', 'addon_path') and configParser.get('blender', 'addon_path'):
    BLENDER_ADDON_PATH = configParser.get('blender', 'addon_path')

# The default release dir. Must not within the current workspace
# 插件发布的默认目录，不能在当前工作空间内
DEFAULT_RELEASE_DIR = os.path.join(PROJECT_ROOT, "../addon_release/")

# The default test release dir. Must not within the current workspace
# 测试插件发布的默认目录，不能在当前工作空间内
TEST_RELEASE_DIR = os.path.join(PROJECT_ROOT, "../addon_test/")
