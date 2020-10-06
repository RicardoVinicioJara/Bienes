# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

from odoo import api, fields, models
from datetime import date


def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class AnimalVivo(models.Model):
    _name = 'act.ani.animalvivo'
    _description = 'Activos - Bienes - Aminam Vivo'
    # _rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self, 4),
                         help='Codigo de Animal Vivo')

    ideftificacion = fields.Char('Identificación', required=True, help='Identificación del Bien')
    caratesiticas_unicas = fields.Char('Características únicas', required=True, help='Características unicas')
    raza = fields.Many2one('act.ani.raza', string='Raza', required=True, help='Raza del animal')

    sexo = fields.Selection([('M', 'Macho'), ('H', 'Hembra')], required=True, string='Sexo', help='Sexo del animal')
    fecha_nacimineto = fields.Date('Fecha nacimiento', required=False, help='Fecha de nacimiento del animal')
    edad = fields.Char('Edad | AÑOS', required=True, help='Edad | AÑOS')
    peso = fields.Float('Peso', digits=(6, 2), required=False, help='Peso')
    num_arete = fields.Char('Número de arete', required=True, help='Numero de arete')

    dato_icorrecto = fields.Boolean("Dato Icorrecto", default=False)

    @api.onchange('fecha_nacimineto')
    def _calcular_edad(self):
        if self.fecha_nacimineto:
            fecha_actual = date.today()
            self.edad = fecha_actual.year - self.fecha_nacimineto.year - ((fecha_actual.month, fecha_actual.day) <
                                                                          (self.fecha_nacimineto.month,
                                                                           self.fecha_nacimineto.day))


class Raza(models.Model):
    _name = 'act.ani.raza'
    _description = 'Activos - Bienes - Aminam Vivo - Raza'
    # _rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self, 4),
                         help='Codigo del Raza')
    raza = fields.Char('Raza', required=True, help='Raza')
    descripcion = fields.Char('Descripcion', required=True, help='Descripcion de la Raza')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.raza))
        return result
