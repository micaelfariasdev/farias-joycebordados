from django.shortcuts import render
from django.utils.timezone import now
from ..models import Empresa
from ..forms import FilterForm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def DashBoardView(request):
    dados = Empresa.objects.get(pk=1)
    filter = {
        'data_init': request.GET.get('data_init') or (datetime(now().year, now().month, 1)).strftime('%Y-%m-%d'),
        'data_end': request.GET.get('data_end') or (datetime.now()).strftime('%Y-%m-%d')
    }
    if isinstance(filter['data_init'], str):
        filter['data_init'] = datetime.strptime(
            filter['data_init'], '%Y-%m-%d')
    if isinstance(filter['data_end'], str):
        filter['data_end'] = datetime.strptime(filter['data_end'], '%Y-%m-%d')
    dif_days = filter['data_end'] - filter['data_init']
    filtercompare = {
        'data_init': (filter['data_init'] - relativedelta(months=1)),
        'data_end': (filter['data_init'] - relativedelta(months=1) + dif_days)
    }
    if filtercompare['data_end'] > filter['data_init']:
        filtercompare['data_end'] = (
            filter['data_init'] - relativedelta(days=1))

    filter['data_init'] = filter['data_init'].strftime('%Y-%m-%d')
    filter['data_end'] = filter['data_end'].strftime('%Y-%m-%d')
    filtercompare['data_init'] = filtercompare['data_init'].strftime(
        '%Y-%m-%d')
    filtercompare['data_end'] = filtercompare['data_end'].strftime('%Y-%m-%d')

    contexto = {'dados': dados, 'filter': filter}
    form = FilterForm(initial=filter)
    form2 = FilterForm(initial=filtercompare)
    contexto.update({'form': form, 'form2': form2})
    return render(request, 'empresa/profile-detail.html', context=contexto)
