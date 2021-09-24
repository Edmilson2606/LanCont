from django.contrib import admin

from .models import Clientes, Debitos, Creditos, Historicos, Lancamentos


class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'contato')


class DebitosAdmin(admin.ModelAdmin):
    list_display = ('codigo_reduzido', 'descricao')


class CreditosAdmin(admin.ModelAdmin):
    list_display = ('codigo_reduzido', 'descricao')


class HistoricosAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao')


class LancamentosAdmin(admin.ModelAdmin):
    list_display = ('data_lancamento', 'id_conta_debito_id', 'id_conta_credito_id',
                    'valor', 'id_historico_id', 'compl_historico', 'id_cliente_id')


admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Debitos, DebitosAdmin)
admin.site.register(Creditos, CreditosAdmin)
admin.site.register(Historicos, HistoricosAdmin)
admin.site.register(Lancamentos, LancamentosAdmin)
