from authent import authList
from authent import getExchangeInstance
from LiveTrader.TrailingStopLoss import Session
from Helpers.Logger import logDebugToFile


class LiveSession:

    def __init__(self):
        self.sessions = []
        self.active = True

    # TODO add method to close session and output data when it's no longer active... ie has sold

    def start(self) -> None:
        """
         initializes all session options from authe
        :return:
        """
        sess = None
        for authorization in authList:
            print(authList)
            try:
                tempInst = getExchangeInstance(authorization)
                sess = Session(tempInst)
                sess.initializeSession()
                self.sessions.append(sess)

            except Exception as e:
                logDebugToFile(e)
                if sess is None and self.sessions.count(sess) is not 0:
                    del self.sessions[self.sessions.index(sess)]

    def run(self):
        print(self.sessions)
        for session in self.sessions:
            session.run()


test = LiveSession()
test.start()
test.run()