from repositories.base_repository import BaseRepository
from .utils import save_chart_to_png, build_pdf, make_image_element, make_table
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import datetime


def generar_utilizacion_mensual(output_path: str):
    repo = BaseRepository()
    sql = (
        "SELECT strftime('%Y-%m', t.fecha) as mes, COUNT(rd.id_detalle) as usos "
        "FROM ReservaDetalle rd "
        "JOIN Turno t ON rd.id_turno = t.id_turno "
        "GROUP BY mes ORDER BY mes"
    )
    rows = repo.query_all(sql)

    meses = [r["mes"] for r in rows]
    usos = [r["usos"] for r in rows]

    styles = getSampleStyleSheet()
    elements = [Paragraph("Utilización mensual de canchas", styles["Heading2"]), Spacer(1, 12)]

    # Intentar crear gráfico; si falla (por ejemplo incompatibilidad NumPy/matplotlib),
    # generar una tabla con los datos y un mensaje en el PDF.

    try:
        import matplotlib.pyplot as plt

        # Calcular ancho usable en puntos para A4 (72 pts = 1 inch), dejar márgenes
        page_width_pts, page_height_pts = A4
        usable_width_pts = page_width_pts - 2 * 36  # 0.5" (36 pts) margen cada lado

        # Queremos que el gráfico sea más pequeño (p.ej. 70% del ancho usable)
        target_width_pts = usable_width_pts * 0.70

        # Crear figura con ancho en pulgadas equivalente al ancho objetivo
        fig_width_in = target_width_pts / 72
        fig_height_in = 2.5  # altura más reducida para caber mejor en la página
        fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in))
        ax.bar(meses, usos, color="tab:blue")
        ax.set_title("Utilización mensual de canchas")
        ax.set_xlabel("Mes")
        ax.set_ylabel("Cantidad de usos")
        plt.xticks(rotation=45)

        # Guardar gráfico y ajustar el ancho de la imagen en el PDF para que entre en A4
        img_path = save_chart_to_png(fig)
        # Añadir un pequeño espacio superior para centrar visualmente
        elements.append(Spacer(1, 12))
        elements.append(make_image_element(img_path, width=target_width_pts))
        elements.append(Spacer(1, 12))

    except Exception as e:
        # Fallback: tabla con los datos y mensaje de error
        elements.append(Paragraph("No se pudo generar el gráfico por un problema con la librería de gráficos.", styles["Normal"]))
        elements.append(Paragraph(f"Error: {str(e)}", styles["Normal"]))
        # Construir tabla de meses/usos
        table_data = [["Mes", "Usos"]]
        for r in rows:
            table_data.append([r["mes"], str(r["usos"])])
        elements.append(make_table(table_data))

    build_pdf(output_path, "Utilización mensual de canchas", elements)
