import os
import logging

class Logger(object):
    def __init__(self, file_name):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # create a file handler
    	log_file_name = os.path.join(os.path.dirname(__file__), file_name)
        handler = logging.FileHandler(log_file_name)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)

        # create a stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(handler)
        self.logger.addHandler(stream_handler)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)
