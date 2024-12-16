from util import *
ConfigManager.initialize()
log = Logger(log_file= ConfigManager.get("app.logger.log_file"), log_level=ConfigManager.get("app.logger.log_level"))

root = ConfigManager.get("app.root")

#directory_builder = DirectoryBuilder(root)
#tree_structure = directory_builder.build()
#sync_directories_files(tree_structure)
#get_list_files_updated(tree_structure)
check_duplicated_files(root)
#delete_files_from_file()