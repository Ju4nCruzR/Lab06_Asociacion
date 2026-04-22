# =============================================================================
# Parser de archivos DBF a objetos Factura y LineItem
# =============================================================================

import os
import re
from datetime import datetime
from dbfread import DBF
from src.models import LineItem, Factura


def _extraer_fecha_desde_nombre(nombre_archivo: str) -> datetime:
    # Formato: fcDDMMAAAA.DBF
    match = re.search(r'fc(\d{2})(\d{2})(\d{4})', nombre_archivo)
    if not match:
        raise ValueError(f"No se pudo extraer fecha de: {nombre_archivo}")
    dia, mes, anio = int(match.group(1)), int(match.group(2)), int(match.group(3))
    return datetime(anio, mes, dia)


def _limpiar_nombre_producto(descri: str) -> str:
    return descri.strip().rstrip('B').strip() if descri else 'DESCONOCIDO'


def cargar_dbf(ruta_archivo: str, dia_semana: str) -> list[Factura]:
    tabla = DBF(ruta_archivo, encoding='latin-1')
    fecha = _extraer_fecha_desde_nombre(os.path.basename(ruta_archivo))

    facturas_dict: dict[int, Factura] = {}

    for row in tabla:
        numero = row['FACNRO']
        if numero not in facturas_dict:
            facturas_dict[numero] = Factura(
                numero=numero,
                fecha=fecha.date(),
                dia_semana=dia_semana
            )

        item = LineItem(
            producto=_limpiar_nombre_producto(row['DESCRI']),
            cantidad=float(row['CANT'] or 0),
            precio_unitario=float(row['PRECIO'] or 0),
            subtotal=float(row['TOTAL'] or 0)
        )
        facturas_dict[numero].items.append(item)

    return list(facturas_dict.values())


def cargar_todos(ruta_datos: str) -> list[Factura]:
    todas = []

    for dia_semana in os.listdir(ruta_datos):
        ruta_dia = os.path.join(ruta_datos, dia_semana)
        if not os.path.isdir(ruta_dia):
            continue
        for archivo in os.listdir(ruta_dia):
            if archivo.endswith('.DBF'):
                ruta = os.path.join(ruta_dia, archivo)
                facturas = cargar_dbf(ruta, dia_semana)
                todas.extend(facturas)

    return todas