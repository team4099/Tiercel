from enum import Enum

class Status(Enum):
    NOT_STARTED = "Not started"
    ON_HOLD = "On Hold"
    IN_PROGRESS = "In progress"
    DONE = "Done"

    @staticmethod
    def from_str(label):
        if label in ("Not started"):
            return Status.NOT_STARTED
        elif label in ("On Hold"):
            return Status.ON_HOLD
        elif label in ("In progress"):
            return Status.IN_PROGRESS
        elif label in ("Done"):
            return Status.DONE
        else:
            raise NotImplementedError