# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################

from odoo import api, fields, models

def compute_default_codigo(self, tam):
    listado = self.env[self._name].search([])
    numero = str(int(listado[-1].codigo if listado else '0') + 1)
    return numero.zfill(tam)


class Pinacoteca(models.Model):
    _name = 'act.pin.pinacoteca'
    _description = 'Activos - Bienes - Pinacoteca'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo del Detalle')

    serie = fields.Char('Serie', required=True, help='Serie del Bien')
    modelo = fields.Char('Modelo', required=True, help='Modelo del Bien')
    marca = fields.Char('Marca', required=True, help='Marca del bien')


    nombre = fields.Char('Nombre de la obra', required = True, help='Nombre de la obra')
    epoca_id = fields.Many2one('act.pin.epoca', string='Epoca', required = True, help='Epoca de la obra')
    pintura_id = fields.Many2one('act.pin.pintura', string='Pintura', required = True, help='Tipo  de la pintura')
    autor_id = fields.Many2one('act.pin.autor', string='Autor', required = True, help='Autor de la obra')
    ancho = fields.Float('Ancho de la obra',digits=(6,2), required=True)
    largo = fields.Float('Largo de la obra',digits=(6,2), required=True)
    artes_menores = fields.Many2one('act.pin.artesmenores', string='Artes Menores', required = True, help='Artes menores de la obra')
    tecnicas_id = fields.Many2one('act.pin.tecnicasdecorativas', string='Técnicas Decorativas', required = True, help='Técnicas Decorativas')
    procedencia = fields.Char('Procedencia', required= True, help='Procedencia')
    estado_conservacion = fields.Many2one('act.pin.conservacion', string='Estado de Conservación', required = True, help='Estado de Conservación')
    estado_integridad = fields.Many2one('act.pin.integridad', string='Estado de Integridad', required = True, help='Estado de Integridad')

    dato_icorrecto = fields.Boolean("Dato Icorrecto", default=False)


class Epoca(models.Model):
    _name = 'act.pin.epoca'
    _description = 'Activos - Bienes - Pinacoteca -Epoca'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Código Epoca')
    siglo = fields.Char('Siglo', required = True, help='Siglo en numero romanos')
    decripcion = fields.Char('Descripción', required = False, help='Descripción ')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.siglo)))
        return result


class Pintura(models.Model):
    _name = 'act.pin.pintura'
    _description = 'Activos - Bienes - Pinacoteca -Pintura'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Código Pintura')
    pintura = fields.Char('Pintura', required = True, help='Pintura de la obra')
    decripcion = fields.Char('Descripción', required = False, help='Descripción')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.pintura) + " | " + str(record.decripcion)))
        return result



class Estilo(models.Model):
    _name = 'act.pin.estilo'
    _description = 'Activos - Bienes - Pinacoteca -Estilo'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo')
    estilo = fields.Char('Estilo', required = True, help='Estilo de la obra')
    decripcion = fields.Char('Descripción', required = False, help='Descripción')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.estilo)))
        return result


class ArtesMenores(models.Model):
    _name = 'act.pin.artesmenores'
    _description = 'Activos - Bienes - Pinacoteca -Artes Menores'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Código Artes Menores')
    artes = fields.Char('Artes Menores', required = True, help='Artes menores de la obra')
    decripcion = fields.Char('Descripción', required = False, help='Descripción  ')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.artes) + " | " + str(record.decripcion)))
        return result


class TecnicasDecorativas(models.Model):
    _name = 'act.pin.tecnicasdecorativas'
    _description = 'Activos - Bienes - Pinacoteca -Técnicas Decorativas'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Código Técnicas Decorativas')
    tecnicas = fields.Char('Técnicas Decorativas', required = True, help='Técnicas Decorativas')
    decripcion = fields.Char('Descripción', required = False, help='Descripción  ')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.tecnicas) + " | " + str(record.decripcion)))
        return result


class Conservacion(models.Model):
    _name = 'act.pin.conservacion'
    _description = 'Activos - Bienes - Pinacoteca -Estado de Conservación'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Código Conservacion')
    estado = fields.Char('Estado de Conservación', required = True, help='Estado de Conservación')
    decripcion = fields.Char('Descripción', required = False, help='Descripción  ')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.estado) + " | " + str(record.decripcion)))
        return result


class Integridad(models.Model):
    _name = 'act.pin.integridad'
    _description = 'Activos - Bienes - Pinacoteca -Estado de Integridad'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Código Itegridad')
    estado = fields.Char('Estado de Integridad', required = True, help='Estado de Integridad')
    decripcion = fields.Char('Descripción', required = False, help='Descripción  ')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.estado) + " | " + str(record.decripcion)))
        return result


class Autor(models.Model):
    _name = 'act.pin.autor'
    _description = 'Activos - Bienes - Autor'
    #_rec_name = ''
    codigo = fields.Char('Código', required=True, size=4, default=lambda self: compute_default_codigo(self,4) , help='Codigo')
    nombres = fields.Char('Nombres', required = True, help='Nombres del autor')
    apellidos = fields.Char('Apellidos', required = False, help='Apellidos del autor  ')
    genero = fields.Selection([('f', 'FEMENINO'), ('m', 'MASCULINO'), ('LGBT', 'LGBT')], 'Genero', required=True, help='Genero del autor')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, str(record.apellidos) + " " + str(record.nombres)))
        return result


