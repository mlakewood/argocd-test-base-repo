from flask import Flask
import requests
import environ
import structlog
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    BatchSpanProcessor,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Set OpenTelemetry Resource Attributes
resource = Resource(attributes={
    "service.name": "back-app"
})

# Configure OpenTelemetry Tracer and Exporter
trace.set_tracer_provider(TracerProvider(resource=resource))
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(insecure=True, timeout=1))
)
tracer = trace.get_tracer(__name__)


logger = structlog.get_logger()
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

def hello_other():
    return "Other"

@app.route("/message")
def hello_world():
    return {"Message": "Hello, World!"}
