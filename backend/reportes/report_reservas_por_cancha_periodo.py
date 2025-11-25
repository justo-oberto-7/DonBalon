from repositories.turno_repository import TurnoRepository
from repositories.reserva_detalle_repository import ReservaDetalleRepository
from repositories.reserva_repository import ReservaRepository
from repositories.cancha_repository import CanchaRepository
from repositories.cliente_repository import ClienteRepository
from .utils import build_pdf, make_table
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generar_reservas_por_cancha(output_path: str, id_cancha: int, fecha_inicio: str, fecha_fin: str):
    """Genera un PDF con las reservas de una cancha en un período.

    fechas en formato YYYY-MM-DD
    """
    turno_repo = TurnoRepository()
    detalle_repo = ReservaDetalleRepository()
    reserva_repo = ReservaRepository()
    cancha_repo = CanchaRepository()
    cliente_repo = ClienteRepository()

    inicio = datetime.fromisoformat(fecha_inicio).date()
    fin = datetime.fromisoformat(fecha_fin).date()

    turnos = turno_repo.get_by_cancha(id_cancha)
    turnos_periodo = [t for t in turnos if inicio <= datetime.fromisoformat(str(t.fecha)).date() <= fin]

    elements = []
    styles = getSampleStyleSheet()
    nombre_cancha = cancha_repo.get_by_id(id_cancha).nombre if cancha_repo.get_by_id(id_cancha) else f"Cancha {id_cancha}"
    elements.append(Paragraph(f"Reservas para {nombre_cancha} desde {fecha_inicio} hasta {fecha_fin}", styles["Heading2"]))

    table_data = [["ID Reserva", "Fecha Turno", "ID Turno", "Cliente", "Monto Item"]]
    for t in turnos_periodo:
        detalles = detalle_repo.get_by_turno(t.id_turno)
        for d in detalles:
            reserva = reserva_repo.get_by_id(d.id_reserva)
            cliente = cliente_repo.get_by_id(reserva.id_cliente) if reserva else None
            table_data.append([
                str(d.id_reserva),
                str(t.fecha),
                str(t.id_turno),
                f"{cliente.nombre} {cliente.apellido}" if cliente else "N/A",
                str(d.precio_total_item),
            ])

    elements.append(make_table(table_data))
    elements.append(Spacer(1, 12))

    build_pdf(output_path, f"Reservas por Cancha {nombre_cancha}", elements)
