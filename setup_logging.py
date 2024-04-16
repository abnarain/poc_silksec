import logging

def get_logger():

    logging.basicConfig(
        level=logging.ERROR, 
        format="%(asctime)s - %(levelname)s - %(message)s", 
        #filename="example.log",  # Specify the file to write logs to
        #filemode="a"  # Use 'a' mode to append logs to the file
    )

    logger = logging.getLogger(__name__)
    return logger
