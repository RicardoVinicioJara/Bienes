# -*- coding: utf-8 -*-
##############################################################################
#   SICAF - Copyright  2019
##############################################################################
{
    'name': 'Bienes',
    'version': '0.1',
    'author': 'SICAF',
    'website': 'http://www.sicaf.com.ec',
    'category': 'Contabilidad - Auditoria',
    'sequence': 15,
    'summary': 'Sistema Informatico Contabilidad Auditoria Financiero',
    'description': """ SICAF - Sistema Informatico Contabilidad Auditoria Financiero """,
    'depends': ['base', 'compras', 'gestion_administrativa', 'presupuesto', 'rrhh_nomina','presupuesto'],
    'data': ['security/ir.model.access.csv', 'views/act_menu.xml', 'views/act_veh_view.xml', 'views/act_arq_view.xml',
             'views/act_bos_view.xml', 'views/act_mue_view.xml', 'views/act_ani_view.xml', 'views/act_lib_view.xml',
             'views/act_inm_view.xml', 'views/act_view.xml', 'views/act_pin_view.xml', 'views/act_esc_view.xml'],
    'demo': [],
    'js': ['static/src/js/Bienes.js','static/src/js/toastify.js'],
    'css': ['static/src/less/toastify.css'],
    'update_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
