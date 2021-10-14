from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader

from .models import Clientes
from .models import Debitos
from .models import Creditos
from .models import Historicos
from .models import Lancamentos
from .forms import LancamentosModelForm

import csv

from datetime import date
from datetime import datetime

identificacao = 0


def index(request):
    if str(request.user) != 'AnonymousUser':
        usuario = request.user.first_name
        clientes = Clientes.objects.all()
        context = {
            'logado': usuario,
            'acesso': 'Sair',
            'titulo1': 'Aécia Contabilidade',
            'titulo2': 'Lançamentos Contabeis',
            'titulo3': 'C L I E N T E S',
            'cabecalho1': 'Nome',
            'cabecalho2': 'Contato',
            'clientes': clientes,
        }
        return render(request, 'index.html', context)
    else:
        context = {
            'acesso': 'Entrar',
            'titulo1': 'Aécia Contabilidade',
            'titulo2': 'Lançamentos Contabeis',
        }
        return render(request, 'index.html', context)


def cliente(request, pk):
    usuario = request.user.first_name
    cli = Clientes.objects.get(id=pk)
    lanc = Lancamentos.objects.all()
    global identificacao
    identificacao = cli.id
    lanca = [lan for lan in lanc if lan.id_cliente_id == cli.id]
    context = {
        'logado': usuario,
        'cliente': cli,
        'lancamento': lanca,
    }
    return render(request, 'cliente.html', context)


def lancamentos(request):
    usuario = request.user.first_name
    if str(request.method) == 'POST':
        form = LancamentosModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lançamento salvo com sucesso')
            form = LancamentosModelForm()
        else:
            messages.error(request, 'Erro ao salvar o Lançamento')
    else:
        form = LancamentosModelForm()
    context = {
        'logado': usuario,
        'form': form,
    }
    return render(request, 'lancamentos.html', context)


def erro500():
    template = loader.get_template('500.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8')


def geracsv(request):
    if str(request.method) == 'POST':
        lanc = Lancamentos.objects.all()
        lanca = [lan for lan in lanc if lan.id_cliente_id == identificacao]
        if len(lanca) > 0:
            debitos = Debitos.objects.all()
            creditos = Creditos.objects.all()
            historicos = Historicos.objects.all()
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="lancamentos_contabeis.csv"'}
                                    )
            writer = csv.writer(response)
            writer.writerow([f"Tipo Registro;Data;Código da Conta Débito;Código da Conta Crédito;Valor;"
                             f"Histórico;Código do Estabelecimento Débito;Código do Centro de Resultado Débito;"
                             f"Código do Estabelecimento Crédito;Código do Centro de Resultado Crédito"])
            for lan in lanca:
                tipo = '1'
                deb = 0
                cred = 0
                hist = 0
                for debito in debitos:
                    if lan.id_conta_debito_id == debito.id:
                        deb = debito.codigo_reduzido
                        break
                for credito in creditos:
                    if lan.id_conta_credito_id == credito.id:
                        cred = credito.codigo_reduzido
                        break
                for historico in historicos:
                    if lan.id_historico_id == historico.id:
                        hist = historico.descricao
                        break
                writer.writerow([f'{tipo};{date_para_str(lan.data_lancamento)};{deb};{cred};'
                                 f'{formata_float_str_moeda(lan.valor)};{hist} {lan.compl_historico};'
                                 f'{lan.ced};{lan.ccrd};{lan.cec};{lan.ccrc}'])
            return response
        return messages.error(request, 'Erro ao gerar o arquivo'), exit(0)


def date_para_str(data: date) -> str:
    return data.strftime('%d/%m/%Y')


def str_para_date(data: str) -> date:
    return datetime.strptime(data, '%d/%m/%Y')


def formata_float_str_moeda(valor: float) -> str:
    val = f'{valor:-.2f}'
    val = val.replace('.', ',').replace('-', '.')
    return val
