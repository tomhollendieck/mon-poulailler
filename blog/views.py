from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement

def character_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/post_list.html', {'characters': characters, 'equipements': equipements})

def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    lieu = character.lieu
    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)
    else:
        form = MoveForm()
    if form.is_valid():
        form.save(commit=False) # lieu mis à jour dans character mais pas dans base de données
        if character.lieu.disponibilite == "libre":
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
            nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            if nouveau_lieu.id_equip != "extérieur":
                nouveau_lieu.disponibilite = "occupé"
            nouveau_lieu.save()
            if nouveau_lieu.id_equip == "nid":
                character.etat = "affamée"
            elif nouveau_lieu.id_equip == "extérieur":
                character.etat = "repus"
            elif nouveau_lieu.id_equip == "abri":
                character.etat = "fatiguée"
            else:
                character.etat = "endormie"
            character.save()
            return redirect('character_detail', id_character=id_character)
        else:
            message = 'Attention, ce lieu est déjà occupé !'
            character.lieu.id_equip = ancien_lieu.id_equip
            return render(request, 'blog/character_detail.html', {'character': character, 'message': message})
    else:
        return render(request,'blog/character_detail.html',{'character': character, 'lieu': lieu, 'form': form})

def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    return render(request,'blog/equipement_detail.html',{'equipement': equipement})