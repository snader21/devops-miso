import newrelic.agent
import logging

# Inicializar New Relic
newrelic.agent.initialize()

class LoggerUtility:
    logger = None

    @staticmethod
    def initialize_logger():
        if LoggerUtility.logger is None:
            LoggerUtility.logger = logging.getLogger("Basic Logger")
            LoggerUtility.logger.setLevel(logging.INFO)
        
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            LoggerUtility.logger.addHandler(stream_handler)
    
    @staticmethod
    def log_to_new_relic(message):
        newrelic.agent.record_custom_event("CustomLogEvent", {"message": message})
    
    @staticmethod
    def log(message):
        if LoggerUtility.logger is None:
            LoggerUtility.initialize_logger()
        LoggerUtility.logger.info(f"[INFO] {message}")
        LoggerUtility.log_to_new_relic(f"[INFO] {message}")
