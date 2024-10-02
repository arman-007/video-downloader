import logging

# Custom logger for yt-dlp
class MyLogger:
    def __init__(self):
        # Setting up the logger
        self.logger = logging.getLogger('yt-dlp')
        self.logger.setLevel(logging.DEBUG)  # Adjust this level as necessary

        # Add a console handler to log to the console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)  # Adjust this level as necessary

        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(ch)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
