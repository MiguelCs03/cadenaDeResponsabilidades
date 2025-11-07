
from flask import Flask, render_template, request, jsonify
from pedido import Pedido
from manejadores import (
    ManejadorInventario,
    ManejadorFraude,
    ManejadorPago,
    ManejadorEnvio
)

app = Flask(__name__)


def crear_cadena_manejadores():
    """Crea y configura la cadena de responsabilidad"""
    inventario = ManejadorInventario()
    fraude = ManejadorFraude()
    pago = ManejadorPago()
    envio = ManejadorEnvio()
    
    # Configurar la cadena
    inventario.set_siguiente(fraude).set_siguiente(pago).set_siguiente(envio)
    
    return inventario


@app.route('/')
def index():
    """Página principal con la interfaz"""
    return render_template('index.html')


@app.route('/procesar_pedido', methods=['POST'])
def procesar_pedido():
    """Endpoint para procesar un pedido"""
    try:
        datos = request.get_json()
        
        # Crear el pedido
        items = datos.get('items', [])
        datos_pago = datos.get('datos_pago', {})
        
        pedido = Pedido(items, datos_pago)
        
        # Crear la cadena y procesar
        cadena = crear_cadena_manejadores()
        cadena.procesar(pedido)
        
        # Retornar el resultado
        return jsonify({
            'success': True,
            'pedido': pedido.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/procesar_paso', methods=['POST'])
def procesar_paso():
    """Endpoint para procesar paso a paso"""
    try:
        datos = request.get_json()
        
        items = datos.get('items', [])
        datos_pago = datos.get('datos_pago', {})
        paso_actual = datos.get('paso', 0)
        
        pedido = Pedido(items, datos_pago)
        
        # Crear manejadores individuales
        manejadores = [
            ManejadorInventario(),
            ManejadorFraude(),
            ManejadorPago(),
            ManejadorEnvio()
        ]
        
        nombres_pasos = ["Inventario", "Fraude", "Pago", "Envío"]
        
        
        for i in range(paso_actual + 1):
            if i < len(manejadores):
                # Crear cadena temporal solo con el manejador actual
                manejador = manejadores[i]
                manejador.procesar(pedido)
                
                
                if pedido.errores:
                    break
        
        return jsonify({
            'success': True,
            'pedido': pedido.to_dict(),
            'paso_actual': paso_actual,
            'nombre_paso': nombres_pasos[paso_actual] if paso_actual < len(nombres_pasos) else "Completado"
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    print(" http://localhost:5000")
    app.run(debug=True, port=5000)
