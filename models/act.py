# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

import base64
from xml import etree

from pandas import *
from odoo import api, fields, models


def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class Bodega(models.Model):
    _name = 'act.bodega'
    _description = 'Activos - Bodega '
    # _rec_name = ''
    codigo = fields.Char('Nominal', required=True, size=3, readonly=True,
                         default=lambda self: compute_default_codigo(self, 3), help='Nominal')
    noBodega = fields.Char('NumeroBodega', required=True, help='Numero de Bodega')
    tipo = fields.Selection([('fisica', 'FISICA'), ('virtual', 'VIRTUAL')],
                            'TIPO DE BODEGA', default='fisica', required=True, help='TIPO DE BODEGA')
    naturaleza = fields.Selection([('administracion', 'ADMINISTRACIÓN'), ('inversion', 'INVERSIÓN'), (
        'produccion', 'PRODUCCIÓN')], 'NATURALEZA', default='administracion', required=True, help='NATURALEZA')
    Denominacion = fields.Char('Denominacion', required=True, help='Denominacion')
    uni_operativa_id = fields.Many2one('pre.centrogestor', string='Centro Gestor', required=True, help='Centro Gestor')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.codigo) +
                           ' ' + str(record.Denominacion)))
        return result

    @api.onchange('uni_operativa_id')
    def _get_code(self):
        centrogestor = self.uni_operativa_id
        codigo = ''
        if centrogestor:
            codigo = centrogestor.codigo + self.codigo

    @api.onchange('Denominacion')
    def _description_mayusculas(self):
        if self.Denominacion:
            self.Denominacion = str(self.Denominacion).upper()


class VidaUtil(models.Model):
    _name = 'act.vidautil'
    _description = 'Activos - Vida Util '
    # _rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self, 4),
                         help='Código del Detalle')
    tipo = fields.Char('Tipo', required=True, help='Nominación de tipo de vida útil')
    adm_proy_prog = fields.Char('Administración Proyectos y Programas', required=True,
                                help='Administración Proyectos y Programas | años')
    produccion = fields.Char('Producción', required=True, help='Producción | UTPE* | numero años')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.tipo))
        return result


class Cabacera(models.Model):
    _name = 'act.cabacera'
    _description = 'Activos - Bienas - Cabecera'
    _rec_name = 'codigo'

    currency_id = fields.Many2one('res.currency', "Currency")

    codigo = fields.Char('Código', required=True, size=20, default=lambda self: compute_default_codigo(self, 5),
                         help='Código del Detalle')
    item_padre = fields.Many2one(related='item_hijo.item_padre_id', string='Item  Categoria', store=False,
                                 readonly=False, domain=[('codigo', 'in', ('53.14', '53.15', '63.14', '63.15', '73.14',
                                                                           '73.15', '84.01', '84.02', '84.03',
                                                                           '84.05'))],
                                 default=lambda self: self.item_hijo.item_padre_id == '5314')
    item_hijo = fields.Many2one('ges.cat.cue.item', string='Item Sub Categoria', required=True)
    tipo_activo = fields.Selection([('BLD', 'Bienes de larga duracion'), ('BCA', 'Control Administrativo')],
                                   string='Tipo Activo', required=True, readonly=True,
                                   help='Activo Fijo (BLD) o Control Administrativo (BCA)')
    fecha_ingreso = fields.Date('Fecha ingreso', required=True, default=fields.Date.today,
                                help='Fecha de ingreso del Bien de Larga Duración')
    forma_ingreso = fields.Selection([('I', 'Individual'), ('M', 'Masivo ')], string='Forma de Ingreso', default='I',
                                     required=True, readonly=True, help='Forma de Ingreso del Bien', store=True)

    bodega_id = fields.Many2one('act.bodega', string='Bodega', required=True, help='Bodega')
    bodega_cod = fields.Char(related='bodega_id.codigo', string='Codigo de Bodega', store=False, readonly=True,
                             help='Codigo de bodega')
    bodega_descripcion = fields.Char(related='bodega_id.Denominacion', string='Denominación', store=False,
                                     readonly=True, help='Denominación de la Bodega')
    bodego_ubicacion = fields.Many2one(related='bodega_id.uni_operativa_id', string='Ubicacion de la Bodega',

                                       readonly=True, help='Ubicacion de la Bodega')

    codigo_bien_padre = fields.Char('Codigo Bien Padre', required=False, default='No definido',
                                    help='Codigo del Bien Padre')

    compra_id = fields.Many2one('com.orden', string='Compra del Bien', required=True)

    certificado_id = fields.Many2one('pre.certificado', string="Certificado", required=True, default=False)

    partida_presupuestaria = fields.Char(related='certificado_id.presupuesto_id.codigo_completo',
                                         string='Partidas Presupuestarias', store=False, readonly=True)

    item_prespuestario = fields.Char(related='certificado_id.presupuesto_id.item_id.codigo',
                                     string='Ítem Prespuestario / Renglón', store=False, readonly=True)

    codigo_proyecto = fields.Char(related='certificado_id.proyecto_institucional_id.codigo',
                                  string='Código Proyecto', store=False, readonly=True)

    cuenta_contable = fields.Many2one('ges.cat.cue.cuenta', string='Cuenta Contable', store=False, readonly=True)

    producto_id = fields.Many2one('prd.producto', string='Producto', required=True, help='Producto')
    producto_codigo = fields.Char(related='producto_id.codigo', string='Identificador', store=False, readonly=True)
    producto_des = fields.Char(related='producto_id.descripcion', string='Catálogo de Bienes', store=False,
                               readonly=True)
    producto_costo = fields.Monetary(string='Costo de Adquisición', default=0.0, store=False, readonly=True)
    descripcion = fields.Char('Descripción - Características del Bien', required=False,
                              help='Descripción  - Características del Bien')

    cantidad_compra = fields.Integer('Cantidad en Compra', readonly=False)
    cantidad_ingresar = fields.Integer('Cantidad por Ingresar', readonly=False)
    cantidad = fields.Integer('Cantidad a Ingresar', help='Catidad de producto', store=True)

    org_ingreso = fields.Selection([('M', 'Matriz'), ('C', 'Compra'), ('D', 'Donacion')], string='Origen del Ingreso',
                                   required=True, help='Origen del Ingreso', default='C', readonly=True)
    tipo_respaldo_id = fields.Many2one('act.tiporespaldo', string='Tipo Respaldo', required=True,
                                       help='Tipo de Documento de Respaldo')
    clase_respaldo_id = fields.Many2one('act.claserespaldo', string='Clase Respaldo', required=True,
                                        help='Clases de Documento de Respaldo')
    tip_comprobante = fields.Selection(
        [('F', 'Factura'), ('NV', 'Notas de Venta'), ('LC', 'Liquidacion de Compras'), ('O', 'Otros')],
        string='Tipo de Comprobante', required=True)
    fecha_comprobante = fields.Date('Fecha de Comprobante', required=True, related='compra_id.fecha',
                                    help='Fecha del comprobante')
    codigo_actual = fields.Char('Código Actual', related='codigo', required=True, help='Código Actual del bien')

    estado = fields.Selection([('B', 'Bueno'), ('R', 'Regular'), ('M', 'Malo')], string='Estado del bien', default='B',
                              required=True, help='Estado del bien')
    depreciacion = fields.Selection([('S', 'SI'), ('N', 'NO')], string='Depreciación', required=True, readonly=True)

    empleado_id = fields.Many2one('ges.rrhh.empleado', string='Empleado', required=True, help='Empleado')
    empleado_identificacion = fields.Char(related='empleado_id.numero_identificacion', string='Identificacion',
                                          required=True, help='Identificacion  Empleado')
    empleado_apellido = fields.Char(related='empleado_id.apellidos', string='Apellidos ', required=True,
                                    help='Apellidos Empleado')
    empleado_nombre = fields.Char(related='empleado_id.nombres', string='Nombres ', required=True,
                                  help='Nombres Empleado')
    empleado_ubicacion = fields.Char(related='empleado_id.numero_residencia', string='Número de la Ubicación',
                                     required=True,
                                     help='Número de la Ubicación')

    valor_contable = fields.Monetary('Valor Contable', default=0.0, required=True, help='Valor Contable')
    valor_residual = fields.Monetary('Valor residual', default=0.0, required=True, help='Valor Residual')
    valor_libros = fields.Monetary('Valor en libros', default=0.0, required=True, help='Valor en libros')
    valor_dep_acumulada = fields.Monetary('Valor Depreciación Acumulada', default=0.0, required=True,
                                          help='Valor Depreciación Acumulada')
    fecha_u_depreciacion = fields.Date('Fecha de la última depreciación', default=fields.Date.today)

    vida_util_id = fields.Many2one('act.vidautil', string='Vida Util', help='Vida Util', required=False)
    vida_anios = fields.Char('Números de años', help='Años de Vida Util', readonly=True)
    vida_util_num = fields.Integer("Unidades | Produccion estimadas", help='Digite el numero de años', default=False)
    cambiar_num_vida = fields.Boolean("No puedo definir: Unidades de Tiempo | Producción Estimadas", default=False)

    observaciones = fields.Text('Observaciones', required=False, help='OBSERVACIONES')

    bienes_muebles_id = fields.One2many('act.mue.bienesmuebles', 'codigo', string='Bienes Muebles', required=True,
                                        help='Bienes Muebles', store=True)

    vehiculos_id = fields.One2many('act.veh.vehiculos', 'codigo', string='Vehiculos', required=False, help='Vehiculos')
    inmueble_id = fields.One2many('act.inm.inmueble', 'codigo', string='Inmueble', required=False, help='Inmueble')
    animal_vivo_id = fields.One2many('act.ani.animalvivo', 'codigo', string='Animal Vivo', required=False,
                                     help='Animal Vivo')
    bosques_plantas_id = fields.One2many('act.bos.bosquesplantas', 'codigo', string='Bosques Plantas', required=False,
                                         help='Bosques Plantas')
    pinacoteca_id = fields.One2many('act.pin.pinacoteca', 'codigo', string='Pinacoteca', required=False,
                                    help='Pinacoteca')
    escultura_id = fields.One2many('act.esc.escultura', 'codigo', string='Escultura', required=False, help='Escultura')
    arqueologia_id = fields.One2many('act.arq.arqueologia', 'codigo', string='Arqueologia', required=False,
                                     help='Arqueologia')
    libros_colecciones_id = fields.One2many('act.lib.libroscolecciones', 'codigo', string='Libros y Colecciones',
                                            required=False, help='Libros y Colecciones')

    tipo_herencia_item = fields.Selection([('6', 'Pinacoteca'), ('7', 'Escultura'), ('8', 'Arqueologia')],
                                          string="Seleccionar Tipo Bien a Ingresar",
                                          store=False)

    duplicacion_datos = fields.Boolean('Los Bienes tiene atributos diferentes', default=False)
    duplicacion_datos_catidad = fields.Boolean(default=False)

    tipo_herencia = fields.Selection(
        [('1', 'Bienes Muebles'), ('2', 'Vehiculos'), ('3', 'Inmueble'), ('4', 'Anivales Vivos'), ('5', 'Bosques'),
         ('6', 'Pinacoteca'), ('7', 'Escultura'), ('8', 'Arqueologia'), ('9', 'Libros')],
        string="Bien Ingresado", required=False, store=True, default='1')

    valor_mostrar = fields.Integer('Variable a mostrar', store=True, default=1)

    @api.model
    def fields_view_get(self, view_id=None, view_type='tree', toolbar=False, submenu=False):
        res = super(Cabacera, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                                 submenu=submenu)
        default_type = self.env.context.get('cantidad', False)
        if default_type:
            doc = etree.XML(res['arch'])
            for t in doc.xpath("//" + view_type):
                t.attrib['create'] = '1'
            res['arch'] = etree.tostring(doc)
        return res

    def hola(self,p):
        print("hola", " >>>>>>>>>>>>>", p)

    def name_get(self):
        result = []
        diccionario = dict(self._fields['tipo_herencia'].selection)
        for record in self:
            result.append((record.id, record.codigo + " " + diccionario[
                str(record.tipo_herencia)] + " | " + record.producto_des + " | " + record.empleado_apellido))
        return result


class TipoIngreso(models.Model):
    _name = 'act.tipoingreso'
    _description = 'Activos - Bienes - Cabecera - Tipo Ingreso Bien'
    # _rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self, 4),
                         help='Codigo Tipo Ingreso')
    tipo = fields.Char('Tipo', required=True, help='Tipo')
    descripcion = fields.Char('Descripción', required=True, help='Descripción del tipo de vehiculo')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.tipo))
        return result


class TipoRespaldo(models.Model):
    _name = 'act.tiporespaldo'
    _description = 'Activos - Bienes - Cabecera - Tipo de Documento de Respaldo'
    # _rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self, 4),
                         help='Codigo del Detalle')
    tipo = fields.Char('Tipo Documento Respaldo', required=True, help='Tipo de Documento de Respaldo')
    descripcion = fields.Char('Descripción', required=True, help='Descripción del tipo de vehiculo')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.tipo + '| ' + record.descripcion))
        return result


class ClaseRespaldo(models.Model):
    _name = 'act.claserespaldo'
    _description = 'Activos - Bienes - Cabecera - Clase de Documento de Respaldo'
    # _rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self, 4),
                         help='Codigo Clase Respaldo')
    tipo = fields.Char('Clase Documento Respaldo', required=True, help='Clase de Documento de Respaldo')
    descripcion = fields.Char('Descripción', required=True, help='Descripción del tipo de vehiculo')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.tipo + '| ' + record.descripcion))
        return result


class Importar(models.Model):
    _name = 'act.importar'
    _description = 'Activos - Bienes - Importar'
    tipo_ingresar = fields.Selection(
        [('1', 'Bienes Muebles'), ('2', 'Vehiculos'), ('3', 'Inmueble'), ('4', 'Anivales Vivos'), ('5', 'Bosques'),
         ('6', 'Pinacoteca'), ('7', 'Escultura'), ('8', 'Arqueologia'), ('9', 'Libros')],
        string="Bien Ingresado", required=True)

    archivo = fields.Binary('CARGAR CSV', store=True)

    @api.onchange('archivo')
    def _onchange_archivo(self):
        if self.archivo:
            f = open("mca_temp.xlsx", "wb")
            f.write(base64.decodestring(self.archivo))
            xls = ExcelFile('mca_temp.xlsx')
            df = xls.parse(xls.sheet_names[0])
            f.close()
            return {
                'name': 'Cabacera',
                'view_type': 'tree',
                'view_mode': 'tree',
                'view_id': 'view_act_cabacera_tree',
                'res_model': 'act.cabacera',
                'context': "{}",
                'type': 'ir.ui.view',
                'target': 'new',
            }
