import logging

class Logger:
    def __init__(self, log_file: str = "app.log", log_level: int = logging.INFO):
        """
        Inicializa o Logger.

        :param log_file: Nome do arquivo de log.
        :param log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Evita duplicação de handlers
        if not self.logger.handlers:
            # Adicionar manipulador de arquivo
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

            # Adicionar manipulador de console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)