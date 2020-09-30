# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

from odoo import api, fields, models

def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class Escultura(models.Model):
    _name = 'act.esc.escultura'
    _description = 'Activos - Bienes - Escultura'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo del Detalle')

    serie = fields.Char('Serie', required=True, help='Serie del Bien')
    caratesiticas_unicas = fields.Char('Características únicas', required=True, help='Características unicas')
    marca = fields.Char('Marca', required=True, help='Marca del bien')

    registro = fields.Char('Registro Patrimonial', required = True, help='Registro Patrimonial')
    titulo = fields.Char('Especificación y Título', required= False, help='Especificación y Título')
    epoca_id = fields.Many2one('act.pin.epoca', string='Epoca', required = True, help='Epoca de la obra')
    autor_id = fields.Many2one('act.pin.autor', string='Autor', required = True, help='Autor de la obra')
    material_id = fields.Many2one('act.esc.material', string='Material de la escultura', required = True, help='Material de la escultura')
    tecnicas_id = fields.Many2one('act.pin.tecnicasdecorativas', string='Técnicas Decorativas', required = True, help='Técnicas Decorativas')
    ancho = fields.Float('Ancho de la obra',digits=(6,2), required=False)
    largo = fields.Float('Largo de la obra',digits=(6,2), required=False)
    inscripciones = fields.Char('Inscripciones', required=False, help='Inscripciones')
    fecha_realizacion = fields.Date('Fecha de realización', required=False, help='Fecha de realización')
    fecha_procedencia = fields.Date('Fecha de requisición o procedencia', required= False, help='Fecha de requisición o procedencia')

    dato_icorrecto = fields.Boolean("Dato Icorrecto", default=False)


class Material(models.Model):
    _name = 'act.esc.material'
    _description = 'Activos - Bienes - Escultura -Material'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo Material Escultura')
    material = fields.Char('Material de la escultura', required = True, help='Material de la escultura')
    decripcion = fields.Char('Descripción', required = False, help='Descripción  ')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.material)))
        return result


