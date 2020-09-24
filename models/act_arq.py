# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

from odoo import api, fields, models

def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class Arqueologia(models.Model):
    _name = 'act.arq.arqueologia'
    _description = 'Activos - Bienes - Arqueología'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo Arqueologia')

    serie = fields.Char('Serie', required=True, help='Serie del Bien')
    modelo = fields.Char('Modelo', required=True, help='Modelo del Bien')
    marca = fields.Char('Marca', required=True, help='Marca del bien')


    nombre = fields.Char('Nombre de la Obra', required = True, help='Nombre de la Obra')
    ubicacion = fields.Many2one('act.inm.direccion', string='Ubicación Física', required = True, help='Ubicación Física ')
    precedencia = fields.Char('Procedencia', required= True, help='Procedencia')
    material_id = fields.Many2one('act.esc.material', string='Material', required = True, help='Material')
    cultura_id = fields.Many2one('act.arq.cultura', string='Cultura', required = False, help='Cultura')
    ancho = fields.Float('Ancho',digits=(6,2), required=False)
    largo = fields.Float('Largo',digits=(6,2), required=False)
    marfologia_id = fields.Many2one('act.arq.marfologia', string='Morfología', required = False, help='Morfología')
    tenicnicaselb_id = fields.Many2one('act.arq.tecnicaselaboracion', string='Técnicas de Elaboración', required = True, help=' Técnicas de Elaboración')
    decoracion_id = fields.Many2one('act.pin.tecnicasdecorativas', string='Técnicas Decorativas', required = False, help='Decoración')
    porcetaje_integridad = fields.Float('Porcetaje de Integridad',digits=(3,2), required=False, help='Porcetaje de Integridad')
    porcentaje_conservacion = fields.Float('Porcetaje de conservación',digits=(3,2), required=False, help='Porcetaje de conservación ')


class Cultura(models.Model):
    _name = 'act.arq.cultura'
    _description = 'Activos - Bienes - Arqueologia -Cultura'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo')
    cultura = fields.Char('Cultura', required = True, help='Cultura del sistio arqueologico ')
    decripcion = fields.Char('Descripción', required = False, help='Descripción  ')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.cultura)))
        return result


class Marfologia(models.Model):
    _name = 'act.arq.marfologia'
    _description = 'Activos - Bienes - Arqueologia -Marfologia'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo')
    marfologia = fields.Char('Morfología', required = True, help='Morfología')
    decripcion = fields.Char('Descripción', required = False, help='Descripción  ')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.marfologia) + " | " + str(record.decripcion)))
        return result



class TecnicasElaboracion(models.Model):
    _name = 'act.arq.tecnicaselaboracion'
    _description = 'Activos - Bienes - Arqueologia -Técnicas de Elaboración'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo')
    tecnicas_elaboracion = fields.Char('Técnicas de Elaboración', required = True, help='Técnicas de Elaboración')
    decripcion = fields.Char('Descripción', required = False, help='Descripción  ')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.tecnicas_elaboracion) + " | " + str(record.decripcion)))
        return result


