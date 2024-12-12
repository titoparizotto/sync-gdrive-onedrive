import filecmp
import logging
import os
import shutil

from directories.directory import DirectoryBuilder
from logger import Logger


log = Logger(log_file="out.log", log_level=logging.DEBUG)
root = "G:\\Meu Drive\\fotos_videos"

directory_builder = DirectoryBuilder(root)
tree_structure = directory_builder.build()
directory_builder.sync_directories_files(tree_structure)

