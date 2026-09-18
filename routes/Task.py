from fastapi import APIRouter

Task_route=APIRouter(prefix="/Task", tags=["Task"])



@Task_route.post("/ajouter_tache")
def ajoutes():
    return "ajouter"

@Task_route.get("/consulter_one_tache")
def consulter_one():
    return "Voire ces tache"

@Task_route.get("/consulter_all_tache")
def consulter_all():
    return "Voire ces tache"
@Task_route.put("/modifier_tache")
def modifier():
    return "modifier tache"

@Task_route.get("/marquer_tache_terminer")
def marquer_fin():
    return "tache marquer"

@Task_route.delete("/suppimer_tache")
def supprimer():
    return "tache suppmier"

@Task_route.get("/filtrer_tache")
def filtrer():
    return "Voire ces tache filtrer"

