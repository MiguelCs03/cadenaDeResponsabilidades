"""
Clase Pedido que representa un pedido en el sistema
"""
from typing import List, Dict, Any


class Pedido:
    """Clase que representa un pedido con sus datos"""
    
    def __init__(self, items: List[Dict[str, Any]], datos_pago: Dict[str, Any]):
        self.items = items  # Lista de items: [{'producto': 'X', 'cantidad': 2, 'stock': 5}]
        self.datos_pago = datos_pago  # {'monto': 100, 'tarjeta': '1234', 'usuario_id': 1}
        self.estado = "Pendiente"
        self.errores: List[str] = []
        self.pasos_completados: List[str] = []
    
    def agregar_error(self, error: str):
        """Agrega un error al pedido"""
        self.errores.append(error)
    
    def agregar_paso_completado(self, paso: str):
        """Agrega un paso completado al pedido"""
        self.pasos_completados.append(paso)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el pedido a diccionario para JSON"""
        return {
            'items': self.items,
            'datos_pago': self.datos_pago,
            'estado': self.estado,
            'errores': self.errores,
            'pasos_completados': self.pasos_completados
        }
