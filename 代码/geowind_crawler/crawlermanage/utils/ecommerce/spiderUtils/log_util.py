import logging
import logging.config



def get_logger():
    logging.config.fileConfig("../logger.conf")

    logger = logging.getLogger("root")

    return logger

def info(message):
    get_logger().info(message)
def error(message):
    get_logger().error(message)