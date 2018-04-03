import logging

class Logger():

    def __init__(self, name):
        self.name = name
        self.logger = self.getLogger()

    def getLogger(self):
        disable_logger = [ 'pika' ]

        for logger in disable_logger:
            logging.getLogger(logger).setLevel(logging.CRITICAL)

        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)