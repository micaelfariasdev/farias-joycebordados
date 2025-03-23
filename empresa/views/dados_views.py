from django.shortcuts import render, redirect, get_object_or_404
from ..models import Empresa
from ..forms import EmpresaForm
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def DadosProfileView(request):
    dados = Empresa.objects.get(pk=1)
    form = EmpresaForm(instance=dados)
    return render(request, 'empresa/profile-dados.html', {'dados': dados, 'form': form})

def DadosEditView(request):
    dados = get_object_or_404(Empresa, pk=1)
    if request.method == "POST":
        form = EmpresaForm(request.POST or None,
                           request.FILES or None, instance=dados)
        if form.is_valid():
            form.save()
            return redirect('adm:dados')
        else:
            return redirect('adm:dados')
    return redirect('adm:dados')

