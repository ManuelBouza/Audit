# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Generator(models.Model):
    _name = 'generator'

    stringConverter = fields.One2many(comodel_name='string.converter', inverse_name='generator_id', string='Regla')

    @api.multi
    def validate_rule(self):

        pass
        # tables = self.model1.model
        # tables = tables.split(".")
        # tables = "_".join(tables)
        #
        # query ="SELECT * FROM " + tables
        #
        # self.env.cr.execute(query)
        # result = self.env.cr.dictfetchall()

    @api.multi
    def add_rule(self):
        # stringConverter = self.env['string.converter'].create({'generator_id':self.id,'name':'hytg'})

        self.ensure_one() # asegurarce que solo sea un solo record del modelo.
        wiz = self.env['rule.wizard'].create({}) #Creando lo que va ha mostrar el wiard
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rule.wizard',
            'res_id': wiz.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'generator_id': self.id},
            'nodestroy': True,
        }

    @api.multi
    def add_operator(self):

        wiz = self.env['binary.operator.wizard'].create({}) #Creando lo que va ha mostrar el wiard
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'binary.operator.wizard',
            'res_id': wiz.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'generator_id': self.id},
            'nodestroy': True,
        }
        pass


class Operators(models.Model):
    _name = 'operators'

    name = fields.Char(string='Nombre')
    symbol = fields.Char(string='Símbolo')

class BinaryOperators(models.Model):
    _name = 'binary.operators'

    name = fields.Char(string='Nombre')
    symbol = fields.Char(string='Símbolo')

class stringConverter(models.Model):
    _name = 'string.converter'
    _order = 'sequence'

    generator_id = fields.Many2one(comodel_name='generator', required=True, ondelete='cascade')
    name = fields.Char(string='Nombre')
    sequence =fields.Integer('Secuencia', default=0)
    is_rule = fields.Boolean(string='Is_rule', default='True')

    @api.multi
    def edit(self):
        is_rule = self.is_rule

        if is_rule:
            name = self.name
            split = name.split(', ')
            model = split[0]
            model = self.env['ir.model'].search([('model','=',model)], limit=1)
            if model:
                fields = split[1]
                fields = self.env['ir.model.fields'].search([('model_id', '=', model.id),('name','=',fields)], limit=1)
                operator = split[2]
                operator = self.env['operators'].search([('symbol', '=', operator)], limit=1)
                value1 = split[3]
                self.ensure_one()
                wiz = self.env['rule.wizard'].create({'model1':model.id,
                                                      'fields1':fields.id,
                                                      'operator':operator.id,
                                                      'value1':value1})
                return {
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'rule.wizard',
                    'res_id': wiz.id,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'generator_id': False, 'stringconverter':self.id},
                    'nodestroy': True,
                }
        else:
            import sys
            binary_operator = self.name
            binary_operator = self.env['binary.operators'].search([('symbol', '=', binary_operator)], limit=1)
            if binary_operator:
                wiz = self.env['binary.operator.wizard'].create({'operator': binary_operator.id})

                return {
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'binary.operator.wizard',
                    'res_id': wiz.id,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'generator_id': False, 'stringconverter': self.id},
                    'nodestroy': True,
                }


