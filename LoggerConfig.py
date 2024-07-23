import logging
import os

log_file_path = os.path.join(os.path.dirname(__file__), 'Logs', 'Pulse.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logger = logging.getLogger("Pulse_Logger")
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(log_file_path)
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.DEBUG)

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)
