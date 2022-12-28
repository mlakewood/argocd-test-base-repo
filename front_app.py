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
    "service.name": "front-app"
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

@environ.config
class AppConfig:
    back_app_host = environ.var(help="This is the back_app hostname")
    back_app_port = environ.var(help="This is the back_app port")

@app.route("/health")
def health():
    return "ok"

@app.route("/")
def hello_world():
    cfg = environ.to_config(AppConfig)

    resp = requests.get(f"http://{cfg.back_app_host}:{cfg.back_app_port}/message")
    if resp.status_code == 200:
        return f"<p>{resp.json()['Message']}</p>"
    else:
        return "<p>oops something bad happend</p>"