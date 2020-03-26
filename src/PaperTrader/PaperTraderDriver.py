# import time
# from datetime import datetime
#
# from Helpers.Logger import logToSlack
#
# while True:
#
#     try:
#         t = int(str(datetime.now())[14:16])
#         if t % timeStep == 0 or t == 0:
#
#
#     except Exception as e:
#         logToSlack(f"DATABASE BREAKING ERROR :: \n{e}", tagChannel=True)
