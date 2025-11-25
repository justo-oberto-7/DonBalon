"""Script para generar los reportes solicitados.

Uso:
    python generar_reportes.py --salida_dir ./salidas --generar all

"""
import os
import argparse
from datetime import datetime

# Import report generators lazily inside the CLI so modules that require heavy
# libs (matplotlib) are only imported when needed.


def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def main():
    parser = argparse.ArgumentParser(description="Generar reportes DonBalon")
    parser.add_argument("--salida_dir", default="./reportes_out", help="Directorio de salida para los PDFs")
    parser.add_argument("--generar", default="all", choices=["all", "por_cliente", "por_cancha", "mas_utilizadas", "mensual"], help="Qué reporte generar")
    parser.add_argument("--id_cancha", type=int, default=1, help="Id de la cancha para reporte por cancha")
    parser.add_argument("--id_cliente", type=int, default=1, help="Id del cliente para reporte por cliente")
    parser.add_argument("--inicio", default=(datetime.now().date().replace(day=1).isoformat()), help="Fecha inicio YYYY-MM-DD")
    parser.add_argument("--fin", default=(datetime.now().date().isoformat()), help="Fecha fin YYYY-MM-DD")

    args = parser.parse_args()
    salida = args.salida_dir
    ensure_dir(salida)

    if args.generar in ("all", "por_cliente"):
        from .report_reservas_por_cliente import generar_reservas_por_cliente
        generar_reservas_por_cliente(os.path.join(salida, "reservas_por_cliente.pdf"), args.id_cliente)

    if args.generar in ("all", "por_cancha"):
        from .report_reservas_por_cancha_periodo import generar_reservas_por_cancha
        generar_reservas_por_cancha(os.path.join(salida, "reservas_por_cancha.pdf"), args.id_cancha, args.inicio, args.fin)

    if args.generar in ("all", "mas_utilizadas"):
        from .report_canchas_mas_utilizadas import generar_canchas_mas_utilizadas
        generar_canchas_mas_utilizadas(os.path.join(salida, "canchas_mas_utilizadas.pdf"))

    if args.generar in ("all", "mensual"):
        from .report_utilizacion_mensual import generar_utilizacion_mensual
        generar_utilizacion_mensual(os.path.join(salida, "utilizacion_mensual.pdf"))

    print(f"Reportes generados en: {os.path.abspath(salida)}")


if __name__ == "__main__":
    main()
