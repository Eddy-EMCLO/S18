"""Squelette - persistance d'un catalogue de livres (S18).

Ce module orchestre les fichiers et les formats. Il s'appuie sur les
méthodes de sérialisation que vous avez écrites dans la hiérarchie
Livre (to_dict / from_dict).

À IMPLÉMENTER (voir l'énoncé du TP) : le registre de reconstruction,
la fabrique livre_depuis_dict(), et les fonctions de sauvegarde et de
chargement. Aucune fonction de ce module ne doit tester le type concret
d'un livre avec isinstance : le polymorphisme s'en charge.

Programmation Orientée Objet - EICPN 2025-2026.
"""

import json

from livre_s18_squelette import Livre, LivreNumerique, LivreAudio


# Registre discriminateur "type" -> classe. À COMPLÉTER (voir l'énoncé).
_FABRIQUES = {}


def livre_depuis_dict(donnees):
    """Reconstruit le bon sous-type de livre à partir d'un dictionnaire.

    Lit le champ "type", choisit la classe associée dans le registre,
    et délègue à sa classmethod from_dict().

    Args:
        donnees (dict): Dictionnaire produit par une méthode to_dict().

    Returns:
        Livre: Une instance du sous-type exact décrit par "type".

    Raises:
        ValueError: Si le champ "type" est absent ou inconnu du registre.
    """
    if "type" not in donnees :
        raise ValueError ("il faut un type")
    L_type =  donnees["type"]
    if L_type == "Livre":
        return Livre.from_dict(donnees)
    elif L_type == "LivreNumerique":
        return LivreNumerique.from_dict(donnees)
    elif L_type == "LivreAudio" :
        return LivreAudio.from_dict(donnees)
    else:
        raise ValueError ("le type est inconnu")


def sauvegarder_catalogue_json(livres, chemin):
    """Sauvegarde un catalogue (liste de livres) au format JSON.

    Args:
        livres (list[Livre]): Catalogue, éventuellement hétérogène.
        chemin (str): Chemin du fichier de destination.
    """
    save = [livre.to_dict() for livre in livres]
    with open (chemin , "w" ,encoding="utf-8") as f :
        json.dump(save, f)


def charger_catalogue_json(chemin):
    """Recharge un catalogue depuis un fichier JSON, types exacts restaurés.

    Args:
        chemin (str): Chemin du fichier JSON à relire.

    Returns:
        list[Livre]: Le catalogue reconstruit.
    """
    with open(chemin, "r", encoding="utf-8") as f:
        save = json.load(f)

    return [livre_depuis_dict(i) for i in save]