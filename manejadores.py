
from abc import ABC, abstractmethod
from pedido import Pedido
import time
# cadena de responsabilidad para el procesamiento de pedidos
#Miguel Acs
class ManejadorPedido(ABC):
    """Interfaz para los manejadores de pedidos"""
    
    @abstractmethod
    def set_siguiente(self, manejador: 'ManejadorPedido') -> 'ManejadorPedido':
        """Establece el siguiente manejador en la cadena"""
        pass
    
    @abstractmethod
    def procesar(self, pedido: Pedido) -> None:
        """Procesa el pedido"""
        pass


class ManejadorInventario(ManejadorPedido):
    """Manejador que verifica el inventario"""
    
    def __init__(self):
        self._siguiente_manejador: ManejadorPedido = None
    
    def set_siguiente(self, manejador: ManejadorPedido) -> ManejadorPedido:
        """Establece el siguiente manejador en la cadena"""
        self._siguiente_manejador = manejador
        return manejador
    
    def procesar(self, pedido: Pedido) -> None:
        """Verifica que hay suficiente stock para todos los items"""
        print(" Verificando inventario...")
        time.sleep(0.5)  # Simular procesamiento
        
        errores = []
        for item in pedido.items:
            producto = item.get('producto', 'Desconocido')
            cantidad = item.get('cantidad', 0)
            stock = item.get('stock', 0)
            
            if cantidad > stock:
                errores.append(f"Stock insuficiente para {producto}: necesita {cantidad}, disponible {stock}")
        
        if errores:
            pedido.estado = "Rechazado - Inventario"
            for error in errores:
                pedido.agregar_error(error)
            print(" Error en inventario")
        else:
            pedido.agregar_paso_completado("Inventario")
            print(" Inventario verificado")
            # Solo continuar si no hay errores
            if self._siguiente_manejador:
                self._siguiente_manejador.procesar(pedido)


class ManejadorFraude(ManejadorPedido):
    """Manejador que detecta posibles fraudes"""
    
    def __init__(self):
        self._siguiente_manejador: ManejadorPedido = None
    
    def set_siguiente(self, manejador: ManejadorPedido) -> ManejadorPedido:
        """Establece el siguiente manejador en la cadena"""
        self._siguiente_manejador = manejador
        return manejador
    
    def procesar(self, pedido: Pedido) -> None:
        """Verifica si el pedido es fraudulento"""
        print(" Verificando fraude...")
        time.sleep(0.5)  # Simular procesamiento
        
        # Simulación de detección de fraude
        monto = pedido.datos_pago.get('monto', 0)
        tarjeta = pedido.datos_pago.get('tarjeta', '')
        usuario_id = pedido.datos_pago.get('usuario_id', 0)
        
        es_fraudulento = False
        
        # Reglas simples de detección
        if monto > 10000:
            es_fraudulento = True
            pedido.agregar_error("Monto sospechosamente alto")
        
        if tarjeta == '0000':
            es_fraudulento = True
            pedido.agregar_error("Tarjeta en lista negra")
        
        if usuario_id < 0:
            es_fraudulento = True
            pedido.agregar_error("Usuario sospechoso")
        
        if es_fraudulento:
            pedido.estado = "Rechazado - Fraude"
            print(" Fraude detectado")
        else:
            pedido.agregar_paso_completado("Fraude")
            print(" Sin fraude detectado")
            if self._siguiente_manejador:
                self._siguiente_manejador.procesar(pedido)


class ManejadorPago(ManejadorPedido):
    """Manejador que procesa el pago"""
    
    def __init__(self):
        self._siguiente_manejador: ManejadorPedido = None
    
    def set_siguiente(self, manejador: ManejadorPedido) -> ManejadorPedido:
        """Establece el siguiente manejador en la cadena"""
        self._siguiente_manejador = manejador
        return manejador
    
    def procesar(self, pedido: Pedido) -> None:
        """Procesa el pago del pedido"""
        print(" Procesando pago...")
        time.sleep(0.5)  # Simular procesamiento
        
        monto = pedido.datos_pago.get('monto', 0)
        tarjeta = pedido.datos_pago.get('tarjeta', '')
        
        # Simulación de procesamiento de pago
        if not tarjeta or len(tarjeta) < 4:
            pedido.estado = "Rechazado - Pago"
            pedido.agregar_error("Tarjeta inválida")
            print(" Error en pago")
        elif monto <= 0:
            pedido.estado = "Rechazado - Pago"
            pedido.agregar_error("Monto inválido")
            print(" Error en pago")
        else:
            pedido.agregar_paso_completado("Pago")
            print(" Pago procesado")
            if self._siguiente_manejador:
                self._siguiente_manejador.procesar(pedido)


class ManejadorEnvio(ManejadorPedido):
    """Manejador que gestiona el envío"""
    
    def __init__(self):
        self._siguiente_manejador: ManejadorPedido = None
    
    def set_siguiente(self, manejador: ManejadorPedido) -> ManejadorPedido:
        """Establece el siguiente manejador en la cadena"""
        self._siguiente_manejador = manejador
        return manejador
    
    def procesar(self, pedido: Pedido) -> None:
        """Procesa el envío del pedido"""
        print(" Procesando envío...")
        time.sleep(0.5)  # Simular procesamiento
        
        pedido.agregar_paso_completado("Envío")
        pedido.estado = "Completado"
        print(" Envío procesado - ¡Pedido completado!")
        
        # Este es el último, no hay siguiente
