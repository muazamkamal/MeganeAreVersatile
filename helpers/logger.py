from dateutil import tz
import datetime

class Logger:
    def __init__(self, db, console = False):
        self.db = db
        self.console = console

    def log_response(self, res_type, sub_id, response, caller = None):
        if not caller:
            caller = sub_id

        time = datetime.datetime.now(tz = tz.gettz())

        data = {
            u"time": str(time),
            u"response_type": res_type,
            u"submission_id": str(sub_id),
            u"response_id": str(response),
            u"caller_id": str(caller)
        }

        self.db.log(data)

        if self.console:
            print(f"Time: {time}")
            print(f"Type: {res_type}")
            print(f"Submission ID: {sub_id}")
            print(f"Response ID: {response}")
            print(f"Caller ID: {caller}")