# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

from odoo import api, fields, models

def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class BosquesPlantas(models.Model):
    _name = 'act.bos.bosquesplantas'
    _description = 'Activos - Bienes - Bosques Plantas'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo del Bosques y Plantas')

    ideftificacion = fields.Char('Identificación', required=True, help='Identificación del Bien')
    caratesiticas_unicas = fields.Char('Características únicas', required=True, help='Características unicas')
    raza = fields.Char('Raza | Otros', required=True, help='Raza / Otros')


    tipo_cultivo_id = fields.Many2one('act.bos.tipocultivo', string='Tipo Cultivo', required=True, help='Tipo cultivo')
    fecha_siembra = fields.Date('Fecha de Siembra', required = False, help='Fecha de Siembra de planta')
    aera_siembra = fields.Float('Área de Siembra m2',digits=(6,2), required=True, help='Área de Siembra m2')
    finalidad_cultivo = fields.Selection( [('C','Comercio'),('E','Explotación'),('O','Otros')], string='Finalidad del cultivo', required = True, help='Finalidad del cultivo')

    dato_icorrecto = fields.Boolean("Dato Icorrecto", default=False)



class TipoCultivo(models.Model):
    _name = 'act.bos.tipocultivo'
    _description = 'Activos - Bienes - Bosques Plantas - Tipo Cultivo'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo Tipo de cultivo')
    tipo = fields.Char('Tipo', required=True, help='Tipo de Cultivo')
    descripcion = fields.Char('Descripcion', required=True, help='Descripcion de la Clase vehiculo')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.tipo)))
        return result


