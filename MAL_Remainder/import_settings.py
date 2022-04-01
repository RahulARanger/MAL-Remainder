import sys
from MAL_Remainder.utils import SETTINGS, Settings

if __name__ == "__main__":
    temp = Settings(sys.argv[-1])
    SETTINGS.from_dict(temp.to_dict()) if sys.argv[-1] else ...
    SETTINGS.close()
    temp.close()
