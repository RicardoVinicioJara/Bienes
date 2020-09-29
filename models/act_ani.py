# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

from odoo import api, fields, models

def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class AnimalVivo(models.Model):
    _name = 'act.ani.animalvivo'
    _description = 'Activos - Bienes - Aminam Vivo'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo de Animal Vivo')

    serie = fields.Char('Identificación', required=True, help='Serie del Bien')
    modelo = fields.Char('Características únicas', required=True, help='Modelo del Bien')
    marca = fields.Char('Raza', required=True, help='Marca del bien')

    sexo = fields.Selection([('M', 'Macho'),('H','Hembra')], required=True, string='Sexo', help='Sexo del animal')
    fecha_nacimineto = fields.Date('Fecha nacimiento', required = False, help='Fecha de nacimiento del animal')
    edad = fields.Char('Edad', required = True, help='Edad')
    peso = fields.Float('Peso',digits=(6,2), required=False, help='Peso')
    num_arete = fields.Char('Número de arete', required = True, help='Numero de arete')

    dato_icorrecto = fields.Boolean("Dato Icorrecto", default=False)


