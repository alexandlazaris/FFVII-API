import os
import logfire
from dotenv import load_dotenv

class Telemetry:
    def initialise(self, app):
        load_dotenv()    
        logfire.configure(service_name=os.getenv("SERVICE_NAME"), environment=os.getenv("LOGFIRE_ENVIRONMENT"))
        logfire.instrument_flask(app)

telemetry = Telemetry()