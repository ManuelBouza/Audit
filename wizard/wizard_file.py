# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Akretion (<http://www.akretion.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, osv


class RuleWizard(models.TransientModel):
    _name = "rule.wizard"

    # Modelos
    model1 = fields.Many2one(comodel_name='ir.model', string='Modelo 1')

    # Campos
    fields1 = fields.Many2one(comodel_name='ir.model.fields', string='Campo 1')

    # Operador entre los campos
    operator = fields.Many2one(comodel_name='operators', string='Operador 1')

    # Campo 1 de la restriccion 1
    value1 = fields.Char(string="Valor 1")


    @api.multi
    def create_rule(self):  #para crear la regla, necesito recibir en el context el generator id para le realcion entre many2one
        context = self.env.context
        if context and context.get('generator_id', False):
            generator_id = context.get('generator_id')
            generator_id = int(generator_id)
            name = self.model1.model+' - '+self.fields1.name + ' ' + self.operator.symbol+ ' '+ self.value1
            self.env['string.converter'].create({
                'generator_id': generator_id,
                'name': name,
                'is_rule': True,
            })
        return True

    @api.multi
    def edit_rule(self):
        context = self.env.context
        if context and context.get('stringconverter', False):
            stringconverter = context.get('stringconverter')
            stringconverter = int(stringconverter)

            name = self.model1.model + ' - ' + self.fields1.name + ' ' + self.operator.symbol + ' ' + self.value1
            self.env['string.converter'].browse(stringconverter).write({'name': name})

class BinaryOperatorWizard(models.TransientModel):
    _name = "binary.operator.wizard"

    # Operator
    operator = fields.Many2one(comodel_name='binary.operators', string='Operador')

    @api.multi
    def create_operator(self):  #para crear la regla, necesito recibir en el context el generator id para le realcion entre many2one
        context = self.env.context
        if context and context.get('generator_id', False):
            generator_id = context.get('generator_id')
            generator_id = int(generator_id)
            symbol = self.operator.symbol
            self.env['string.converter'].create({
                'generator_id': generator_id,
                'symbol': symbol,
                'is_rule': False,
            })
        return True

    @api.multi
    def edit_operator(self):
        context = self.env.context
        if context and context.get('stringconverter', False):
            stringconverter = context.get('stringconverter')
            stringconverter = int(stringconverter)

            symbol = self.operator.symbol
            self.env['string.converter'].browse(stringconverter).write({'name': symbol})