from django import forms
from .models import Lancamentos


class LancamentosModelForm(forms.ModelForm):

    class Meta:
        model = Lancamentos
        fields = ['data_lancamento', 'id_conta_debito', 'id_conta_credito', 'valor',
                  'id_historico', 'compl_historico', 'id_cliente']
