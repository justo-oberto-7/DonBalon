import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os


def save_chart_to_png(fig) -> str:
    """Guarda una figura matplotlib en un archivo PNG temporal y devuelve la ruta."""
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    # Import matplotlib lazily to avoid importing it when not needed
    import matplotlib.pyplot as plt
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def build_pdf(path: str, title: str, elements: list):
    """Construye un PDF en `path` con los elementos Platypus dados."""
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    header = Paragraph(title, styles["Title"])
    story = [header, Spacer(1, 12)]
    story.extend(elements)
    doc.build(story)


def make_table(data, col_widths=None):
    """Crea un Table estilizada para reportlab a partir de una lista de filas."""
    table = Table(data, colWidths=col_widths)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ]
    table.setStyle(style)
    return table


def make_image_element(image_path, width=None, height=None):
    img = Image(image_path)
    if width:
        img.drawWidth = width
    if height:
        img.drawHeight = height
    # Center horizontally by default
    try:
        img.hAlign = 'CENTER'
    except Exception:
        pass
    return img
