# Logger for pass/fail results and errors
import logging
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))


# Set the log file path to the script's directory
log_file_path = os.path.join(script_dir, 'reports/logs', 'cbe_test_report_logs.log')
print('Setting log file path to: ', log_file_path)

logging.basicConfig(
    filename=log_file_path,  # Log to a file (use 'selenium_test.log')
    filemode='a',                  # Overwrite the log file each run (use 'a' to append) or (use 'w' to overide)
    format='%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',  # Log format including file name and line number
    level=logging.INFO              # Logging level
)


def log_info(error):
    print(error)
    logging.info(error)

def log_error(error):
    print(error)
    logging.error(error)

