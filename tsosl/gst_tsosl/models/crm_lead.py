# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    x_studio_descuento_1 = fields.Float("Descuento")
    x_studio_precio_final_de_venta = fields.Float('Precio Final de Venta', compute="_compute_final_price", store=True)

    @api.onchange('x_studio_descuento_1')
    def onchange_discount(self):
        res = {}
        if self.x_studio_descuento_1 > 0.20:
            res['warning'] = {'title': _('Warning'), 'message': _('Discount greater than 20% not allowed.')}
            self.x_studio_descuento_1 = 0
            return res

    @api.depends('x_studio_descuento_1', 'x_studio_tarifa_plana_ee_pvp_1')
    def _compute_final_price(self):
        for lead in self:
            lead.x_studio_precio_final_de_venta = lead.x_studio_tarifa_plana_ee_pvp_1 * (1 - lead.x_studio_descuento_1)
