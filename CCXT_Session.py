from authent import authList
from authent import getExchangeInstance
from TrailingStopLoss import Session


class Sessions:

    def __init__(self):
        self.sessions = []
        self.active = True

    # TODO add method to close session and output data when it's no longer active... ie has sold

    def start(self) -> None:  # initializes all session options from authent.
        print('STARTING.....')
        sess = None
        for authorization in authList:
            try:
                tempInst = getExchangeInstance(authorization)
                sess = Session(tempInst)
                sess.initializeSession()
                self.sessions.append(sess)

            except Exception as e:
                print("ERROR: ", e)
                if sess is None and self.sessions.count(sess) is not 0:
                    del self.sessions[self.sessions.index(sess)]


    def run(self):
        # TODO mulithread session operations in for loop
        print(self.sessions)
        for session in self.sessions:
            session.run()

