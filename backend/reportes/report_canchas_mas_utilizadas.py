from repositories.base_repository import BaseRepository
from .utils import build_pdf, make_table
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generar_canchas_mas_utilizadas(output_path: str, top_n: int = 10):
    repo = BaseRepository()
    sql = (
        "SELECT t.id_cancha as id_cancha, c.nombre as nombre, COUNT(rd.id_detalle) as usos "
        "FROM ReservaDetalle rd "
        "JOIN Turno t ON rd.id_turno = t.id_turno "
        "JOIN Cancha c ON t.id_cancha = c.id_cancha "
        "GROUP BY t.id_cancha ORDER BY usos DESC"
    )
    rows = repo.query_all(sql)

    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Canchas más utilizadas", styles["Heading2"]))

    table_data = [["ID Cancha", "Nombre", "Usos"]]
    count = 0
    for r in rows:
        if count >= top_n:
            break
        table_data.append([str(r["id_cancha"]), r["nombre"], str(r["usos"])])
        count += 1

    elements.append(make_table(table_data))
    elements.append(Spacer(1, 12))
    build_pdf(output_path, "Canchas más utilizadas", elements)
