from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Empresa, FotosCarrossel
from ..forms import FotosCarrosselForm
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def CarrosselProfileView(request):
    dados = Empresa.objects.get(pk=1)
    fotos = dados.fotos_carrossel.all()
    form = FotosCarrosselForm(initial={'empresa': dados})
    return render(request, 'empresa/profile-carrosel.html', {'dados': dados, 'form': form, 'fotos': fotos})


def DelFotoCarroselView(request, pk):
    foto = get_object_or_404(FotosCarrossel, pk=pk)
    foto.delete()
    return redirect('adm:carrossel')



def AddFotoCarroselView(request):
    if request.method == "POST":
        form = FotosCarrosselForm(request.POST or None,
                                  request.FILES or None,)
        if form.is_valid():
            form.save()
            print('salvo')
            return redirect('adm:carrossel')
        else:
            print(form.errors) 
            return redirect('adm:carrossel')
    return redirect('adm:carrossel')




