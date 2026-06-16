"""Squelette - hiérarchie Livre avec persistance (S18).

Le comportement de la S14 (construction, validation, properties,
constructeurs CSV, méthodes métier, représentations, identité) vous
est fourni COMPLET et fonctionnel. Vous n'avez pas à le modifier.

À IMPLÉMENTER (voir l'énoncé du TP) : les méthodes de sérialisation
JSON de chaque classe, signalées par `raise NotImplementedError`.
Elles sont au nombre de deux par classe :

    to_dict(self)             -> dict
    from_dict(cls, donnees)   -> Livre / LivreNumerique / LivreAudio

Les spécifications précises (format, champs, restauration de l'état)
figurent dans l'énoncé du TP, qui en est l'unique référence.

Programmation Orientée Objet - EICPN 2025-2026.
"""


class Livre:
    """Représente un livre du catalogue de la bibliothèque.

    Un Livre est une ENTITÉ largement immuable : son identité métier
    est son ISBN, et ses cinq caractéristiques (titre, auteur, ISBN,
    nombre de pages, année) sont fixées à la construction et ne
    changent plus. Seule la disponibilité change au cours du temps.

    Attributes:
        titre (str): Titre du livre, lecture seule.
        auteur (str): Nom de l'auteur, lecture seule.
        isbn (str): Code ISBN-13 (13 chiffres exactement), lecture seule.
        nb_pages (int): Nombre de pages (strictement positif), lecture seule.
        annee (int): Année de publication (1455 à 2026), lecture seule.
        disponible (bool): État de disponibilité, lecture seule.
            Modifié uniquement par emprunter() et rendre().
    """

    def __init__(self, titre, auteur, isbn, nb_pages, annee):
        """Initialise un Livre en validant toutes les caractéristiques."""
        if not isinstance(titre, str) or not titre.strip():
            raise ValueError("Le titre ne peut pas être vide.")
        if not isinstance(auteur, str) or not auteur.strip():
            raise ValueError("L'auteur ne peut pas être vide.")
        if not Livre.isbn_valide(isbn):
            raise ValueError(
                "ISBN invalide : 13 chiffres exactement attendus."
            )
        if not isinstance(nb_pages, int) or isinstance(nb_pages, bool):
            raise TypeError("Le nombre de pages doit être un entier.")
        if nb_pages <= 0:
            raise ValueError(
                "Le nombre de pages doit être strictement positif."
            )
        if not isinstance(annee, int) or isinstance(annee, bool):
            raise TypeError("L'année doit être un entier.")
        if not 1455 <= annee <= 2026:
            raise ValueError(
                "L'année doit être comprise entre 1455 et 2026."
            )

        self._titre = titre
        self._auteur = auteur
        self._isbn = isbn
        self._nb_pages = nb_pages
        self._annee = annee
        self._disponible = True

    # ----- Properties en lecture seule (fournies) ---------------------

    @property
    def titre(self):
        """str: Titre du livre (lecture seule)."""
        return self._titre

    @property
    def auteur(self):
        """str: Nom de l'auteur (lecture seule)."""
        return self._auteur

    @property
    def isbn(self):
        """str: Code ISBN-13 du livre (lecture seule)."""
        return self._isbn

    @property
    def nb_pages(self):
        """int: Nombre de pages du livre (lecture seule)."""
        return self._nb_pages

    @property
    def annee(self):
        """int: Année de publication (lecture seule)."""
        return self._annee

    @property
    def disponible(self):
        """bool: État de disponibilité (lecture seule)."""
        return self._disponible

    # ----- Méthode statique (fournie) ---------------------------------

    @staticmethod
    def isbn_valide(chaine):
        """Vérifie qu'une chaîne est un ISBN-13 de forme valide."""
        if not isinstance(chaine, str):
            return False
        if len(chaine) != 13:
            return False
        return chaine.isdigit()

    # ----- Constructeur alternatif CSV (fourni, rappel S13) -----------

    @classmethod
    def depuis_chaine_csv(cls, ligne):
        """Crée un Livre à partir d'une ligne CSV à cinq champs.

        Format : 'titre;auteur;isbn;nb_pages;annee'.
        """
        champs = ligne.split(";")
        if len(champs) != 5:
            raise ValueError(
                "La ligne doit contenir exactement 5 champs séparés "
                "par des points-virgules."
            )
        titre, auteur, isbn, nb_pages_txt, annee_txt = champs
        return cls(titre, auteur, isbn, int(nb_pages_txt), int(annee_txt))

    # ----- Sérialisation JSON : À IMPLÉMENTER --------------------------

    def to_dict(self):
        """Sérialise le livre en dictionnaire compatible JSON.

        Returns:
            dict: Données du livre, incluant un discriminateur de type.
        """
        return {"type" : "livre",
                "titre" : self._titre,
                "auteur" : self._auteur,
                "isbn" : self._isbn,
                "nb_pages" : self._nb_pages,
                "annee" : self._annee,
                }

    @classmethod
    def from_dict(cls, donnees):
        """Reconstruit un livre à partir d'un dictionnaire (pendant JSON).

        Returns:
            Livre: Un livre équivalent à celui qui a été sérialisé.
        """
        
        obj = cls(titre = donnees["titre"],
                   auteur = donnees["auteur"],
                   isbn = donnees["isbn"],
                   nb_pages = donnees["nb_pages"],
                   annee = donnees["annee"], 
            
        )
        if not donnees["disponible"] :
            obj.emprunter()
        return obj

    # ----- Méthodes métier (fournies) ---------------------------------

    def emprunter(self):
        """Marque le livre comme emprunté."""
        if not self._disponible:
            raise ValueError("Livre déjà emprunté")
        self._disponible = False

    def rendre(self):
        """Marque le livre comme rendu (à nouveau disponible)."""
        if self._disponible:
            raise ValueError("Livre déjà disponible")
        self._disponible = True

    def taille_estimee(self):
        """Retourne une description lisible de la taille ('N pages')."""
        return f"{self._nb_pages} pages"

    # ----- Représentations et identité (fournies) ---------------------

    def __str__(self):
        etat = "disponible" if self._disponible else "emprunté"
        return (
            f'"{self._titre}" de {self._auteur} ({self._annee}) - '
            f"{self._nb_pages} p. - {etat}"
        )

    def __repr__(self):
        return (
            f"Livre(titre={self._titre!r}, auteur={self._auteur!r}, "
            f"isbn={self._isbn!r}, nb_pages={self._nb_pages}, "
            f"annee={self._annee})"
        )

    def __eq__(self, autre):
        if not isinstance(autre, Livre):
            return NotImplemented
        return self._isbn == autre._isbn

    def __hash__(self):
        return hash(self._isbn)


class LivreNumerique(Livre):
    """Représente un livre disponible au format numérique."""

    FORMATS_AUTORISES = ("PDF", "EPUB", "MOBI")

    def __init__(self, titre, auteur, isbn, nb_pages, annee, format_fichier):
        """Initialise un LivreNumerique en validant tous les attributs."""
        super().__init__(titre, auteur, isbn, nb_pages, annee)

        if not isinstance(format_fichier, str):
            raise TypeError("Le format doit être une chaîne.")
        if format_fichier not in LivreNumerique.FORMATS_AUTORISES:
            raise ValueError(
                f"Format invalide. Formats autorisés : "
                f"{LivreNumerique.FORMATS_AUTORISES}."
            )
        self._format_fichier = format_fichier

    @property
    def format_fichier(self):
        """str: Format du fichier numérique (lecture seule)."""
        return self._format_fichier

    @classmethod
    def depuis_chaine_csv(cls, ligne):
        """Crée un LivreNumerique depuis une ligne CSV à six champs.

        Format : 'titre;auteur;isbn;nb_pages;annee;format_fichier'.
        """
        champs = ligne.split(";")
        if len(champs) != 6:
            raise ValueError(
                "La ligne doit contenir exactement 6 champs séparés "
                "par des points-virgules."
            )
        titre, auteur, isbn, nb_pages_txt, annee_txt, format_fichier = champs
        return cls(
            titre, auteur, isbn,
            int(nb_pages_txt), int(annee_txt),
            format_fichier,
        )

    # ----- Sérialisation JSON : À IMPLÉMENTER --------------------------

    def to_dict(self):
        """Enrichit le dictionnaire parent avec le format de fichier."""
        num = super.to_dict()
        num["type"] = "LivreNumerique"
        num["format_fichier"] = self._format_fichier
        return num

    @classmethod
    def from_dict(cls, donnees):
        """Reconstruit un LivreNumerique à partir d'un dictionnaire."""
        return cls(titre = donnees["titre"],
                   auteur = donnees["auteur"],
                   isbn = donnees["isbn"],
                   nb_pages = donnees["nb_pages"],
                   annee = donnees["annee"], 
                   format_fichier = donnees["format_fichier"] 
        )
        

    def taille_estimee(self):
        """Retourne 'N pages [FORMAT]'."""
        return f"{self._nb_pages} pages [{self._format_fichier}]"

    def __str__(self):
        return f"{super().__str__()} [{self._format_fichier}]"

    def __repr__(self):
        return (
            f"LivreNumerique(titre={self._titre!r}, "
            f"auteur={self._auteur!r}, isbn={self._isbn!r}, "
            f"nb_pages={self._nb_pages}, annee={self._annee}, "
            f"format_fichier={self._format_fichier!r})"
        )


class LivreAudio(Livre):
    """Représente un livre disponible au format audio.

    Convention : nb_pages désigne le nombre de pages du livre imprimé
    équivalent (information éditoriale conservée).
    """

    def __init__(self, titre, auteur, isbn, nb_pages, annee, duree_minutes):
        """Initialise un LivreAudio en validant tous les attributs."""
        super().__init__(titre, auteur, isbn, nb_pages, annee)

        if not isinstance(duree_minutes, int) or isinstance(duree_minutes, bool):
            raise TypeError("La durée en minutes doit être un entier.")
        if duree_minutes <= 0:
            raise ValueError(
                "La durée en minutes doit être strictement positive."
            )
        self._duree_minutes = duree_minutes

    @property
    def duree_minutes(self):
        """int: Durée totale d'écoute en minutes (lecture seule)."""
        return self._duree_minutes

    @classmethod
    def depuis_chaine_csv(cls, ligne):
        """Crée un LivreAudio depuis une ligne CSV à six champs.

        Format : 'titre;auteur;isbn;nb_pages;annee;duree_minutes'.
        """
        champs = ligne.split(";")
        if len(champs) != 6:
            raise ValueError(
                "La ligne doit contenir exactement 6 champs séparés "
                "par des points-virgules."
            )
        titre, auteur, isbn, nb_pages_txt, annee_txt, duree_txt = champs
        return cls(
            titre, auteur, isbn,
            int(nb_pages_txt), int(annee_txt),
            int(duree_txt),
        )

    # ----- Sérialisation JSON : À IMPLÉMENTER --------------------------

    def to_dict(self):
        """Enrichit le dictionnaire parent avec la durée d'écoute."""
        aud = super.to_dict()
        aud["type"] = "audio"
        aud["duree"] = self._duree_minutes 
        
        return aud 

    @classmethod
    def from_dict(cls, donnees):
        """Reconstruit un LivreAudio à partir d'un dictionnaire."""
        return cls(titre = donnees["titre"],
                   auteur = donnees["auteur"],
                   isbn = donnees["isbn"],
                   nb_pages = donnees["nb_pages"],
                   annee = donnees["annee"], 
                   duree = donnees["duree_minutes"] 
        )

    def taille_estimee(self):
        """Retourne 'Xh YYmin', ou 'YYmin' si moins d'une heure."""
        heures = self._duree_minutes // 60
        minutes = self._duree_minutes % 60
        if heures == 0:
            return f"{minutes}min"
        return f"{heures}h {minutes:02d}min"

    def __str__(self):
        return f"{super().__str__()} [{self.taille_estimee()}]"

    def __repr__(self):
        return (
            f"LivreAudio(titre={self._titre!r}, "
            f"auteur={self._auteur!r}, isbn={self._isbn!r}, "
            f"nb_pages={self._nb_pages}, annee={self._annee}, "
            f"duree_minutes={self._duree_minutes})"
        )
