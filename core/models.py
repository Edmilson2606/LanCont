from django.db import models


class Clientes(models.Model):
    nome = models.CharField('Nome', max_length=200)
    contato = models.CharField('Contato', max_length=100)

    def __str__(self):
        return self.nome


class Debitos(models.Model):
    codigo_reduzido = models.IntegerField('Codigo Reduzido')
    descricao = models.CharField('Descrição', max_length=200)

    def __str__(self):
        return f'{self.codigo_reduzido} {self.descricao}'


class Creditos(models.Model):
    codigo_reduzido = models.IntegerField('Codigo Reduzido')
    descricao = models.CharField('Descrição', max_length=200)

    def __str__(self):
        return f'{self.codigo_reduzido} {self.descricao}'


class Historicos(models.Model):
    descricao = models.CharField('Descrição', max_length=200)

    def __str__(self):
        return self.descricao


class Lancamentos(models.Model):
    data_lancamento = models.DateField('Data')
    id_conta_debito = models.ForeignKey('core.Debitos', verbose_name='Conta Débito', on_delete=models.CASCADE)
    id_conta_credito = models.ForeignKey('core.Creditos', verbose_name='Conta Crédito', on_delete=models.CASCADE)
    valor = models.DecimalField('Valor', decimal_places=2, max_digits=9)
    id_historico = models.ForeignKey('core.Historicos', verbose_name='Histórico', on_delete=models.CASCADE)
    compl_historico = models.CharField('Complemento do Histórico', max_length=200)
    ced = models.CharField('CED', max_length=4, default='0001')
    ccrd = models.CharField('CCRD', max_length=3, default='001')
    cec = models.CharField('CEC', max_length=4, default='0001')
    ccrc = models.CharField('CCRC', max_length=3, default='001')
    id_cliente = models.ForeignKey('core.Clientes', verbose_name='Cliente', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.data_lancamento} {self.id_conta_debito} {self.id_conta_credito} {self.valor}' \
               f'{self.id_historico} {self.id_cliente}'
