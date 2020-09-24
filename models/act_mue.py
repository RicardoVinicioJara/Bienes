# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

from odoo import api, fields, models

def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class BienesMuebles(models.Model):
    _name = 'act.mue.bienesmuebles'
    _description = 'Activos - Bienes - Muebles'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Código')

    serie = fields.Char('Serie', required=True, help='Serie del Bien')
    modelo = fields.Char('Modelo', required=True, help='Modelo del Bien')
    marca = fields.Char('Marca', required=True, help='Marca del bien')

    material_id = fields.Many2one('act.mue.material', string='Material', required=False, size=20, help='Material del Bien')
    color = fields.Char('Color', required=True, help='Color')
    largo = fields.Float('Largo', required=False, digist=(6,2), help='Dimensiones | Largo')
    ancho = fields.Float('Ancho', required=False, digist=(6,2), help='Dimensiones | Ancho')

    dato_icorrecto = fields.Boolean("Dato Icorrecto", default=False)


class Material(models.Model):
    _name = 'act.mue.material'
    _description = 'Activos - Bienes - Muebles - Materia'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo del Detalle')
    material = fields.Char('Material', required=True, help='Material')
    descripcion = fields.Char('Descripcion', required=True, help='Descripcion del tipo de vehiculo')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.material + ' | ' + record.descripcion ))
        return result


