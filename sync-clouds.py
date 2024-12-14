import logging
from directories.directory import DirectoryBuilder
from logger import Logger
from util import *

log = Logger(log_file="out.log", log_level=logging.DEBUG)
root = r"C:\Users\titop\OneDrive"

#directory_builder = DirectoryBuilder(root)
#tree_structure = directory_builder.build()
#sync_directories_files(tree_structure)
#get_list_files_updated(tree_structure)
#check_duplicated_files(root)
#delete_files_from_file()