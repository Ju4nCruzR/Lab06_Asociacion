# =============================================================================
# Modelos de datos: LineItem y Factura
# =============================================================================

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class LineItem:
    producto: str
    cantidad: float
    precio_unitario: float
    subtotal: float


@dataclass
class Factura:
    numero: int
    fecha: date
    dia_semana: str
    items: List[LineItem] = field(default_factory=list)

    @property
    def total(self) -> float:
        return sum(i.subtotal for i in self.items)

    @property
    def total_iva(self) -> float:
        # IVA = total * 0.19 aproximado, pero lo calculamos desde los items
        return self.total * 0.19

    @property
    def cantidad_total_items(self) -> int:
        return len(self.items)