import os
import logging

def setup_logger(logger_name, log_file, level=logging.DEBUG):

    log_dir = os.path.join(os.path.dirname(__file__), 'Logs')
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(os.path.join(log_dir, log_file))
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(level)

    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    if not logger.handlers:
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger

pulse_logger = setup_logger("Pulse_System_Logger", "Pulse.log")
pulse_database_logger = setup_logger("Pulse_Database_Logger", "Database.log")

