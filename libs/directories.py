import logging
import shutil
import traceback
import os
from logger import Logger

log = Logger(log_file="out.log", log_level=logging.DEBUG)

class Directory:
    def __init__(self,source_dir:str, target_dir:str):
        self.source_dir = source_dir
        if target_dir == None :
            self.target_dir = self.get_target_dir()
        else:
            self.target_dir = target_dir
        self.subdirectory_list=[]
        self.filename_list=[]

        try:
            if os.path.exists(self.source_dir):
                for root,dirs,files in os.walk(self.source_dir):
                    log.info("root -> " + root)
                    for dir in dirs:
                        dir_path = os.path.join(root,dir)
                        log.info("dir_path -> " + dir_path)
                        directory = Directory(dir_path,dir_path.replace(self.source_dir,self.target_dir))
                        self.subdirectory_list.append(directory)
                    for file in files:
                        file_path = os.path.join(root,file)
                        log.info("file_path -> " + file_path)
                        self.filename_list.append(file_path)
            else:
                log.error("Diretório raiz informado não existe")
                return
        except Exception as e:
            log.error(f"Ocorreu um erro {e} ao ler o diretório {dir_path} / arquivo {file}"
                      f"\n{traceback.extract_stack()}")
            return


    def get_target_dir(self):
            source_target_list = get_source_target_list()
            for index, pair_path in enumerate(source_target_list):
                if self.source_dir in str(pair_path[0]):
                    return source_target_list[index][1]



def get_source_target_list():
    return [["G:\\Meu Drive\\geral", "C:\\Users\\titop\\OneDrive\\Documentos\\geral"],
            ["G:\\Meu Drive\\fotos_videos", "C:\\Users\\titop\\OneDrive\\Imagens"],
            ["G:\\Meu Drive\\backup", "C:\\Users\\titop\\OneDrive\\Documentos\\backup"],
            ["G:\\Meu Drive\\fotos_videos\\00_geral", "C:\\Users\\titop\\OneDrive\\Imagens\\00_geral"]
            ]

# def get_directories_list(directory_path):
    #     #dir_list=[]
    #
    #     # try:
    #     #     for rootin os.listdir(root):
    #     #         path = os.path.join(root, dir)
    #     #         dir_list.append(path)
    #     #         if os.path.isdir(path):
    #     #
    #     #             get_directories_list(path)
    #     #
    #     #     return dir_list
    #     #
    #     #
    #     #except Exception as e:
    #     #    log.error(f"Ocorreu um erro: {e}\n{traceback.format_exc()}")
    #
    #     files=[]
    #     for root,dirs,filenames in os.walk(directory_path):
    #         for filename in filenames:
    #             files.append(os.path.join(root,filename))
    #     return files
    #
    #
    #
    #
    #
    # def copy_to_target(dir_list):
    #     for source in dir_list:
    #         target = get_target_dir(source)
    #         log.info("Copiando diretório origem " + source + " para " + target)
    #
    #         try:
    #             if os.path.exists(target):
    #                 shutil.rmtree(target)
    #             shutil.copy2(source, target, ignore=None)
    #         except Exception as e:
    #             log.error(f"Erro ao copiar diretório\n{traceback.format_exc()}")






