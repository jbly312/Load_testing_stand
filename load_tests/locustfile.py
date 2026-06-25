import os
from tasks.browse import ShopUser
from shapes.step_load import StepLoadTest

import influx_listener


ShopUser.host = os.getenv("TARGET_HOST", "http://localhost:8000")


