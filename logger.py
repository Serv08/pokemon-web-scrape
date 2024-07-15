import logging


class Logger:
    def __init__(self):
        self.logger = self.get_logger()


    def get_logger(self):
        '''Logs'''
        # Create a custom logger
        logger = logging.getLogger()
        
        # Check if logger has handlers to avoid duplicate logs
        if not logger.hasHandlers():
            # Set the logging level
            logger.setLevel(logging.DEBUG)
            
            # Create handlers
            c_handler = logging.StreamHandler()
            # f_handler = logging.FileHandler(r'C:\Users\SERVIN\Desktop\Important local files\Data Analyst\data\scraper.log')
            f_handler = logging.FileHandler('scraper.log')
            c_handler.setLevel(logging.DEBUG)
            f_handler.setLevel(logging.DEBUG)
            
            # Create formatters and add it to handlers
            c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)
            
            # Add handlers to the logger
            logger.addHandler(c_handler)
            logger.addHandler(f_handler)
        
        return logger
    