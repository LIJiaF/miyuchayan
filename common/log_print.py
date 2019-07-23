import logging
import os

log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/log')

if not os.path.exists(log_path):
    os.mkdir(log_path)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=log_path + '/journal.log', filemode='a')
logger = logging.getLogger(__name__)
