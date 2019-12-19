# -*- coding: utf-8 -*-

from openerp import models, fields, api, osv


class RuleWizard(models.TransientModel):
    _name = "rule.wizard"

    # Modelos
    model1 = fields.Many2one(comodel_name='ir.model', string='Modelo 1')

    # Campos
    fields1 = fields.Many2one(comodel_name='ir.model.fields', string='Campo 1')

    # Operador entre los campos
    operator = fields.Many2one(comodel_name='operators', string='Operador 1')

    # Campo 1 de la restricción 1
    value1 = fields.Char()

    date_value = fields.Date(
        string='Date',
        required=False)

    date_time_value = fields.Datetime(
        string='Date_time_value',
        required=False)

    integer_value = fields.Integer(
        string='integer_value',
        required=False)

    bool_value = fields.Boolean(
        string='Bool_value',
        required=False)

    char_value = fields.Char(
        string='Char_value',
        required=False)

    float_value = fields.Float(
        string='Float_value',
        required=False)

    @api.onchange('fields1')
    def onchange_method(self):
        self.value1 = self.fields1.ttype

    @api.multi
    def create_rule(
            self):  # para crear la regla, necesito recibir en el context el generator id para le realcion entre many2one
        context = self.env.context
        if context and context.get('generator_id', False):
            generator_id = context.get('generator_id')
            generator_id = int(generator_id)
            name = self.model1.model + ', ' + self.fields1.name + ', ' + self.operator.symbol + ', ' + self.value1
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

            name = self.model1.model + ', ' + self.fields1.name + ', ' + self.operator.symbol + ', ' + self.value1
            self.env['string.converter'].browse(stringconverter).write({'name': name})


class BinaryOperatorWizard(models.TransientModel):
    _name = "binary.operator.wizard"

    # Operator
    operator = fields.Many2one(comodel_name='binary.operators', string='Operador')

    # TODO Refactorizar la función de create y de converter
    @api.multi
    def create_operator(
            self):  # para crear la regla, necesito recibir en el context el generator id para le realcion entre many2one
        context = self.env.context
        if context and context.get('generator_id', False):
            generator_id = context.get('generator_id')
            generator_id = int(generator_id)
            symbol = self.operator.symbol
            self.env['string.converter'].create({
                'generator_id': generator_id,
                'name': symbol,
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
