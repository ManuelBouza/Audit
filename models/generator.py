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

        self.ensure_one()
        wiz = self.env['rule.wizard'].create({})
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
        pass

class Operators(models.Model):
    _name = 'operators'

    name = fields.Char(string='Nombre')
    symbol = fields.Char(string='Símbolo')

class OperatorsBinary(models.Model):
    _name = 'operators.binary'

    name = fields.Char(string='Nombre')
    symbol = fields.Char(string='Símbolo')

class stringConverter(models.Model):
    _name = 'string.converter'
    _order = 'sequence'

    @api.model
    def _get_groups(self):
        return [('a','Grupo A'),('b','Grupo B')]

    generator_id = fields.Many2one(comodel_name='generator')
    name = fields.Char(string='Nombre')
    sequence =fields.Integer('Secuencia', default=0)
    operator_binary = fields.Many2one(comodel_name='operators.binary', string='Operador')
    group= fields.Selection('_get_groups', string='Grupo')

    @api.multi
    def edit_rule(self):
        name = self.name
        split = name.split(' ')
        model = split[0]
        model = self.env['ir.model'].search([('model','=',model)], limit=1)
        if model:
            fields = split[2]
            fields = self.env['ir.model.fields'].search([('model_id', '=', model.id),('name','=',fields)], limit=1)
            operator = split[3]
            operator = self.env['operators'].search([('symbol', '=', operator)], limit=1)
            value1 = split[4]
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
        pass