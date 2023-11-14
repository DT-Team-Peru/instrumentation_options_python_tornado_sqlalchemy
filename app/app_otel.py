import tornado.ioloop
import tornado.web
import json
import os
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#### OTEL Python ####

# OpenTelemetry imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metrics_exporter import OTLPMetricsExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.tornado import TornadoInstrumentor

# Configuración del nombre del servicio para OTel
resource = Resource.create({SERVICE_NAME: "python_pedidos"})

# Configuración de OpenTelemetry para Traces
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configuración del Exportador OTLP para Trazas
otlp_span_exporter = OTLPSpanExporter(
    endpoint=os.getenv("DT_URL"),
    headers={"Authorization": f"Api-Token {os.getenv('DT_TOKEN')}"},
    protocol="http/protobuf"
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_span_exporter))

# Configuración de OpenTelemetry para Metrics
metrics.set_meter_provider(MeterProvider(resource=resource))
meter = metrics.get_meter(__name__)

# Configuración del Exportador OTLP para Métricas
otlp_metrics_exporter = OTLPMetricsExporter(
    endpoint=os.getenv("DT_URL"),
    headers={"Authorization": f"Api-Token {os.getenv('DT_TOKEN')}"},
    protocol="http/protobuf"
)
metrics.get_meter_provider().add_metric_reader(PeriodicExportingMetricReader(otlp_metrics_exporter))

#### OTEL Python ####

# Obtener variables de entorno
db_host = os.getenv('DBHOST', 'localhost')  # Default a 'localhost' si no está definida
db_port = os.getenv('DBPORT', '3306')       # Default a '3306' si no está definida

# Configuración de la Base de Datos
DATABASE_URI = f'mysql+pymysql://user:password@{db_host}:{db_port}/mydatabase'
Base = declarative_base()

# Modelo SQLAlchemy para pedidos
class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    numero = Column(Integer)

# Crear motor y sesión de SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Tornado Request Handler para /ping
class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("pong")

# Tornado Request Handler para /pedido (POST)
class PedidoHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        try:
            numero = int(data.get('numero'))
            session = Session()
            nuevo_pedido = Pedido(numero=numero)
            session.add(nuevo_pedido)
            session.commit()
            session.close()
            self.write({"message": "registro agregado"})
        except ValueError:
            self.set_status(400)
            self.write({"error": "Solo se aceptan números"})

# Tornado Request Handler para /pedidos (GET)
class PedidosHandler(tornado.web.RequestHandler):
    def get(self):
        session = Session()
        pedidos = session.query(Pedido).all()
        session.close()
        self.write({"pedidos": [{"id": pedido.id, "numero": pedido.numero} for pedido in pedidos]})

# Crear aplicación Tornado y definir rutas
def make_app():
    return tornado.web.Application([
        (r"/ping", PingHandler),
        (r"/pedido", PedidoHandler),
        (r"/pedidos", PedidosHandler),
    ])

#### OTEL Python ####
# Instrumentar Tornado
TornadoInstrumentor().instrument()
#### OTEL Python ####

# Ejecutar aplicación
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
