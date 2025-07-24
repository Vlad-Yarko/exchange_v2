import logging
import os


current_dir = os.path.dirname(__file__)
backend_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
log_dir = os.path.join(backend_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, 'logs.log')


class Logger:
    def __init__(self):
        self.filename = log_file_path
        self.level = logging.DEBUG
        self.filemode = 'a'
        self.format = '%(levelname)s---%(asctime)s---%(message)s---%(name)s'

        with open(self.filename, 'w'):
            pass

    def set_logger(self) -> None:
        logging.basicConfig(
            level=self.level,
            filename=self.filename,
            filemode=self.filemode,
            format=self.format
        )
        self.logger = logging

    # def make_router_logger(self, t: str, name: str):
    #     router_logger = logging.getLogger(f"{t}-{name}")
    #     router_logger.setLevel(self.level)
    #     file_handler = logging.FileHandler(self.filename, mode=self.filemode)
    #     file_handler.setFormatter(logging.Formatter(self.format))
    #     router_logger.addHandler(file_handler)
    #     return router_logger
    
    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)


logger = Logger()
logger.set_logger()
