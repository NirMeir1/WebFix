import logging

# Configure logging to write logs to a file and print to console
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Set the default logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Customize the log message format
        handlers=[
            logging.FileHandler("app.log", encoding="utf-8"),  # Logs will be written to 'app.log' in the root directory
            logging.StreamHandler()  # Logs will also be printed to the console
        ]
    )