import logging 
class LOG(object):
    def __init__(self,name):
        self.logger = logging.getLogger(name) 
        self.logger.setLevel(logging.DEBUG) 
        fh = logging.FileHandler("/var/log/crawler/%s.log" %name) 
        fh.setLevel(logging.DEBUG) 
        formatter = logging.Formatter('%(levelname)s - %(message)s') 
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    def get_logger(self):
        return self.logger

if __name__ == "__main__":
    mylog = LOG("my").get_logger()
    mylog.debug("hello")
