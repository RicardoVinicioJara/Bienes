from ..models import act
from odoo import api
from odoo.exceptions import ValidationError
from datetime import date


def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class act_controlador(act.Cabacera):
    @api.onchange('fecha_ingreso')
    def onchange_date(self):
        if self.fecha_comprobante:
            if self.fecha_ingreso < self.fecha_comprobante:
                return {
                    'warning': {
                        'title': 'Fecha Icorrecta!',
                        'message': 'La fecha no puede ser menor a la fecha registrada de la compra del Bien <br> Se '
                                   'Ingresara la fecha Actual',
                        'type': 'notification'}
                }
                self.fecha_ingreso = date.today()

    @api.onchange('tipo_herencia_item')
    def _change_herencia(self):
        if self.tipo_herencia_item:
            self.tipo_herencia = self.tipo_herencia_item

    @api.onchange('item_padre')
    def _change_item_padre(self):
        a = self.item_padre
        if a:
            tipo = a.codigo
            res = tipo[0:3]
            if res in ['53.', '63.', '73.']:
                self.tipo_activo = 'BCA'
                self.depreciacion = 'N'
            elif res == '84.':
                self.depreciacion = 'S'
                self.tipo_activo = 'BLD'
            self.item_hijo = False
            self.item_padre = a
            self.tipo_herencia = '1'
            self.compra_id = False
            self.producto_id = False
            self.certificado_id = False

    @api.onchange('item_hijo')
    def _change_item_hijo(self):
        if self.item_hijo:
            codigo = self.item_hijo.codigo

            if codigo in ['84.02.01', '84.03.01'] and self.depreciacion == 'S':
                self.depreciacion = 'N'

            # Vehiculos
            if codigo in ['84.01.05']:
                self.tipo_herencia = '2'
            # Inmuebles
            elif codigo in ['84.02.01', '84.02.02', '84.02.03', '84.03.01', '84.03.02']:
                self.tipo_herencia = '3'
            # Animales Vivos
            elif codigo in ['84.05.12', '53.15.12', '3.15.12', '73.15.12']:
                self.tipo_herencia = '4'
            # Bosques y Plantas
            elif codigo in ['84.05.13', '84.05.14', '84.05.15',
                            '53.15.14', '53.15.15',
                            '63.15.14', '63.15.15',
                            '73.15.14', '73.15.15']:
                self.tipo_herencia = '5'
            # Pinacoteca | Escultura | Arqueologia
            elif codigo in ['84.01.08', '53.14.08', '73.14.08']:
                self.tipo_herencia = '6'
            # Libros y Colecciones
            elif codigo in ['84.01.09', '53.14.09', '73.14.09']:
                self.tipo_herencia = '9'
            # Bienes
            else:
                self.tipo_herencia = '1'

            # self.valor_mostrar = 6

            domain = [('certificado_ids.certificado_id.presupuesto_id.item_id.codigo', '=', codigo)]
            return {'domain': {'compra_id': domain}}

    @api.onchange('compra_id')
    def _change_compra(self):
        compra = self.compra_id
        codigo = compra.codigo
        if self.compra_id:
            self.producto_id = False
            self.certificado_id = False
            # hay de definir que tipo de comprobente
            self.tip_comprobante = 'F'
            lis_detalles = compra.proveedor_adjudicado_id.proveedor_orden_detalle_ids
            list_productos = []
            for produ in lis_detalles:
                list_productos.append(produ.producto_id)
            productos = []
            for l in list_productos:
                for it in l.producto_item_ids:
                    if it.codigo == self.item_hijo.codigo:
                        productos.append(l.codigo)
            domain = [('codigo', 'in', productos)]

            for l in self.compra_id.certificado_ids:
                if l.certificado_id.presupuesto_id.item_id == self.item_hijo:
                    self.certificado_id = l.certificado_id.id

            return {'domain': {'producto_id': domain}}

    @api.onchange('certificado_id')
    def _change_certificado(self):
        if self.certificado_id:
            self.bodega_id = False
            enlace = self.certificado_id.presupuesto_id.enlace_id
            item = self.certificado_id.presupuesto_id.item_id
            self.cuenta_contable = self.env['ges.cat.cue.plancuenta'].search(
                [('item_debito_id.codigo', '=', item.codigo), ('enlace_id.codigo', '=', enlace.codigo)]).cuenta_id

    @api.onchange('producto_id')
    def _change_producto(self):
        producto = self.producto_id
        codigo = str(producto.codigo)
        if codigo != 'False':
            compra = self.compra_id
            lit = compra.proveedor_adjudicado_id.proveedor_orden_detalle_ids
            for l in lit:
                if l.producto_id.codigo == producto.codigo:
                    # Sacamos todo para los calculos
                    self.producto_costo = l.valor_total
                    self.cantidad = l.cantidad
                    self.forma_ingreso = 'M' if self.cantidad > 1 else 'I'

                    # Valores Contables
                    self.valor_contable = self.producto_costo
                    self.valor_residual = self.valor_contable * 0.1
                    self.valor_libros = self.valor_contable - self.valor_dep_acumulada

    # Validaciones para la vista

    @api.onchange('bodega_id')
    def _change_bodega(self):
        if self.bodega_id:
            self.tipo_respaldo_id = False

    @api.onchange('empleado_id')
    def _change_empleado(self):
        if self.empleado_id:
            if self.depreciacion == 'N':
                self.valor_mostrar = 6
            else:
                self.valor_mostrar = 5
            self.tipo_herencia = '2'

    @api.onchange('tip_comprobante')
    def _change_tip_comprobante(self):
        if self.tip_comprobante:
            if self.tip_comprobante != 'O':
                self.estado = 'B'

    @api.onchange('org_ingreso')
    def _change_org_ingreso(self):
        if self.org_ingreso:
            if self.org_ingreso != 'C':
                self.fecha_u_depreciacion = self.compra_id.fecha

                # valor aculumado iagual a ceroa
                self.valor_dep_acumulada = 0

    @api.onchange('vida_util_id')
    def _change_vida_util(self):
        if self.vida_util_id:
            self.vida_anios = self.vida_util_id.produccion
            self.valor_mostrar = 6

    # Bienes Muebles

    @api.onchange('bienes_muebles_id')
    def _onchange_lis_muebles(self):
        if self.bienes_muebles_id:
            for i, m in enumerate(self.bienes_muebles_id):
                m.dato_icorrecto = False
                if len(m.marca.strip()) < 2 or len(m.modelo.strip()) < 2 or len(m.serie.strip()) < 4 \
                        or len(m.color.strip()) < 4:
                    m.dato_icorrecto = True

    @api.onchange('bienes_muebles_id', 'duplicacion_datos')
    def _change_bienes_muebles(self):
        if self.duplicacion_datos:
            if len(self.bienes_muebles_id) >= self.cantidad:
                self.duplicacion_datos_catidad = True
            else:
                self.duplicacion_datos_catidad = False
        else:
            if len(self.bienes_muebles_id) >= 1:
                self.duplicacion_datos_catidad = True
                bien = self.bienes_muebles_id[0]
                self.bienes_muebles_id = False
                self.bienes_muebles_id = bien
            else:
                self.duplicacion_datos_catidad = False

    # Vehiculos
    @api.onchange('vehiculos_id')
    def _onchange_lis_vehiculos(self):
        if self.vehiculos_id:
            veh = self.vehiculos_id
            for i, h in enumerate(veh):
                h.dato_icorrecto = False
                if len(h.marca.strip()) < 2 or len(h.modelo.strip()) < 2 or len(h.serie.strip()) < 4 \
                        or len(h.n_motor.strip()) < 4 or len(h.n_chasis.strip()) < 4 or len(h.placa.strip()) < 7 \
                        or len(h.color_primerio.strip()) < 4:
                    h.dato_icorrecto = True

    @api.onchange('vehiculos_id', 'duplicacion_datos')
    def _change_bienes_vehiculos(self):
        if self.duplicacion_datos:
            if len(self.vehiculos_id) >= self.cantidad:
                self.duplicacion_datos_catidad = True
            else:
                self.duplicacion_datos_catidad = False
        else:
            if len(self.vehiculos_id) >= 1:
                self.duplicacion_datos_catidad = True
                bien = self.vehiculos_id[0]
                if (len(self.vehiculos_id) > 1):
                    self.vehiculos_id = False
                    self.vehiculos_id = bien
            else:
                self.duplicacion_datos_catidad = False

    @api.model
    def create(self, values):
        self.validar_herencia(values)
        if not values['duplicacion_datos']:
            return super(act.Cabacera, self).create(values)
        else:
            cantidad = values['cantidad']
            values['valor_contable'] = values['valor_contable'] / cantidad
            values['valor_residual'] = values['valor_residual'] / cantidad
            values['valor_libros'] = values['valor_libros'] / cantidad
            # valor acomulado
            values['cantidad'] = 1
            values['forma_ingreso'] = 'I'
            values['duplicacion_datos'] = False
            tipo = values['tipo_herencia']
            if tipo == '1':
                res = self.ingreso_bienes(values, 'bienes_muebles_id')
                return super(act.Cabacera, self).create(res)
            if tipo == '2':
                res = self.ingreso_bienes(values, 'vehiculos_id')
                return super(act.Cabacera, self).create(res)
            if tipo == '3':
                res = self.ingreso_bienes(values, 'inmueble_id')
                return super(act.Cabacera, self).create(res)
            if tipo == '4':
                res = self.ingreso_bienes(values, 'animal_vivo_id')
                return super(act.Cabacera, self).create(res)
            if tipo == '5':
                res = self.ingreso_bienes(values, 'bosques_plantas_id')
                return super(act.Cabacera, self).create(res)
            if tipo == '6':
                res = self.ingreso_bienes(values, 'pinacoteca_id')
                return super(act.Cabacera, self).create(res)
            if tipo == '7':
                res = self.ingreso_bienes(values, 'escultura_id')
                return super(act.Cabacera, self).create(res)
            if tipo == '8':
                res = self.ingreso_bienes(values, 'arqueologia_id')
                return super(act.Cabacera, self).create(res)
            if tipo == '9':
                res = self.ingreso_bienes(values, 'libros_colecciones_id')
                return super(act.Cabacera, self).create(res)

    def ingreso_bienes(self, values, tipo_bien):
        bienes = values[tipo_bien]
        for i, b in enumerate(bienes):
            values['codigo'] = compute_default_codigo(self, 5)
            values[tipo_bien] = [b]
            self.env['act.cabacera'].create(values)
            if i == (len(bienes) - 2):
                values['codigo'] = compute_default_codigo(self, 5)
                values[tipo_bien] = [bienes[-1]]
                return values

    def validar_herencia(self, values):
        tipo = values['tipo_herencia']
        if tipo == '1' and values.get('bienes_muebles_id') == None:
            raise ValidationError("Necesita ingresar Bienes muebles")
        if tipo == '2' and values.get('vehiculos_id') == None:
            raise ValidationError("Necesita ingresar Vehículo")
        if tipo == '3' and values.get('inmueble_id') == None:
            raise ValidationError("Necesita ingresar Inmuebles")
        if tipo == '4' and values.get('animal_vivo_id') == None:
            raise ValidationError("Necesita ingresar Animales Vivos")
        if tipo == '5' and values.get('bosques_plantas_id') == None:
            raise ValidationError("Necesita ingresar Bosques Plantas")
        if tipo == '6' and values.get('pinacoteca_id') == None:
            raise ValidationError("Necesita ingresar Pinacoteca")
        if tipo == '7' and values.get('escultura_id') == None:
            raise ValidationError("Necesita ingresar Esculturas")
        if tipo == '8' and values.get('arqueologia_id') == None:
            raise ValidationError("Necesita ingresar Arqueologia")
        if tipo == '9' and values.get('libros_colecciones_id') == None:
            raise ValidationError("Necesita ingresar Libros y Colecciones")

        dup = values['duplicacion_datos']
        can = values['cantidad']
        if dup and tipo == '1' and len(values['bienes_muebles_id']) < can:
            raise ValidationError("Necesita ingresar " + str(can) + " Bienes muebles")
        elif dup and tipo == '1' and len(values['bienes_muebles_id']) >= can:
            self.buscar_datos_erroneso(values['bienes_muebles_id'])
        elif not dup and tipo == '1':
            self.buscar_datos_erroneso(values['bienes_muebles_id'])

        if dup and tipo == '2' and len(values['vehiculos_id']) < can:
            raise ValidationError("Necesita ingresar " + str(can) + " Vehículo")
        elif dup and tipo == '2' and len(values['vehiculos_id']) >= can:
            self.buscar_datos_erroneso(values['vehiculos_id'])
        elif not dup and tipo == '2':
            self.buscar_datos_erroneso(values['vehiculos_id'])

        if dup and tipo == '3' and len(values['inmueble_id']) < can:
            raise ValidationError("Necesita ingresar " + str(can) + " Inmuebles")
        elif dup and tipo == '3' and len(values['inmueble_id']) >= can:
            self.buscar_datos_erroneso(values['inmueble_id'])
        elif not dup and tipo == '3':
            self.buscar_datos_erroneso(values['inmueble_id'])

        if dup and tipo == '4' and len(values['animal_vivo_id']) < can:
            raise ValidationError("Necesita ingresar " + str(can) + " Animales Vivos")
        elif dup and tipo == '4' and len(values['animal_vivo_id']) >= can:
            self.buscar_datos_erroneso(values['animal_vivo_id'])
        elif not dup and tipo == '4':
            self.buscar_datos_erroneso(values['animal_vivo_id'])

        if dup and tipo == '5' and len(values['bosques_plantas_id']) < can:
            raise ValidationError("Necesita ingresar " + str(can) + " Bosques Plantas")
        elif dup and tipo == '5' and len(values['bosques_plantas_id']) >= can:
            self.buscar_datos_erroneso(values['bosques_plantas_id'])
        elif not dup and tipo == '5':
            self.buscar_datos_erroneso(values['bosques_plantas_id'])

        if dup and tipo == '6' and len(values['pinacoteca_id']) < can:
            raise ValidationError("Necesita ingresar " + str(can) + " Pinacotecas")
        elif dup and tipo == '6' and len(values['pinacoteca_id']) >= can:
            self.buscar_datos_erroneso(values['pinacoteca_id'])
        elif not dup and tipo == '6':
            self.buscar_datos_erroneso(values['pinacoteca_id'])

        if dup and tipo == '7' and len(values['escultura_id']) < can:
            raise ValidationError("Necesita ingresar " + str(can) + " Esculturas")
        elif dup and tipo == '7' and len(values['escultura_id']) >= can:
            self.buscar_datos_erroneso(values['escultura_id'])
        elif not dup and tipo == '7':
            self.buscar_datos_erroneso(values['escultura_id'])

        if dup and tipo == '8' and len(values['arqueologia_id']) < can:
            raise ValidationError("Necesita ingresar " + str(can) + " Arqueologias")
        elif dup and tipo == '8' and len(values['arqueologia_id']) >= can:
            self.buscar_datos_erroneso(values['arqueologia_id'])
        elif not dup and tipo == '8':
            self.buscar_datos_erroneso(values['arqueologia_id'])

        if dup and tipo == '9' and len(values['libros_colecciones_id']) < can:
            raise ValidationError("Necesita ingresar " + str(can) + " Libros y Colecciones")
        elif dup and tipo == '9' and len(values['libros_colecciones_id']) >= can:
            self.buscar_datos_erroneso(values['libros_colecciones_id'])
        elif not dup and tipo == '9':
            self.buscar_datos_erroneso(values['libros_colecciones_id'])

    def buscar_datos_erroneso(self, bienes):
        for b in bienes:
            if b[2]['dato_icorrecto']:
                raise ValidationError("Corregir los Bienes Marcados en ROJO")
