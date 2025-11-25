from repositories.cliente_repository import ClienteRepository
from repositories.reserva_repository import ReservaRepository
from repositories.reserva_detalle_repository import ReservaDetalleRepository
from repositories.turno_repository import TurnoRepository
from repositories.cancha_repository import CanchaRepository
from .utils import build_pdf, make_table
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generar_reservas_por_cliente(output_path: str, id_cliente: int):
    """Genera un PDF con las reservas de un cliente específico.

    Args:
        output_path: Ruta del PDF de salida.
        id_cliente: Id del cliente cuyas reservas se desean listar.
    """
    clientes_repo = ClienteRepository()
    reserva_repo = ReservaRepository()
    detalle_repo = ReservaDetalleRepository()
    turno_repo = TurnoRepository()
    cancha_repo = CanchaRepository()

    cliente = clientes_repo.get_by_id(id_cliente)

    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph(f"Listado de reservas - Cliente id={id_cliente}", styles["Heading2"]))

    if not cliente:
        elements.append(Paragraph("Cliente no encontrado.", styles["Normal"]))
        build_pdf(output_path, f"Reservas por Cliente {id_cliente}", elements)
        return

    header = Paragraph(f"Cliente: {cliente.nombre} {cliente.apellido} (id={cliente.id_cliente})", styles["Heading4"])
    elements.append(header)

    reservas = reserva_repo.get_by_cliente(cliente.id_cliente)
    if not reservas:
        elements.append(Paragraph("No tiene reservas.", styles["Normal"]))
        elements.append(Spacer(1, 8))
        build_pdf(output_path, f"Reservas por Cliente {cliente.nombre} {cliente.apellido}", elements)
        return

    table_data = [["ID Reserva", "Fecha", "Monto", "Estado", "Detalle (Cancha - Fecha - Horario)"]]
    for r in reservas:
        detalles = detalle_repo.get_by_reserva(r.id_reserva)
        detalle_texts = []
        for d in detalles:
            turno = turno_repo.get_by_id(d.id_turno)
            cancha = cancha_repo.get_by_id(turno.id_cancha) if turno else None
            detalle_texts.append(f"{cancha.nombre if cancha else 'N/A'} - {turno.fecha if turno else 'N/A'} - turno:{turno.id_horario if turno else 'N/A'}")
        table_data.append([
            str(r.id_reserva),
            str(r.fecha_reserva),
            str(r.monto_total),
            str(r.estado_nombre),
            "\n".join(detalle_texts),
        ])

    elements.append(make_table(table_data))
    elements.append(Spacer(1, 12))

    build_pdf(output_path, f"Reservas por Cliente {cliente.nombre} {cliente.apellido}", elements)
