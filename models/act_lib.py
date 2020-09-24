# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

from odoo import api, fields, models

def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class LibrosColecciones(models.Model):
    _name = 'act.lib.libroscolecciones'
    _description = 'Activos - Bienes - Libros Coleccione'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=20,  default=lambda self: compute_default_codigo(self, 3), help='Codigo del Detalle')

    serie = fields.Char('Serie', required=True, help='Serie del Bien')
    modelo = fields.Char('Modelo', required=True, help='Modelo del Bien')
    marca = fields.Char('Marca', required=True, help='Marca del bien')


    titulo = fields.Char('Título de la Obra', required = True, help='Título de la Obra')
    autor_id = fields.Many2one('act.pin.autor', string='Autor', required = True, help='Autor de la obra')
    editorial_id = fields.Many2one('act.lib.editorial', string='Editorial', required = True, help='Editorial')
    fecha_edicion = fields.Date('Fecha Edición', required= True, help='Fecha Edición')
    num_edicion = fields.Integer('Numero Edición', required = True, help='Numero de Edición')
    clasifiacion_biografia = fields.Many2one('act.lib.clasifiacionbiografia', string='Clasificación Bibliográfica', required = False, help='Clasificación Bibliográfica')


class Editorial(models.Model):
    _name = 'act.lib.editorial'
    _description = 'Activos - Bienes - Editorial'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo')
    nombre = fields.Char('Nombre', required = True, help='Nombre del la editorial')
    datelles = fields.Char('Detalles',  required = False, help='Detalles de la editorial')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.nombre)))
        return result


class ClasifiacionBiografia(models.Model):
    _name = 'act.lib.clasifiacionbiografia'
    _description = 'Activos - Bienes - Clasificación Bibliográfica'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo')
    clasificacion = fields.Char('Clasificación', required = True, help='Clasificación')
    Bibliografica = fields.Char('Bibliográfica', required = False, help='Bibliográfica  ')
    detales = fields.Char('Detalles', required = False, help='Datalles')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.clasificacion) + " | " + str(record.Bibliografica) ))
        return result


