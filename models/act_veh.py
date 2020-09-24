# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import date


def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class Vehiculos(models.Model):
    _name = 'act.veh.vehiculos'
    _description = 'Activos - Bienes - Hehiculos'
    # _rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self, 5),
                         help='Codigo del Vehiculo')

    serie = fields.Char('Serie', required=True, help='Serie del Bien')
    modelo = fields.Char('Modelo', required=True, help='Modelo del Bien')
    marca = fields.Char('Marca', required=True, help='Marca del bien')

    tipo_vehiculo_id = fields.Many2one('act.veh.vehiculostipo', string='Tipo', required=True, help='Tipo de vehiculo')
    clase_vehiculo_id = fields.Many2one('act.veh.vehiculosclase', string='Clase', required=True,
                                        help='Clase de vehiculo')
    n_motor = fields.Char('Número Motor', required=True, help='Número de Motor')
    n_chasis = fields.Char('Número Chasis', required=True, help='Número de Chasis')

    anio_fabricacion = fields.Selection('get_years', string='Año de Fabricación', required=True,
                                        help='Año de Fabricación', )

    placa = fields.Char('Placa', required=True, help='Placa')
    color_primerio = fields.Char('Color primario', required=True, help='Color primario')
    color_secundario = fields.Char('Color secundario', required=False, help='Color Secundario')

    dato_icorrecto = fields.Boolean("Dato Icorrecto", default=False)

    def get_years(self):
        year_list = []
        for i in range(date.today().year, 1950, -1):
            year_list.append((str(i), str(i)))
        return year_list



class VehiculosClase(models.Model):
    _name = 'act.veh.vehiculosclase'
    _description = 'Activos - Bienes - Hehiculos - Clase'
    # _rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self, 4),
                         help='Codigo vehiculo Clase')
    tipo = fields.Char('Tipo', required=True, help='Tipo')
    descripcion = fields.Char('Descripcion', required=True, help='Descripcion de la Clase vehiculo')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.tipo) + " | " + str(record.descripcion)))
        return result


class VehiculosTipo(models.Model):
    _name = 'act.veh.vehiculostipo'
    _description = 'Activos - Bienes - Hehiculos - Tipo'
    # _rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self, 4),
                         help='Codigo Tipo de vehiculo')
    tipo = fields.Char('Tipo', required=True, help='Tipo')
    descripcion = fields.Char('Descripcion', required=True, help='Descripcion del tipo de vehiculo')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.tipo) + " | " + str(record.descripcion)))
        return result
