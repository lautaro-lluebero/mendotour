from flask import Blueprint, render_template, request, jsonify
routes_main = Blueprint('routes_main', __name__)
@routes_main.route('/map')
def map_view():
    return render_template('map.html')

#Routas rutas
@routes_main.route('/rutas')
def rutas():
    return render_template("tour/rutas/rutas.html", title="Rutas turísticas")

@routes_main.route('/ruta-centro')
def ruta_centro():
    return render_template("tour/rutas/ruta_centro.html", title="Ruta Arístides Mendoza")

@routes_main.route('/ruta-bodegas')
def ruta_bodegas():
    return render_template("tour/rutas/ruta_bodegas.html", title="Ruta Bodegas y Viñedos")

@routes_main.route('/ruta-parque')
def ruta_parque():
    return render_template("tour/rutas/ruta_parque.html", title="Ruta Parque General San Martín")

#Routas restaurantes
@routes_main.route('/restaurantes')
def restaurantes():
    return render_template('tour/restaurantes/restaurantes.html', title="Restaurantes")
@routes_main.route('/restaurantes/azafran')
def detalle_azafran():
    return render_template('tour/restaurantes/azafran.html', title="Azafrán")
@routes_main.route('/restaurantes/centauro')
def detalle_centauro():
    return render_template('tour/restaurantes/centauro.html', title="Centauro")
@routes_main.route('/restaurantes/casa')
def detalle_casa():
    return render_template('tour/restaurantes/casa.html', title="Casa Vigil")
@routes_main.route('/restaurantes/campo')
def detalle_campo():
    return render_template('tour/restaurantes/campo.html', title="Casa de Campo")

#Routas bodegas
@routes_main.route('/bodegas')
def bodegas():
    return render_template('tour/bodegas/bodegas.html', title="Bodegas")
@routes_main.route('/bodegas/lujan_de_cuyo')
def detalle_Lujan():
    return render_template('tour/bodegas/Bodega_Catena_Zapata.html', title="Bodega Catena Zapata")
@routes_main.route('/bodegas/valle_de_uco')
def detalle_Valle():
    return render_template('tour/bodegas/Bodega_Salentein.html', title="Bodega Salentein")
@routes_main.route('/bodegas/maipu')
def detalle_Maipu():
    return render_template('tour/bodegas/Bodega_Lopez.html', title="Bodega López")
@routes_main.route('/bodegas/chacras_de_coria')
def detalle_Chacras():
    return render_template('tour/bodegas/Bodega_Alta_Vista.html', title="Bodega Alta Vista")

#Routas atractivos
@routes_main.route('/atractivos')
def atractivos():
    return render_template('tour/atractivos/atractivos.html', title="Atractivos turísticos")
@routes_main.route('/atractivos/villavicencio')
def detalle_villavicencio():
    return render_template('tour/atractivos/villavicencio.html', title="Villavicencio")
@routes_main.route('/atractivos/caverna')
def detalle_caverna():
    return render_template('tour/atractivos/caverna.html', title="Caverna de las Brujas")
@routes_main.route('/atractivos/laguna')
def detalle_laguna():
    return render_template('tour/atractivos/laguna.html', title="Laguna del Diamante")
@routes_main.route('/atractivos/san_martin')
def detalle_san_martin():
    return render_template('tour/atractivos/san_martin.html', title="Parque San Martín")
@routes_main.route('/atractivos/lenas')
def detalle_lenas():
    return render_template('tour/atractivos/lenas.html', title="Las Leñas")
@routes_main.route('/atractivos/potrerillos')
def detalle_potrerillos():
    return render_template('tour/atractivos/potrerillos.html', title="Potrerillos")
@routes_main.route('/atractivos/estadio')
def detalle_estadio():
    return render_template('tour/atractivos/estadio.html', title="Estadio Malvinas Argentinas")
@routes_main.route('/atractivos/puente')
def detalle_puente():
    return render_template('tour/atractivos/puente.html', title="Puente del Inca")

#Routas hospedajes
@routes_main.route('/hospedajes')
def hospedajes():
    return render_template('tour/hospedajes/hospedajes.html', title="Hospedajes")
@routes_main.route('/hospedajes/park_hyatt')
def detalle_park_hyatt():
    return render_template('tour/hospedajes/park_hyatt.html', title="Park Hyatt Mendoza")
@routes_main.route('/hospedajes/diplomatic')
def detalle_diplomatic():
    return render_template('tour/hospedajes/diplomatic.html', title="Diplomatic Hotel")
@routes_main.route('/hospedajes/sheraton')
def detalle_sheraton():
    return render_template('tour/hospedajes/sheraton.html', title="Sheraton Mendoza Hotel")
@routes_main.route('/hospedajes/cielos')
def detalle_cielos():
    return render_template('tour/hospedajes/cielos.html', title="Entre Cielos")

#Routas transporte
@routes_main.route('/transporte')
def transporte():
    return render_template('tour/transporte/transporte.html', title="Medios de transportes")

#Routas actividades
@routes_main.route('/actividades')
def actividades():
    return render_template('tour/actividades/actividades.html', title="Actividades recreativas")
@routes_main.route('/actividades/rafting')
def detalle_rafting():
    return render_template('tour/actividades/rafting.html', title="Rafting")
@routes_main.route('/actividades/cabalgata')
def detalle_cabalgata():
    return render_template('tour/actividades/cabalgata.html', title="Cabalgata")
@routes_main.route('/actividades/museo')
def detalle_museo():
    return render_template('tour/actividades/museo.html', title="Museo del Vino")
@routes_main.route('/actividades/parque')
def detalle_parque():
    return render_template('tour/actividades/parque.html', title="Parque General San Martín")
@routes_main.route('/actividades/termas')
def detalle_termas():
    return render_template('tour/actividades/termas.html', title="Termas de Cacheuta")
@routes_main.route('/actividades/trekking')
def detalle_trekking():
    return render_template('tour/actividades/trekking.html', title="Trekking en Mendoza")

@routes_main.route('/sobre')
def sobre():
    return render_template('sobre.html', title="Sobre Nosotros")
