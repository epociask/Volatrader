"""
Functional logger script to log data to either .txt file or Slack
"""
import logging
from datetime import datetime
from Helpers.HelpfulOperators import cleanDate
import slack
import os
from enum import *

class Channel(Enum):
    """
    Enum used to represent different slack channels
    """

    DEBUG = '#debug'
    VOLATRADER = '#volatrader'


class MessageType(Enum):
    """
    Enum used to represent different message types
    """
    ERROR = 'error'
    WARNING = 'warning'
    DEBUG = 'debug'


""""
    GLOBAL VARIABLES 
"""

configFile = None  # initally none, redefined in local scope of checkIfConfig()
slack_token = os.environ.get('SLACK_API_TOKEN')
client = slack.WebClient(token=slack_token)
logger = None


def logToSlack(message, channel: Channel = Channel.DEBUG, tagChannel=False,
               messageType: MessageType = MessageType.WARNING):
    """"
    Logs data message to slack channel
    @:param message to send to slackbot
    @:param channel -> channel enum, preset to DEBUG channel unless specified otherwise
    @:param tagChannel -> boolean that specifies if @channel should be used, preset to false unless specified otherwise
    @:param messageType -> corresponds to messageType enum; determines which error to log to file
    @:returns None
    """
    if messageType.WARNING:
        logWarningToFile(message)
    elif messageType.DEBUG:
        logDebugToFile(message)
    elif messageType.ERROR:
        logDebugToFile(message)

    client.chat_postMessage(
        channel=channel.value,
        text=f'{"<!channel>" if tagChannel else ""} *[{messageType.value.upper()}]* ```{message}```'
    )


def configureFile() -> None:
    """
    Configures basic configuration settings for txt log file
    """

    cwd = os.getcwd()
    logdir = os.path.join(cwd, 'logs/')

    logging.basicConfig(filename=os.path.join(logdir, cleanDate(str(datetime.now())) + ".txt"),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(lineno)d %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    global logger
    logger = logging.getLogger("[DATABASE_LOGGER]")
    logger.setLevel(logging.DEBUG)
    requestLogger = logging.getLogger("requests")
    requestLogger.setLevel(logging.ERROR)
    urllibLogger = logging.getLogger("urllib3")
    urllibLogger.setLevel(logging.ERROR)
    ccxtLogger = logging.getLogger("ccxt")
    
def logDebugToFile(data: str) -> None:
    """
    Logs debug data to txt file in logs directory
    @:param data -> data to log to file
    @:returns Nothing
    """

    checkIfConfig()
    global logger
    logger.debug(f'[DEBUG] {data}\n')


def logWarningToFile(warning: str) -> None:
    """
    Logs warning data to txt file in logs directory
    @:param warning -> warning data to log to file
    @:returns Nothing
    """
    checkIfConfig()
    global logger
    logger.warning(f'[WARNING] {warning}\n')




def logErrorToFile(error: str) -> None:
    """
    Logs error data to txt file in logs directory
    @:param error -> error message to log to file
    @:returns Nothing
    """

    checkIfConfig()
    global logger
    logger.error(f'[ERROR] {error}\n')


def checkIfConfig() -> None:
    """
    Checks if txt file has been configured yet ====> if it hasn't then @configFile is called
    @:returns None
    """
    global configFile
    if configFile is None:
        configureFile()
        configFile = True


def resetConfig() -> None:
    """
    Sets global configFile variable to None
    """
    global configFile
    configFile = None

