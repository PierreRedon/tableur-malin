"""Contenu du site Tableur Malin. Ajouter une astuce = ajouter une entrée à ASTUCES, puis relancer build.py."""

SITE = {
    "nom": "Tableur Malin",
    "url": "https://tableurmalin.fr",
    "email": "tableurmalin@gmail.com",
    "accroche": "Une astuce Excel ou Google Sheets par jour, expliquée simplement.",
    # Pack en vente depuis le 11/11/2026 (lien de paiement Stripe fourni par Pierre).
    "stripe_lien": "https://buy.stripe.com/8x26oH8Vq46ZdYcaBq3gk02",
    "pack_prix": "9 €",
    "editeur": "Pierre Redon, entrepreneur individuel",
    "siret": "981 175 714 00030",
    "adresse": "46 route de Vouillé, 86170 Cissé",
}

PACK_MODELES = [
    ("Budget mensuel", "Revenus, dépenses fixes et variables, reste à vivre calculé tout seul."),
    ("Budget annuel", "Douze mois côte à côte, solde du mois et solde cumulé."),
    ("Suivi des dépenses", "Une ligne par achat, le total par catégorie et par mois se met à jour."),
    ("Objectifs d'épargne", "Avancement de chaque objectif et effort mensuel pour tenir l'échéance."),
    ("Suivi des abonnements", "Coût réel sur un an et alerte avant chaque renouvellement."),
    ("Simulateur de prêt", "Mensualité, coût des intérêts et échéancier mois par mois."),
    ("Comptes partagés", "Colocation, couple, vacances : qui doit combien à qui."),
    ("Facture et devis", "Totaux et TVA calculés, mention de franchise affichée si besoin."),
    ("Suivi des factures clients", "Factures payées, en attente, en retard, avec les jours de retard."),
    ("Chiffre d'affaires micro-entreprise", "Cumul, part du plafond et cotisations estimées."),
    ("Suivi de stock", "Entrées, sorties, stock restant et alerte quand il faut recommander."),
    ("Feuille d'heures", "Heures travaillées, heures supplémentaires ou manquantes sur la semaine."),
    ("Planning hebdomadaire", "Une grille par semaine, couleurs automatiques selon le type d'activité."),
    ("Rétroplanning de projet", "Un diagramme en barres qui se dessine à partir des dates."),
    ("Liste de tâches", "Tâches faites barrées, retards signalés en rouge, avancement en pourcentage."),
    ("Suivi d'habitudes", "Une case par jour et un taux de réussite par habitude."),
    ("Suivi de recherche d'emploi", "Candidatures, entretiens et relances à faire."),
    ("Comparateur d'offres", "Notes pondérées par vos priorités pour départager trois options."),
    ("Menus et liste de courses", "Repas de la semaine et courses classées par rayon."),
    ("Organisation d'événement", "Liste d'invités, réponses reçues et budget prévu contre réel."),
    ("Bonus : aide-mémoire", "36 formules en français avec exemple, et 15 raccourcis clavier."),
]

ASTUCES = [
    {
        "slug": "repeter-derniere-action-f4",
        "titre": "Répéter la dernière action d'une seule touche avec F4",
        "court": "Répéter la dernière action avec F4",
        "description": "La touche F4 refait votre dernière action dans Excel : couleur, gras, bordure, ligne insérée ou "
                       "supprimée. Étapes, équivalent Ctrl + Y, Google Sheets et pièges à connaître.",
        "bref": "Faites l'action une première fois, par exemple colorier une ligne en jaune. Sélectionnez ensuite "
                "une autre ligne et appuyez sur F4 : Excel refait la même chose, sans repasser par les menus. "
                "Ctrl + Y a le même effet.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-19",
        "video": "repeter-derniere-action-f4",
        "etapes": [
            "Faites l'action une première fois, normalement : par exemple, sélectionnez une ligne de votre tableau et coloriez-la avec le bouton Couleur de remplissage (le pot de peinture) de l'onglet Accueil.",
            "Sélectionnez la cellule ou la ligne suivante à traiter.",
            "Appuyez sur <kbd>F4</kbd> : la même couleur est appliquée à la nouvelle sélection.",
            "Recommencez autant de fois que nécessaire : une sélection, puis <kbd>F4</kbd>.",
            "Sur un ordinateur portable, si rien ne se passe, maintenez la touche <kbd>Fn</kbd> et appuyez sur <kbd>F4</kbd>, ou utilisez <kbd>Ctrl</kbd> + <kbd>Y</kbd>.",
        ],
        "formules": [],
        "texte": "<p>Colorier dix lignes éparpillées, insérer une ligne vide à cinq endroits, mettre en gras "
                 "plusieurs titres : à chaque fois, il faut retourner chercher le même bouton. La touche "
                 "<kbd>F4</kbd> évite ces allers-retours, car elle rejoue la dernière commande sur la sélection en "
                 "cours.</p>"
                 "<p>Elle fonctionne avec la plupart des actions de mise en forme (couleur de remplissage, couleur "
                 "du texte, gras, bordures, format de nombre), mais aussi avec l'insertion ou la suppression d'une "
                 "ligne ou d'une colonne. Vous pouvez sélectionner plusieurs cellules avant d'appuyer : l'action "
                 "s'applique à toute la sélection.</p>"
                 "<p>Seule la toute dernière action est mémorisée. Si vous mettez une cellule en jaune puis en gras, "
                 "<kbd>F4</kbd> ne répète que le gras. Pour appliquer plusieurs réglages d'un coup, passez par la "
                 "fenêtre Format de cellule (<kbd>Ctrl</kbd> + <kbd>1</kbd>) : tout ce que vous y validez compte "
                 "pour une seule action. Autre solution pour copier toute une mise en forme : le pinceau "
                 "Reproduire la mise en forme, dans l'onglet Accueil.</p>"
                 "<p>La touche <kbd>F4</kbd> a un second rôle, sans rapport : pendant que vous écrivez une formule, "
                 "elle ajoute les signes $ qui servent à "
                 "<a href=\"/astuces/bloquer-cellule-formule-dollar-f4/\">bloquer une cellule</a>.</p>",
        "sheets": "<p>Dans Google Sheets, l'aide de Google indique F4, Ctrl + Y et Ctrl + Maj + Z comme raccourcis "
                  "de la commande Rétablir. En pratique, juste après une mise en forme simple (une couleur, du "
                  "gras), ces touches l'appliquent aussi à la nouvelle sélection. Si F4 ne réagit pas, essayez "
                  "Ctrl + Y. Sur Mac, utilisez ⌘ + Y, dans Google Sheets comme dans Excel.</p>",
        "pieges": [
            "F4 ne répète que la dernière action. Si vous avez fait autre chose entre-temps (une saisie, un collage), c'est cette autre action qui compte, ou rien du tout.",
            "Tout ne se répète pas : la saisie d'un texte ou d'une formule, par exemple, n'est en général pas rejouée. Si F4 reste sans effet, l'action n'est pas répétable.",
            "Juste après une annulation (Ctrl + Z), F4 et Ctrl + Y rétablissent ce que vous venez d'annuler au lieu de répéter.",
            "Sur beaucoup d'ordinateurs portables, la touche F4 règle d'abord le son ou la luminosité : il faut alors appuyer sur Fn + F4.",
            "Pendant la saisie d'une formule, F4 ne répète rien : elle ajoute des $ à la référence. Validez d'abord avec Entrée.",
            "Alt + F4 n'a rien à voir : ce raccourci ferme Excel.",
        ],
    },
    {
        "slug": "nombre-de-jours-entre-deux-dates",
        "titre": "Calculer le nombre de jours entre deux dates dans Excel",
        "court": "Compter les jours entre deux dates",
        "description": "Comment calculer le nombre de jours entre deux dates dans Excel ou Google Sheets : simple "
                       "soustraction, fonctions JOURS et DATEDIF, jours ouvrés, et pièges à éviter.",
        "bref": "Soustrayez simplement la date de début de la date de fin : =B2-A2. Avec le 01/11/2026 en A2 et le "
                "25/12/2026 en B2, vous obtenez 54. Si le résultat ressemble à une date, passez la cellule au "
                "format Standard.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-19",
        "etapes": [
            "Saisissez la date de début dans une cellule, par exemple A2, et la date de fin dans une autre, par exemple B2.",
            "Cliquez dans une cellule vide, tapez =B2-A2 (la date de fin d'abord), puis validez avec <kbd>Entrée</kbd>.",
            "La cellule affiche le nombre de jours qui séparent les deux dates.",
            "Si elle affiche une date au lieu d'un nombre, sélectionnez-la puis, dans l'onglet Accueil, choisissez Standard dans la liste des formats de nombre.",
        ],
        "formules": [
            ("=B2-A2", "Nombre de jours entre la date de début (A2) et la date de fin (B2)."),
            ("=JOURS(B2;A2)", "Le même résultat avec une fonction, à partir d'Excel 2013. Attention à l'ordre : la date de fin d'abord."),
            ("=AUJOURDHUI()-A2", "Nombre de jours écoulés depuis la date en A2. Le résultat change chaque jour."),
            ('=DATEDIF(A2;B2;"m")', "Nombre de mois entiers entre les deux dates. Remplacez \"m\" par \"y\" pour les années entières, ou par \"d\" pour les jours."),
            ("=NB.JOURS.OUVRES(A2;B2)", "Nombre de jours du lundi au vendredi, les deux dates comprises."),
        ],
        "texte": "<p>Pour un tableur, une date est un nombre : chaque jour vaut 1 de plus que la veille. C'est "
                 "pourquoi une simple soustraction suffit pour connaître l'écart entre deux dates, sans aucune "
                 "fonction. La fonction JOURS donne exactement le même résultat ; elle est seulement plus lisible "
                 "dans une longue formule.</p>"
                 "<p>La soustraction compte les jours qui séparent les deux dates : du lundi au vendredi de la même "
                 "semaine, elle renvoie 4. Pour compter aussi le premier jour, par exemple pour la durée d'une "
                 "location ou d'un congé, ajoutez 1 : =B2-A2+1.</p>"
                 "<p>Pour un écart en mois ou en années entières (un âge, une ancienneté), utilisez DATEDIF. "
                 "Cette fonction est un peu à part : Excel ne la propose pas dans la liste qui s'affiche pendant la "
                 "frappe, il faut donc l'écrire en entier. Elle attend la date de début d'abord, puis la date de "
                 "fin, puis une lettre entre guillemets : \"d\" pour les jours, \"m\" pour les mois, \"y\" pour les "
                 "années. Ces lettres restent en anglais, même dans Excel en français.</p>"
                 "<p>Pour un délai en jours travaillés, NB.JOURS.OUVRES laisse de côté les samedis et les "
                 "dimanches. Vous pouvez lui indiquer en troisième position une plage contenant les jours fériés à "
                 "retirer : =NB.JOURS.OUVRES(A2;B2;F2:F12).</p>"
                 "<p>Pour inscrire rapidement la date du jour dans une cellule, voyez "
                 "<a href=\"/astuces/date-du-jour-ctrl-point-virgule/\">le raccourci Ctrl + ;</a>.</p>",
        "sheets": "<p>Dans Google Sheets, la soustraction =B2-A2 fonctionne de la même façon, et les fonctions JOURS "
                  "et DATEDIF s'écrivent à l'identique, avec le point-virgule. Si le résultat s'affiche comme une "
                  "date, ouvrez le menu Format, puis Nombre, et choisissez Nombre. Pour les jours ouvrés, la "
                  "fonction existe aussi ; l'aide de Google la présente sous son nom anglais, NETWORKDAYS.</p>",
        "pieges": [
            "Si le résultat s'affiche sous la forme d'une date (par exemple 23/02/1900), le calcul est juste : c'est le format de la cellule qu'il faut remettre sur Standard.",
            "L'erreur #VALEUR! signale qu'une des deux dates est en réalité du texte (souvent alignée à gauche dans la cellule). Ressaisissez-la sous la forme 25/12/2026.",
            "Avec JOURS, la date de fin s'écrit en premier ; avec DATEDIF, c'est la date de début. Dans le mauvais ordre, JOURS renvoie un nombre négatif et DATEDIF une erreur (#NOMBRE! dans Excel).",
            "La soustraction ne compte pas le premier jour, alors que NB.JOURS.OUVRES compte les deux dates. Ajoutez 1 à la soustraction si vous voulez les deux jours.",
            "Si vos cellules contiennent aussi une heure, le résultat comporte des décimales. Gardez la partie entière avec =ENT(B2-A2).",
            "Microsoft déconseille l'unité \"md\" de DATEDIF, qui peut donner des résultats inexacts.",
        ],
    },
    {
        "slug": "aller-en-bas-liste-ctrl-fleche",
        "titre": "Aller tout en bas d'une longue liste avec Ctrl + ↓",
        "court": "Aller en bas d'une liste avec Ctrl + ↓",
        "description": "Le raccourci Ctrl + flèche bas envoie directement à la dernière ligne remplie d'une colonne "
                       "dans Excel et Google Sheets, sans faire défiler. Avec Maj pour sélectionner, et les pièges.",
        "bref": "Cliquez sur une cellule de la colonne, maintenez Ctrl et appuyez sur la flèche vers le bas : vous "
                "arrivez d'un coup sur la dernière cellule remplie, même 500 lignes plus bas. Ctrl + flèche vers le "
                "haut vous ramène au début.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-18",
        "video": "aller-en-bas-liste-ctrl-fleche",
        "etapes": [
            "Cliquez sur une cellule remplie de votre liste, par exemple le titre de la première colonne.",
            "Maintenez <kbd>Ctrl</kbd> enfoncée, puis appuyez sur la flèche <kbd>↓</kbd> : la cellule active saute à la dernière cellule remplie de la colonne.",
            "Pour revenir en haut, appuyez sur <kbd>Ctrl</kbd> + <kbd>↑</kbd>.",
            "Les flèches <kbd>→</kbd> et <kbd>←</kbd> fonctionnent de la même façon, pour atteindre la dernière ou la première colonne remplie de la ligne.",
            "Pour sélectionner les cellules au lieu de simplement vous déplacer, ajoutez <kbd>Maj</kbd> : <kbd>Ctrl</kbd> + <kbd>Maj</kbd> + <kbd>↓</kbd> sélectionne tout, de la cellule active jusqu'à la dernière cellule remplie.",
        ],
        "formules": [],
        "texte": "<p>Faire tourner la molette de la souris pendant de longues secondes pour atteindre la fin d'une "
                 "liste n'est plus nécessaire : avec <kbd>Ctrl</kbd> et une flèche, le tableur saute directement au "
                 "bord des données, dans la direction de la flèche. C'est pratique pour ajouter une ligne à la suite "
                 "d'une liste, vérifier le dernier enregistrement ou savoir combien de lignes contient un fichier.</p>"
                 "<p>En ajoutant <kbd>Maj</kbd>, le même saut devient une sélection. <kbd>Ctrl</kbd> + <kbd>Maj</kbd> + "
                 "<kbd>↓</kbd> sélectionne toute une colonne de données sans la faire défiler ; enchaînez avec "
                 "<kbd>Ctrl</kbd> + <kbd>Maj</kbd> + <kbd>→</kbd> pour étendre la sélection à tout le tableau. Une "
                 "fois les nombres sélectionnés, leur total s'affiche en bas de la fenêtre : voyez "
                 "<a href=\"/astuces/somme-sans-formule-barre-etat/\">la somme sans formule</a>.</p>"
                 "<p>Deux autres raccourcis complètent celui-ci : <kbd>Ctrl</kbd> + <kbd>Origine</kbd> (la touche "
                 "marquée d'une flèche en diagonale ↖ sur beaucoup de claviers français) ramène à la cellule A1, et "
                 "<kbd>Ctrl</kbd> + <kbd>Fin</kbd> conduit à la dernière cellule utilisée de la feuille.</p>"
                 "<p>Si vos titres disparaissent de l'écran une fois en bas de la liste, pensez à "
                 "<a href=\"/astuces/figer-premiere-ligne/\">figer la première ligne</a>.</p>",
        "sheets": "<p>Le raccourci est le même dans Google Sheets : Ctrl + ↓ pour atteindre la dernière cellule "
                  "remplie, Ctrl + ↑ pour remonter, et Ctrl + Maj + flèche pour sélectionner. Sur Mac, remplacez "
                  "Ctrl par la touche ⌘, dans Google Sheets comme dans Excel.</p>",
        "pieges": [
            "Le saut s'arrête à la première cellule vide rencontrée : si une case est vide au milieu de la colonne, vous vous arrêtez juste au-dessus. Appuyez de nouveau sur le raccourci pour passer au bloc suivant, ou partez d'une colonne entièrement remplie.",
            "Si vous utilisez le raccourci depuis la dernière cellule remplie, ou dans une colonne vide, vous vous retrouvez tout en bas de la feuille (ligne 1 048 576 dans Excel). Pas de panique : Ctrl + ↑ vous ramène aux données.",
            "Si une cellule est en cours de modification (le curseur clignote dedans), le raccourci déplace le curseur dans le texte au lieu de changer de cellule. Validez d'abord avec Entrée, ou annulez avec Échap.",
            "Dans une liste filtrée, le saut ne tient compte que des lignes visibles.",
            "Si, dans Excel, les flèches font défiler la feuille sans changer de cellule, la touche Arrêt défil est sans doute activée : appuyez dessus pour la désactiver.",
        ],
    },
    {
        "slug": "calculer-une-moyenne",
        "titre": "Calculer une moyenne dans Excel",
        "court": "Calculer une moyenne",
        "description": "Comment calculer une moyenne dans Excel ou Google Sheets avec la fonction MOYENNE : étapes, "
                       "cellules vides et zéros, moyenne avec condition grâce à MOYENNE.SI, et pièges à éviter.",
        "bref": "Tapez =MOYENNE(B2:B10) pour obtenir la moyenne des nombres de B2 à B10. La fonction additionne les "
                "nombres et divise par leur quantité. Les cellules vides et le texte sont laissés de côté, mais "
                "un 0 compte.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-18",
        "etapes": [
            "Cliquez dans une cellule vide, là où la moyenne doit s'afficher.",
            "Tapez =MOYENNE( puis sélectionnez à la souris les nombres concernés, par exemple B2:B10.",
            "Fermez la parenthèse et validez avec <kbd>Entrée</kbd> : la cellule affiche la moyenne.",
            "Si le résultat a trop de décimales, réduisez-en le nombre avec le bouton Réduire les décimales de l'onglet Accueil.",
        ],
        "formules": [
            ("=MOYENNE(B2:B10)", "Moyenne des nombres de B2 à B10."),
            ("=MOYENNE(B2:B10;D2:D10)", "Moyenne de deux plages à la fois, séparées par un point-virgule."),
            ('=MOYENNE.SI(A2:A100;"Lyon";C2:C100)', "Moyenne des montants de la colonne C, uniquement pour les lignes où la colonne A contient Lyon."),
            ('=MOYENNE.SI(B2:B10;">0")', "Moyenne des nombres supérieurs à 0 : les zéros ne sont plus comptés."),
            ("=ARRONDI(MOYENNE(B2:B10);1)", "La moyenne, arrondie à une décimale."),
        ],
        "texte": "<p>La fonction MOYENNE fait le calcul appris à l'école : elle additionne les nombres, puis divise "
                 "le total par le nombre de valeurs. Avec les notes 12, 15 et 9, elle renvoie 12.</p>"
                 "<p>Une règle à connaître : une cellule vide est laissée de côté, alors qu'une cellule qui contient "
                 "0 est prise en compte et fait baisser la moyenne. Pour un élève absent à un contrôle, laissez "
                 "donc la case vide plutôt que d'y écrire 0, sauf si le zéro est voulu. Le texte présent dans la "
                 "plage (« absent », « n.c. ») est ignoré lui aussi.</p>"
                 "<p>Pour une moyenne limitée à certaines lignes, MOYENNE.SI fonctionne comme "
                 "<a href=\"/astuces/compter-cellules-nb-si/\">NB.SI</a> : la plage à examiner, le critère entre "
                 "guillemets, puis la plage des nombres. Avec plusieurs conditions, utilisez MOYENNE.SI.ENS.</p>"
                 "<p>Besoin de la moyenne juste pour information, sans l'écrire dans la feuille ? Sélectionnez les "
                 "nombres : Excel l'affiche en bas de la fenêtre, comme expliqué dans "
                 "<a href=\"/astuces/somme-sans-formule-barre-etat/\">la somme sans formule</a>. Et pour maîtriser "
                 "les décimales du résultat, voyez <a href=\"/astuces/arrondir-un-nombre/\">comment arrondir un "
                 "nombre</a>.</p>",
        "sheets": "<p>La fonction porte le même nom dans Google Sheets en français : =MOYENNE(B2:B10), avec le "
                  "point-virgule pour séparer plusieurs plages. Le texte y est ignoré de la même façon, et "
                  "MOYENNE.SI existe aussi. Pour la valeur du milieu plutôt que la moyenne, la fonction s'appelle "
                  "MEDIANE.</p>",
        "pieges": [
            "Un 0 n'est pas une cellule vide : il compte dans la moyenne. Videz la cellule, ou utilisez =MOYENNE.SI(B2:B10;\">0\").",
            "Si la plage ne contient aucun nombre, la formule affiche l'erreur #DIV/0!.",
            "Une seule cellule en erreur (#N/A, #VALEUR!) dans la plage suffit à mettre toute la moyenne en erreur.",
            "Des nombres enregistrés comme du texte (souvent alignés à gauche) sont ignorés sans aucun avertissement : la moyenne est alors calculée sur les autres valeurs seulement.",
            "La moyenne de plusieurs moyennes n'est juste que si les groupes ont la même taille. En cas de doute, calculez la moyenne directement sur toutes les valeurs.",
            "MOYENNE donne le même poids à chaque valeur. Pour des notes avec coefficients, il faut une moyenne pondérée : =SOMMEPROD(B2:B10;C2:C10)/SOMME(C2:C10), avec les notes en B et les coefficients en C.",
        ],
    },
    {
        "slug": "filtrer-liste-ctrl-maj-l",
        "titre": "Filtrer une liste en trois touches avec Ctrl + Maj + L",
        "court": "Filtrer une liste avec Ctrl + Maj + L",
        "description": "Le raccourci Ctrl + Maj + L ajoute des flèches de filtre aux titres d'un tableau Excel ou Google "
                       "Sheets : vous n'affichez que les lignes voulues, sans rien supprimer. Étapes et pièges.",
        "bref": "Cliquez dans votre liste, puis appuyez sur Ctrl + Maj + L : une petite flèche apparaît à côté de "
                "chaque titre de colonne. Cliquez sur une flèche, cochez ce que vous voulez voir, validez. Les autres "
                "lignes sont masquées, pas supprimées.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-17",
        "video": "filtrer-liste-ctrl-maj-l",
        "etapes": [
            "Cliquez sur n'importe quelle cellule de votre liste. La première ligne doit contenir les titres des colonnes.",
            "Maintenez <kbd>Ctrl</kbd> et <kbd>Maj</kbd> enfoncées, puis appuyez sur <kbd>L</kbd> : une flèche apparaît dans chaque cellule de titre.",
            "Cliquez sur la flèche de la colonne à filtrer, par exemple Ville.",
            "Décochez (Sélectionner tout), cochez la ou les valeurs à garder, par exemple Lyon, puis cliquez sur OK.",
            "Pour tout réafficher, appuyez de nouveau sur <kbd>Ctrl</kbd> + <kbd>Maj</kbd> + <kbd>L</kbd> : les flèches disparaissent et toutes les lignes reviennent.",
        ],
        "formules": [("=SOUS.TOTAL(9;C2:C100)", "Additionne uniquement les lignes encore visibles après un filtre. Une formule SOMME, elle, continue de compter les lignes masquées.")],
        "texte": "<p>Un filtre ne supprime rien : il masque provisoirement les lignes qui ne vous intéressent pas. "
                 "C'est le moyen le plus simple de retrouver les clients d'une ville, les factures d'un mois ou les "
                 "lignes encore vides dans une longue liste.</p>"
                 "<p>Le raccourci fait la même chose que le bouton Filtrer de l'onglet Données. Dans Excel, vous "
                 "reconnaissez une liste filtrée à deux détails : les numéros des lignes passent en bleu, et la "
                 "flèche de la colonne concernée est remplacée par un petit entonnoir.</p>"
                 "<p>Vous pouvez filtrer plusieurs colonnes à la suite, par exemple la ville puis le mois : seules "
                 "les lignes qui respectent toutes les conditions restent affichées. Sur une colonne de nombres, le "
                 "menu de la flèche propose aussi des filtres numériques, pour ne garder que les montants supérieurs "
                 "à une valeur. Pour retirer le filtre d'une seule colonne sans toucher aux autres, cliquez sur son "
                 "entonnoir, puis sur la commande Effacer le filtre.</p>"
                 "<p>Le petit total affiché en bas de la fenêtre suit le filtre : voyez "
                 "<a href=\"/astuces/somme-sans-formule-barre-etat/\">la somme sans formule</a>.</p>",
        "sheets": "<p>Dans Google Sheets, cliquez dans la liste, ouvrez le menu Données, puis choisissez Créer un "
                  "filtre. Sur PC, le raccourci Ctrl + Maj + L fait la même chose. Une icône de filtre apparaît dans "
                  "chaque titre : cliquez dessus, décochez les valeurs à masquer, puis validez avec OK. La fonction "
                  "SOUS.TOTAL existe aussi, avec la même écriture.</p>",
        "pieges": [
            "Une ligne entièrement vide au milieu de la liste arrête le filtre : les lignes situées en dessous ne sont pas prises en compte. Supprimez la ligne vide, ou sélectionnez toute la liste avant d'utiliser le raccourci.",
            "Sans ligne de titres, c'est votre première ligne de données qui reçoit les flèches et qui n'est plus filtrée. Ajoutez toujours une ligne de titres.",
            "Les lignes masquées existent toujours : une formule SOMME continue de les additionner. Pour un total qui suit le filtre, utilisez SOUS.TOTAL.",
            "Le raccourci fonctionne comme un interrupteur : si les flèches sont déjà là, il les retire et annule vos filtres en cours.",
            "Sur Mac, le raccourci d'Excel peut différer selon la version : essayez ⌘ + Maj + F, ou passez par l'onglet Données, bouton Filtrer.",
        ],
    },
    {
        "slug": "reunir-deux-cellules-concatener",
        "titre": "Réunir le contenu de deux cellules en une seule",
        "court": "Réunir deux cellules en une seule",
        "description": "Comment assembler le prénom et le nom, ou tout autre texte, de deux cellules dans une seule "
                       "avec le signe & dans Excel et Google Sheets. Avec CONCAT et JOINDRE.TEXTE, et les pièges.",
        "bref": "Tapez =A2&\" \"&B2 : le signe & colle le contenu de A2 et celui de B2, et les guillemets contenant "
                "une espace ajoutent une espace entre les deux. Avec Camille en A2 et Martin en B2, vous obtenez "
                "Camille Martin.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-17",
        "etapes": [
            "Cliquez dans une cellule vide, à droite de vos données, par exemple C2.",
            "Tapez = puis cliquez sur la première cellule à assembler, par exemple A2.",
            "Tapez &\" \"& (le signe &, une espace entre guillemets, puis de nouveau &), et cliquez sur la seconde cellule, B2.",
            "Validez avec <kbd>Entrée</kbd> : la cellule affiche les deux contenus réunis, séparés par une espace.",
            "Recopiez la formule vers le bas pour traiter toute la liste.",
        ],
        "formules": [
            ('=A2&" "&B2', "Réunit A2 et B2 avec une espace entre les deux : Camille Martin."),
            ('=A2&B2', "Colle les deux contenus sans rien entre eux : CamilleMartin."),
            ('=B2&", "&A2', "Tout texte placé entre guillemets est ajouté tel quel : Martin, Camille."),
            ('=CONCAT(A2;" ";B2)', "La même chose avec une fonction, dans Excel 2019 et les versions suivantes. Dans les versions plus anciennes, la fonction s'appelle CONCATENER."),
            ('=JOINDRE.TEXTE(" ";VRAI;A2:D2)', "Dans Excel 2019 et les versions suivantes : réunit toute une plage en plaçant une espace entre chaque valeur. VRAI demande d'ignorer les cellules vides."),
        ],
        "texte": "<p>Le signe & (l'esperluette, sur la touche 1 d'un clavier français) est le moyen le plus court "
                 "d'assembler des textes : il fonctionne dans toutes les versions d'Excel et dans Google Sheets, "
                 "sans fonction à retenir. Tout ce que vous écrivez entre guillemets est ajouté tel quel : une "
                 "espace, une virgule, un tiret ou un mot entier.</p>"
                 "<p>Les fonctions CONCAT et CONCATENER font exactement la même chose, en séparant les éléments par "
                 "des points-virgules. Microsoft indique que CONCAT remplace CONCATENER, qui reste disponible pour "
                 "les anciens fichiers.</p>"
                 "<p>JOINDRE.TEXTE devient intéressante dès qu'il y a plus de trois ou quatre cellules à réunir : "
                 "vous indiquez le séparateur une seule fois, puis la plage entière. C'est pratique pour assembler "
                 "une adresse répartie sur plusieurs colonnes.</p>"
                 "<p>Le résultat est une formule : il change si vous modifiez A2 ou B2. Pour le figer, copiez les "
                 "cellules, puis collez-les au même endroit avec l'option de collage Valeurs. Et pour faire le "
                 "chemin inverse, c'est-à-dire séparer un prénom et un nom, voyez "
                 "<a href=\"/astuces/remplissage-instantane-ctrl-e/\">le remplissage instantané avec Ctrl + E</a>.</p>",
        "sheets": "<p>Le signe & fonctionne à l'identique dans Google Sheets : =A2&\" \"&B2. La fonction CONCATENER "
                  "y existe aussi et accepte autant d'éléments que nécessaire. Attention à CONCAT, qui n'y réunit "
                  "que deux valeurs à la fois. Pour réunir une plage avec un séparateur, l'aide de Google présente "
                  "la fonction sous son nom anglais : =TEXTJOIN(\" \";VRAI;A2:D2).</p>",
        "pieges": [
            "Sans l'espace entre guillemets, les deux mots sont collés : CamilleMartin. Vérifiez qu'il y a bien une espace entre les deux guillemets.",
            "Une date ou un montant réunis à un texte perdent leur mise en forme : la date devient un nombre comme 46343. Dans Excel, utilisez la fonction TEXTE, par exemple =A2&\" le \"&TEXTE(B2;\"jj/mm/aaaa\").",
            "Le résultat est toujours du texte, même s'il ne contient que des chiffres : il ne pourra pas être additionné tel quel.",
            "Ne supprimez pas les colonnes d'origine tant que la formule en dépend : collez d'abord le résultat en valeurs.",
            "Réunir le contenu de deux cellules n'est pas fusionner les cellules : le bouton de fusion d'Excel ne conserve que le contenu de la cellule en haut à gauche.",
        ],
    },
    {
        "slug": "somme-sans-formule-barre-etat",
        "titre": "Obtenir une somme sans formule : sélectionnez, regardez en bas",
        "court": "Obtenir une somme sans taper de formule",
        "description": "Pour connaître le total de quelques cellules dans Excel ou Google Sheets, inutile d'écrire une "
                       "formule : sélectionnez-les, la somme et la moyenne s'affichent en bas de la fenêtre.",
        "bref": "Sélectionnez les nombres à la souris, puis regardez tout en bas de la fenêtre : le tableur y affiche "
                "leur somme, sans rien écrire dans la feuille. Excel y ajoute la moyenne et le nombre de cellules "
                "remplies.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-16",
        "video": "somme-sans-formule-barre-etat",
        "etapes": [
            "Cliquez sur le premier nombre et, sans relâcher le bouton de la souris, descendez jusqu'au dernier.",
            "Relâchez, puis regardez la barre d'état, la bande située tout en bas de la fenêtre d'Excel, à droite.",
            "Lisez la somme. Juste à côté, Excel affiche aussi la moyenne et le nombre de cellules remplies.",
        ],
        "formules": [],
        "texte": "<p>C'est le moyen le plus rapide de vérifier un total, de contrôler une addition faite ailleurs ou "
                 "de répondre à une question au téléphone : rien n'est écrit dans la feuille, et le résultat "
                 "disparaît dès que vous cliquez ailleurs.</p>"
                 "<p>Les cellules n'ont pas besoin de se toucher. Cliquez sur la première, maintenez la touche "
                 "<kbd>Ctrl</kbd> enfoncée, puis cliquez sur les autres : la somme tient compte de toutes les "
                 "cellules sélectionnées. Vous pouvez aussi cliquer sur la lettre d'une colonne pour obtenir le "
                 "total de la colonne entière.</p>"
                 "<p>Dans Excel, un clic droit sur la barre d'état ouvre la liste des calculs disponibles : vous "
                 "pouvez y cocher le minimum et le maximum, ou décocher ceux qui ne vous servent pas. Dans les "
                 "versions récentes d'Excel pour Microsoft 365, un clic sur une valeur de la barre d'état la copie, "
                 "pour la coller ensuite où vous voulez.</p>"
                 "<p>Si le total doit rester dans le tableau, il faut cette fois une vraie formule : voyez "
                 "<a href=\"/astuces/somme-automatique-alt-egal/\">la somme automatique avec Alt + =</a>.</p>",
        "sheets": "<p>Google Sheets fait la même chose : sélectionnez plusieurs nombres, leur somme apparaît en bas à "
                  "droite de la fenêtre. Cliquez sur ce résultat pour choisir un autre calcul, comme la moyenne, le "
                  "minimum, le maximum ou le nombre de valeurs.</p>",
        "pieges": [
            "Il faut sélectionner au moins deux cellules contenant des nombres : avec une seule cellule, la barre d'état n'affiche aucun calcul.",
            "Si seul le nombre de cellules apparaît, sans somme, vos nombres sont sans doute enregistrés comme du texte (ils sont alors souvent alignés à gauche).",
            "Dans une liste filtrée, le calcul ne porte que sur les lignes visibles, pas sur les lignes masquées par le filtre.",
            "Ce résultat n'est écrit nulle part : il disparaît quand vous cliquez ailleurs. Pour le conserver, utilisez une formule SOMME.",
        ],
    },
    {
        "slug": "compter-cellules-nb-si",
        "titre": "Compter les cellules qui contiennent un mot avec NB.SI",
        "court": "Compter les cellules qui contiennent un mot",
        "description": "Comment compter dans Excel ou Google Sheets le nombre de cellules qui contiennent un mot, une "
                       "valeur ou un nombre supérieur à un seuil avec la fonction NB.SI. Syntaxe, exemples et pièges.",
        "bref": "Tapez =NB.SI(A2:A100;\"Payé\") pour compter combien de cellules de la plage A2:A100 contiennent "
                "exactement le mot Payé. Le premier élément est la plage à examiner, le second le critère, entre "
                "guillemets.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-16",
        "etapes": [
            "Cliquez dans une cellule vide, là où le résultat doit s'afficher.",
            "Tapez =NB.SI( puis sélectionnez à la souris la plage à examiner, par exemple A2:A100.",
            "Tapez un point-virgule, puis le mot recherché entre guillemets, et fermez la parenthèse : =NB.SI(A2:A100;\"Payé\").",
            "Validez avec <kbd>Entrée</kbd> : la cellule affiche le nombre de cellules correspondantes.",
        ],
        "formules": [
            ('=NB.SI(A2:A100;"Payé")', "Compte les cellules qui contiennent exactement Payé."),
            ('=NB.SI(A2:A100;D1)', "Le critère peut venir d'une cellule, ici D1 : pas de guillemets dans ce cas."),
            ('=NB.SI(B2:B100;">50")', "Compte les nombres supérieurs à 50. La comparaison s'écrit entre guillemets."),
            ('=NB.SI(A2:A100;"*facture*")', "L'astérisque remplace n'importe quelle suite de caractères : compte les cellules dont le texte contient le mot facture."),
            ('=NB.SI(B2:B100;">"&D1)', "Pour comparer à une cellule, collez l'opérateur et la cellule avec le signe &."),
        ],
        "texte": "<p>NB.SI répond à toutes les questions du type « combien de fois » : combien de factures payées, "
                 "combien de clients à Lyon, combien de notes au-dessus de 10. La fonction ne tient pas compte des "
                 "majuscules et des minuscules : « payé » et « PAYÉ » sont comptés ensemble.</p>"
                 "<p>Deux caractères spéciaux rendent le critère plus souple : l'astérisque (*) remplace une suite "
                 "de caractères quelconque, et le point d'interrogation (?) un seul caractère. Ainsi, \"Dup*\" "
                 "compte Dupont, Dupond et Dupuis.</p>"
                 "<p>NB.SI n'accepte qu'un seul critère. Pour en combiner plusieurs, par exemple les factures "
                 "payées du mois de janvier, utilisez NB.SI.ENS, qui suit la même logique que "
                 "<a href=\"/astuces/somme-si-ens/\">SOMME.SI.ENS</a> : "
                 "=NB.SI.ENS(A2:A100;\"Payé\";B2:B100;\"Janvier\").</p>",
        "sheets": "<p>La fonction porte le même nom dans Google Sheets en français : NB.SI, avec le point-virgule "
                  "entre la plage et le critère. Les caractères * et ? y fonctionnent de la même façon, et NB.SI.ENS "
                  "existe aussi.</p>",
        "pieges": [
            "Le critère texte et les comparaisons s'écrivent entre guillemets droits : \">50\" et non >50. Sans guillemets, la formule est refusée ou renvoie 0.",
            "Un espace en trop à la fin d'une cellule (« Payé » suivi d'un espace) suffit à ne pas la compter. En cas de résultat trop faible, vérifiez les espaces ou utilisez \"Payé*\".",
            "Sans astérisque, NB.SI cherche le contenu exact de la cellule : \"facture\" ne compte pas une cellule qui contient « facture mars ».",
            "Pour chercher un vrai astérisque ou un vrai point d'interrogation, faites-le précéder d'un tilde : \"~?\".",
        ],
    },
    {
        "slug": "ajuster-largeur-colonne-double-clic",
        "titre": "Des ##### dans une cellule ? Élargir la colonne d'un double-clic",
        "court": "Faire disparaître les ##### d'un double-clic",
        "description": "Une cellule Excel remplie de ##### n'a rien perdu : la colonne est trop étroite. Un "
                       "double-clic sur le bord droit de l'en-tête de colonne l'ajuste au contenu, dans Excel "
                       "comme dans Google Sheets.",
        "bref": "Les ##### signifient que la colonne est trop étroite pour afficher le nombre ou la date. Placez "
                "la souris sur le trait à droite de la lettre de la colonne, tout en haut, puis double-cliquez : "
                "la colonne prend exactement la largeur de son contenu.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-15",
        "video": "ajuster-largeur-colonne-double-clic",
        "etapes": [
            "Repérez la lettre de la colonne concernée, tout en haut de la feuille (par exemple B).",
            "Placez la souris sur le trait qui sépare cette lettre de la suivante (entre B et C). Le pointeur se transforme en double flèche.",
            "Double-cliquez. La colonne s'élargit juste assez pour afficher la cellule la plus longue.",
        ],
        "formules": [],
        "texte": "<p>Rien n'est perdu quand une cellule affiche des dièses : cliquez dessus et regardez la barre de "
                 "formule, la valeur est toujours là. Excel préfère afficher ##### plutôt qu'un nombre coupé, qui "
                 "pourrait être lu de travers.</p>"
                 "<p>Pour ajuster plusieurs colonnes d'un coup, sélectionnez-les en faisant glisser la souris sur "
                 "leurs lettres, puis double-cliquez sur l'un des traits entre deux lettres sélectionnées. Pour "
                 "toute la feuille, cliquez d'abord sur le bouton Sélectionner tout, dans le coin en haut à gauche "
                 "de la grille.</p>"
                 "<p>La même commande existe dans le ruban d'Excel : onglet Accueil, bouton Format, puis Ajuster "
                 "la largeur de colonne. Vous pouvez aussi faire glisser le trait à la main pour choisir une autre "
                 "largeur. Et le double-clic fonctionne de la même façon sur les lignes, pour ajuster leur "
                 "hauteur.</p>",
        "sheets": "<p>Le geste est le même dans Google Sheets : un double-clic sur le bord droit de l'en-tête de "
                  "colonne ajuste la largeur au contenu, et il agit sur toutes les colonnes sélectionnées. Un clic "
                  "droit sur l'en-tête donne aussi accès à une commande de redimensionnement, avec une option "
                  "d'ajustement automatique.</p>",
        "pieges": [
            "Visez bien l'en-tête, c'est-à-dire le trait entre les lettres tout en haut, et non une bordure de cellule dans le tableau : un double-clic dans une cellule ouvre simplement sa modification.",
            "La largeur se cale sur la cellule la plus longue de toute la colonne. Un long titre ou une longue phrase plus bas peut donc donner une colonne très large : raccourcissez ce texte ou réglez la largeur à la main.",
            "Si les ##### restent quelle que soit la largeur, la cellule contient sans doute une date ou une heure négative, par exemple le résultat d'une soustraction entre deux dates faite dans le mauvais sens.",
            "L'ajustement n'est pas permanent : si vous saisissez ensuite une valeur plus longue, refaites un double-clic.",
        ],
    },
    {
        "slug": "arrondir-un-nombre",
        "titre": "Arrondir un nombre dans Excel",
        "court": "Arrondir un nombre",
        "description": "Comment arrondir un nombre dans Excel ou Google Sheets avec ARRONDI, ARRONDI.SUP et "
                       "ARRONDI.INF, et la différence entre arrondir une valeur et masquer ses décimales.",
        "bref": "Tapez =ARRONDI(A2;2) pour arrondir le nombre de la cellule A2 à deux décimales : 1234,567 devient "
                "1234,57. Remplacez le 2 par 0 pour obtenir un nombre entier.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-15",
        "etapes": [
            "Cliquez dans une cellule vide, à côté du nombre à arrondir.",
            "Tapez =ARRONDI(A2;2) : A2 est la cellule qui contient le nombre, et 2 le nombre de décimales à garder.",
            "Validez avec <kbd>Entrée</kbd>. Si A2 contient 1234,567, la cellule affiche 1234,57.",
        ],
        "formules": [
            ("=ARRONDI(A2;2)", "Arrondit à deux décimales, au plus proche : 1234,567 devient 1234,57."),
            ("=ARRONDI(A2;0)", "Arrondit à l'entier le plus proche : 1234,567 devient 1235."),
            ("=ARRONDI.SUP(A2;0)", "Arrondit toujours vers le haut : 12,1 devient 13. Pratique pour compter des cartons ou des trajets."),
            ("=ARRONDI.INF(A2;0)", "Arrondit toujours vers le bas : 12,9 devient 12."),
            ("=ARRONDI(A2;-2)", "Un nombre de décimales négatif arrondit à gauche de la virgule, ici à la centaine : 1234,567 devient 1200."),
        ],
        "texte": "<p>Il y a deux façons très différentes de faire disparaître des décimales. Les boutons de "
                 "décimales de l'onglet Accueil (ajouter ou réduire) changent seulement l'affichage : la cellule "
                 "montre 1234,57, mais Excel continue de calculer avec 1234,567. La fonction ARRONDI, elle, "
                 "change réellement la valeur.</p>"
                 "<p>C'est ce qui explique les totaux qui semblent faux de quelques centimes : les lignes "
                 "affichées sont arrondies à l'écran, mais l'addition porte sur les valeurs complètes. Pour qu'un "
                 "total corresponde à ce qui est affiché, par exemple sur une facture, arrondissez chaque ligne "
                 "avec ARRONDI avant d'additionner.</p>"
                 "<p>Vous pouvez arrondir directement le résultat d'un calcul en le plaçant dans la fonction : "
                 "=ARRONDI(B2*C2;2) arrondit le produit de B2 par C2 à deux décimales.</p>",
        "sheets": "<p>Les fonctions portent les mêmes noms dans Google Sheets en français : ARRONDI, ARRONDI.SUP et "
                  "ARRONDI.INF, avec le point-virgule entre les deux éléments. La distinction est la même : les "
                  "boutons de décimales de la barre d'outils ne changent que l'affichage.</p>",
        "pieges": [
            "Réduire les décimales affichées n'arrondit pas la valeur : les calculs suivants utilisent toujours le nombre complet.",
            "Séparez les deux éléments par un point-virgule, et écrivez les décimales avec une virgule : =ARRONDI(12,345;2).",
            "ARRONDI.SUP éloigne de zéro et ARRONDI.INF rapproche de zéro : avec un nombre négatif, =ARRONDI.SUP(-3,2;0) donne -4.",
            "N'arrondissez pas trop tôt dans une suite de calculs : gardez les valeurs complètes dans les étapes intermédiaires et arrondissez le résultat final, sauf quand chaque ligne doit correspondre à un montant réellement facturé.",
        ],
    },
    {
        "slug": "date-du-jour-ctrl-point-virgule",
        "titre": "Insérer la date du jour en deux touches avec Ctrl + ;",
        "court": "Insérer la date du jour avec Ctrl + ;",
        "description": "Le raccourci Ctrl + ; inscrit la date du jour dans une cellule Excel ou Google Sheets, sans "
                       "formule. Une date fixe, qui ne change plus, contrairement à =AUJOURDHUI().",
        "bref": "Cliquez dans la cellule, puis appuyez sur Ctrl + ; (la touche Ctrl et le point-virgule) : la date du "
                "jour s'inscrit. Validez avec Entrée. Cette date reste fixe : elle ne changera pas demain.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-14",
        "video": "date-du-jour-ctrl-point-virgule",
        "etapes": [
            "Cliquez dans la cellule où la date doit apparaître.",
            "Maintenez la touche <kbd>Ctrl</kbd> enfoncée et appuyez sur la touche <kbd>;</kbd> (point-virgule). La date du jour s'inscrit dans la cellule.",
            "Validez avec <kbd>Entrée</kbd>.",
        ],
        "formules": [("=AUJOURDHUI()", "L'autre méthode : cette formule affiche aussi la date du jour, mais elle se met à jour toute seule. Demain, elle affichera la date de demain.")],
        "texte": "<p>Le raccourci inscrit une date fixe, exactement comme si vous l'aviez tapée à la main. C'est ce "
                 "qu'il faut pour noter le jour d'une réception, d'un paiement, d'un appel ou d'une relance : la "
                 "date ne doit plus bouger ensuite.</p>"
                 "<p>La formule =AUJOURDHUI() fait l'inverse : elle est recalculée à chaque ouverture du fichier et "
                 "affiche toujours la date du moment. Elle est utile pour calculer un nombre de jours restants ou un "
                 "retard, mais pas pour garder la trace d'un événement.</p>"
                 "<p>Pour l'heure, le raccourci indiqué par Microsoft est Ctrl + Maj + ; (point-virgule). Sur un "
                 "clavier français, essayez aussi Ctrl + : (deux-points). Pour obtenir la date et l'heure dans la "
                 "même cellule, insérez la date, tapez une espace, puis insérez l'heure.</p>",
        "sheets": "<p>Le raccourci est le même dans Google Sheets : Ctrl + ; pour la date du jour (⌘ + ; sur Mac) et "
                  "Ctrl + Maj + ; pour l'heure. La formule =AUJOURDHUI() existe aussi, avec le même comportement : "
                  "elle change chaque jour.</p>",
        "pieges": [
            "Ne confondez pas avec =AUJOURDHUI() : une date saisie avec cette formule aura changé demain. Pour dater un événement, utilisez le raccourci.",
            "Si la cellule affiche un nombre comme 46340 au lieu d'une date, elle est au format Nombre. Dans Excel, faites un clic droit, choisissez Format de cellule, puis la catégorie Date.",
            "Le raccourci agit sur la cellule sélectionnée ou en cours de saisie. Si rien ne se passe, vérifiez que vous n'êtes pas dans une autre fenêtre ou dans une zone de recherche.",
            "Sur Mac, le raccourci d'Excel peut différer selon la version : essayez Contrôle + ; (point-virgule).",
        ],
    },
    {
        "slug": "calculer-un-pourcentage",
        "titre": "Calculer un pourcentage dans Excel",
        "court": "Calculer un pourcentage",
        "description": "Comment calculer un pourcentage dans Excel ou Google Sheets : la part d'un total, une "
                       "augmentation ou une baisse en pourcentage, et le bouton Style de pourcentage pour l'affichage.",
        "bref": "Divisez la partie par le total, par exemple =B2/C2, puis cliquez sur le bouton % (Style de "
                "pourcentage) de l'onglet Accueil. Ne multipliez pas par 100 : c'est le format qui s'en charge.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-14",
        "etapes_excel": True,
        "etapes": [
            "Dans une cellule vide, tapez la division de la partie par le total. Exemple : 42 bonnes réponses en B2 sur 50 questions en C2, tapez =B2/C2.",
            "Validez avec <kbd>Entrée</kbd>. Excel affiche 0,84.",
            "Cliquez de nouveau sur la cellule du résultat.",
            "Dans l'onglet Accueil, groupe Nombre, cliquez sur le bouton <kbd>%</kbd> (Style de pourcentage). La cellule affiche 84 %.",
        ],
        "formules": [
            ("=B2/C2", "La part d'un total : la partie divisée par le total, à afficher ensuite au format pourcentage."),
            ("=(C2-B2)/B2", "Une évolution en pourcentage : la nouvelle valeur moins l'ancienne, le tout divisé par l'ancienne. De 2 342 à 2 500, le résultat est 6,75 %."),
            ("=B2*20%", "Le montant d'un pourcentage : 20 % de la valeur en B2."),
            ("=B2*(1+20%)", "Augmenter une valeur de 20 %. Pour la diminuer de 20 %, écrivez =B2*(1-20%)."),
        ],
        "texte": "<p>Pour Excel, un pourcentage est un nombre ordinaire : 84 % et 0,84 sont la même valeur, seul "
                 "l'affichage change. C'est pour cela qu'il ne faut pas multiplier par 100 dans la formule. Le "
                 "bouton Style de pourcentage s'occupe de l'affichage.</p>"
                 "<p>Pour afficher des décimales (84,5 % au lieu de 85 %), utilisez les deux boutons de décimales "
                 "(ajouter ou réduire), juste à côté du bouton %. Le raccourci clavier du format pourcentage "
                 "est Ctrl + Maj + %.</p>"
                 "<p>Une évolution négative correspond à une baisse : de 2 500 à 2 425, la formule donne -3 %.</p>",
        "sheets": "<p>Les formules sont exactement les mêmes dans Google Sheets. Pour l'affichage, sélectionnez la "
                  "cellule puis cliquez sur le bouton % de la barre d'outils, ou ouvrez le menu Format, puis Nombre, "
                  "puis Pourcentage.</p>",
        "pieges": [
            "N'ajoutez pas *100 à la formule si vous appliquez ensuite le format pourcentage : vous obtiendriez 8400 % au lieu de 84 %.",
            "Appliquer le format % à un nombre déjà saisi le multiplie par 100 à l'affichage : 10 devient 1000 %. Saisissez 0,1 ou tapez directement 10 %.",
            "Pour une évolution, divisez toujours par la valeur de départ (l'ancienne), pas par la nouvelle.",
            "Si le total est vide ou égal à zéro, Excel affiche l'erreur #DIV/0!. Renseignez le total, ou attendez d'avoir la valeur.",
        ],
    },
    {
        "slug": "recopier-formule-double-clic",
        "titre": "Recopier une formule jusqu'en bas d'un double-clic",
        "court": "Recopier une formule d'un double-clic",
        "description": "Inutile de tirer une formule sur des centaines de lignes : un double-clic sur la poignée de recopie, "
                       "le petit carré en bas à droite de la cellule, la recopie jusqu'en bas dans Excel et Google Sheets.",
        "bref": "Sélectionnez la cellule qui contient la formule, puis double-cliquez sur le petit carré situé dans son "
                "coin inférieur droit : la formule est recopiée jusqu'à la dernière ligne de votre tableau.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-13",
        "video": "recopier-formule-double-clic",
        "etapes": [
            "Écrivez la formule une seule fois, dans la première ligne de votre tableau, par exemple =B2*1,2 en C2 pour passer un prix hors taxes en prix TTC à 20 %. Validez avec <kbd>Entrée</kbd>.",
            "Cliquez de nouveau sur la cellule de la formule, ici C2.",
            "Placez le pointeur sur le petit carré vert, dans le coin inférieur droit de la cellule : il se transforme en croix noire fine. Ce carré s'appelle la poignée de recopie.",
            "Double-cliquez. La formule descend toute seule jusqu'à la dernière ligne remplie de la colonne voisine.",
        ],
        "formules": [("=B2*1,2", "La formule saisie en C2. Une fois recopiée, elle devient =B3*1,2 en C3, =B4*1,2 en C4, et ainsi de suite.")],
        "texte": "<p>Le double-clic fait exactement la même chose que tirer la poignée vers le bas avec la souris, mais "
                 "il s'arrête tout seul au bon endroit. Sur un tableau de plusieurs centaines de lignes, c'est beaucoup "
                 "plus rapide et plus sûr.</p>"
                 "<p>Pour savoir où s'arrêter, le tableur regarde la colonne d'à côté : la recopie descend tant que "
                 "cette colonne est remplie. La poignée sert aussi à recopier un texte, un nombre ou à prolonger une "
                 "série (lundi, mardi, mercredi).</p>",
        "sheets": "<p>Le geste est le même dans Google Sheets : le petit carré est bleu, et un double-clic recopie la "
                  "formule jusqu'à la dernière ligne remplie de la colonne voisine. Il arrive aussi que Sheets propose "
                  "de lui-même de remplir le reste de la colonne : il suffit alors d'accepter la suggestion.</p>",
        "pieges": [
            "La recopie s'arrête à la première cellule vide de la colonne voisine. Si votre tableau a des trous, vérifiez que la formule est bien allée jusqu'en bas.",
            "Le double-clic recopie seulement vers le bas. Pour recopier vers la droite, tirez la poignée avec la souris.",
            "Si la formule utilise une cellule qui ne doit pas bouger (un taux saisi une seule fois, par exemple), bloquez-la avec le signe $ avant de recopier.",
            "Le petit carré n'apparaît pas dans Excel ? Ouvrez Fichier, Options, puis la rubrique des options avancées, et vérifiez que la case concernant la poignée de recopie et le glisser-déplacer des cellules est cochée.",
        ],
    },
    {
        "slug": "retour-a-la-ligne-dans-une-cellule",
        "titre": "Aller à la ligne dans une cellule",
        "court": "Aller à la ligne dans une cellule",
        "description": "Comment faire un retour à la ligne dans une cellule Excel ou Google Sheets : le raccourci "
                       "Alt + Entrée, le bouton Renvoyer à la ligne automatiquement et les pièges à éviter.",
        "bref": "Pendant que vous écrivez dans la cellule, appuyez sur Alt + Entrée à l'endroit où le texte doit passer "
                "à la ligne. Dans Google Sheets, le raccourci est Ctrl + Entrée.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-13",
        "etapes_excel": True,
        "etapes": [
            "Double-cliquez dans la cellule (ou sélectionnez-la et appuyez sur <kbd>F2</kbd>) pour modifier son contenu.",
            "Placez le curseur à l'endroit exact où le texte doit être coupé.",
            "Appuyez sur <kbd>Alt</kbd> + <kbd>Entrée</kbd> : la suite du texte passe à la ligne, dans la même cellule.",
            "Validez avec <kbd>Entrée</kbd>. La hauteur de la ligne s'adapte pour afficher tout le texte.",
        ],
        "formules": [],
        "texte": "<p>Si vous voulez seulement qu'un texte trop long reste dans sa colonne, sans choisir vous-même où il "
                 "est coupé, sélectionnez les cellules et cliquez sur le bouton Renvoyer à la ligne automatiquement, "
                 "dans l'onglet Accueil, groupe Alignement. Le texte se replie alors selon la largeur de la colonne, "
                 "et s'ajuste si vous l'élargissez.</p>"
                 "<p>Les deux méthodes se complètent : Alt + Entrée impose une coupure à un endroit précis (une "
                 "adresse sur deux lignes, par exemple), le renvoi automatique s'occupe du reste.</p>",
        "sheets": "<p>Dans Google Sheets, appuyez sur Ctrl + Entrée pendant la saisie (⌘ + Entrée sur Mac). Sous "
                  "Windows, Alt + Entrée fonctionne aussi. Pour le renvoi automatique, sélectionnez les cellules puis "
                  "ouvrez le menu Format et choisissez l'option de retour à la ligne automatique qui renvoie le texte "
                  "à la ligne.</p>",
        "pieges": [
            "Appuyer sur Entrée seule ne crée pas de nouvelle ligne : cela valide la cellule et passe à la suivante.",
            "Si une partie du texte reste cachée, la hauteur de la ligne a sans doute été fixée à la main. Dans Excel, onglet Accueil, bouton Format, choisissez Ajuster la hauteur de ligne.",
            "Alt + Entrée est le raccourci d'Excel pour Windows. Sur Mac, la combinaison dépend de la version : essayez Option + Retour, ou Contrôle + Option + Retour.",
        ],
    },
    {
        "slug": "somme-automatique-alt-egal",
        "titre": "Additionner une colonne en deux touches avec Alt + =",
        "court": "Additionner une colonne avec Alt + =",
        "description": "Le raccourci Alt + = d'Excel écrit la formule SOMME à votre place : cliquez sous une colonne de "
                       "nombres, appuyez, validez. Plusieurs totaux d'un coup, et l'équivalent Google Sheets.",
        "bref": "Cliquez dans la cellule située juste sous vos nombres, appuyez sur Alt + =, puis validez avec Entrée : "
                "Excel écrit la formule SOMME et choisit lui-même la plage à additionner.",
        "outils": "Excel", "niveau": "Débutant", "date": "2026-11-12",
        "video": "somme-automatique-alt-egal",
        "etapes": [
            "Cliquez dans la cellule vide située juste sous la colonne de nombres à additionner, par exemple B7 si vos montants vont de B2 à B6.",
            "Appuyez sur <kbd>Alt</kbd> + <kbd>=</kbd>. Excel écrit la formule SOMME et entoure la plage qu'il propose d'additionner.",
            "Vérifiez que la plage proposée est la bonne, puis validez avec <kbd>Entrée</kbd>.",
            "Pour plusieurs totaux d'un coup, sélectionnez d'abord toutes les cellules de total (par exemple B7 à D7), puis appuyez sur <kbd>Alt</kbd> + <kbd>=</kbd> : chaque colonne reçoit sa somme, sans passer par Entrée.",
        ],
        "formules": [("=SOMME(B2:B6)", "La formule qu'Excel écrit à votre place en B7.")],
        "texte": "<p>Ce raccourci déclenche le bouton Somme automatique, que l'on trouve aussi dans l'onglet Accueil et "
                 "dans l'onglet Formules. Il fonctionne également pour une ligne : placez-vous dans la cellule située "
                 "à droite des nombres.</p>"
                 "<p>Le total reste une formule ordinaire : si vous modifiez un montant, il se recalcule tout seul.</p>",
        "sheets": "<p>Dans Google Sheets, le plus sûr est de taper la formule ci-dessous dans la cellule du total. "
                  "Vous pouvez aussi sélectionner vos nombres, cliquer sur le bouton Fonctions (Σ) de la barre "
                  "d'outils et choisir SOMME.</p>",
        "sheets_formule": "=SOMME(B2:B6)",
        "pieges": [
            "Excel s'arrête à la première cellule vide : si votre colonne contient un trou, la plage proposée est incomplète. Corrigez-la avant de valider.",
            "Un nombre saisi comme du texte (souvent aligné à gauche dans la cellule) n'est pas compté dans la somme.",
            "Le raccourci Alt + = est celui d'Excel pour Windows. Sur Mac, le plus simple est de cliquer sur le bouton Somme automatique de l'onglet Accueil.",
        ],
    },
    {
        "slug": "bloquer-cellule-formule-dollar-f4",
        "titre": "Bloquer une cellule dans une formule avec le signe $",
        "court": "Bloquer une cellule avec $ (F4)",
        "description": "Comment figer une cellule dans une formule Excel ou Google Sheets pour qu'elle ne se décale pas "
                       "quand on recopie : le signe $, la touche F4 et les références absolues, relatives et mixtes.",
        "bref": "Écrivez la référence avec deux signes dollar, $B$1 au lieu de B1 : elle ne bouge plus quand vous "
                "recopiez la formule. La touche F4 ajoute les dollars à votre place.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-12",
        "etapes": [
            "Commencez votre formule normalement, par exemple =A2*B1 pour multiplier un prix (A2) par un taux saisi une seule fois en B1.",
            "Dans la barre de formule, cliquez sur la référence à bloquer, ici B1.",
            "Appuyez sur <kbd>F4</kbd> : B1 devient $B$1. Vous pouvez aussi taper les deux signes $ à la main.",
            "Validez, puis recopiez la formule vers le bas : A2 devient A3, A4, A5, mais $B$1 reste $B$1.",
        ],
        "formules": [("=A2*$B$1", "A2 suit la recopie ligne après ligne ; $B$1 désigne toujours la même cellule.")],
        "texte": "<p>Par défaut, une référence est relative : quand on recopie la formule, elle se décale avec elle. "
                 "Le signe $ placé devant la lettre bloque la colonne, celui placé devant le chiffre bloque la ligne. "
                 "Avec les deux, la référence est dite absolue.</p>"
                 "<p>Chaque appui sur F4 passe au type suivant : $B$1 (tout est bloqué), B$1 (seule la ligne est "
                 "bloquée), $B1 (seule la colonne est bloquée), puis de nouveau B1. Les deux formes intermédiaires, "
                 "dites mixtes, servent surtout dans les tableaux à double entrée.</p>",
        "sheets": "<p>Le signe $ fonctionne exactement de la même façon dans Google Sheets, et la touche F4 y ajoute "
                  "aussi les dollars pendant la saisie ou la modification d'une formule.</p>",
        "pieges": [
            "Le signe $ n'a aucun rapport avec la monnaie et ne change pas le résultat de la formule : il agit seulement au moment de la recopie.",
            "Sur beaucoup d'ordinateurs portables, F4 règle d'abord le son ou la luminosité : essayez alors Fn + F4.",
            "Bloquer une cellule dans une formule ne la protège pas contre la modification : pour cela, il faut passer par la protection de la feuille.",
        ],
    },
    {
        "slug": "remplissage-instantane-ctrl-e",
        "titre": "Séparer prénom et nom sans formule avec Ctrl + E",
        "court": "Séparer prénom et nom avec Ctrl + E",
        "description": "Le remplissage instantané d'Excel (Ctrl + E) sépare prénom et nom, extrait un code postal ou "
                       "reformate une liste entière à partir d'un seul exemple. Équivalent Google Sheets inclus.",
        "bref": "Tapez le résultat attendu pour la première ligne, validez, puis appuyez sur Ctrl + E : Excel "
                "comprend le modèle et remplit toute la colonne.",
        "outils": "Excel", "niveau": "Débutant", "date": "2026-11-11",
        "video": "remplissage-instantane-ctrl-e",
        "etapes": [
            "Placez-vous dans la colonne juste à droite de vos données. Si vos noms complets sont en colonne A, travaillez en colonne B.",
            "En B2, tapez à la main le résultat voulu pour la première ligne, par exemple le prénom « Camille », puis validez avec Entrée.",
            "Appuyez sur <kbd>Ctrl</kbd> + <kbd>E</kbd>. Excel remplit toutes les lignes en suivant votre exemple.",
            "Recommencez en colonne C avec le nom de famille.",
        ],
        "formules": [],
        "texte": "<p>Le remplissage instantané ne sert pas qu'aux prénoms. Il fonctionne dès qu'un modèle se répète : "
                 "extraire le code postal d'une adresse, mettre des numéros de téléphone au même format, assembler "
                 "prénom et nom dans une seule cellule, passer une colonne en majuscules.</p>"
                 "<p>Le raccourci se retrouve aussi dans le menu Données, bouton Remplissage instantané. "
                 "Il existe depuis Excel 2013.</p>",
        "sheets": "<p>Google Sheets n'a pas de raccourci Ctrl + E. Pour séparer un prénom et un nom, utilisez la "
                  "fonction SPLIT, qui coupe le texte à chaque espace et range les morceaux dans les cellules voisines.</p>",
        "sheets_formule": '=SPLIT(A2;" ")',
        "pieges": [
            "Le résultat est figé : si vous corrigez un nom en colonne A, la colonne B ne suit pas. Refaites Ctrl + E, ou passez par une formule.",
            "Si Excel se trompe sur une ligne (prénom composé, particule), corrigez deux ou trois exemples à la main et relancez Ctrl + E.",
            "Aucune colonne vide ne doit séparer vos données de la colonne à remplir.",
        ],
    },
    {
        "slug": "recherchex-remplacer-recherchev",
        "titre": "RECHERCHEX : la formule qui remplace RECHERCHEV",
        "court": "Remplacer RECHERCHEV par RECHERCHEX",
        "description": "RECHERCHEX retrouve une valeur dans un tableau sans compter les colonnes, cherche aussi vers la "
                       "gauche et affiche le message de votre choix quand rien n'est trouvé. Syntaxe et exemple.",
        "bref": "RECHERCHEX demande trois choses : la valeur cherchée, la colonne où la chercher, la colonne à "
                "renvoyer. Plus de numéro de colonne à compter, plus de FAUX à ajouter à la fin.",
        "outils": "Excel, Google Sheets", "niveau": "Intermédiaire", "date": "2026-11-11",
        "etapes": [
            "Repérez la valeur que vous connaissez, par exemple une référence produit saisie en E2.",
            "Repérez la colonne où cette référence se trouve dans votre tableau, par exemple A2:A100.",
            "Repérez la colonne qui contient l'information voulue, par exemple le prix en C2:C100.",
            "Écrivez la formule ci-dessous. Le quatrième élément, facultatif, est le texte affiché quand la référence n'existe pas.",
        ],
        "formules": [('=RECHERCHEX(E2;A2:A100;C2:C100;"Introuvable")',
                      "Cherche E2 dans la colonne A et renvoie le prix de la même ligne en colonne C.")],
        "texte": "<p>Avec RECHERCHEV, la colonne de recherche devait être la première du tableau et il fallait compter "
                 "le rang de la colonne à renvoyer. Insérer une colonne suffisait à fausser le résultat. RECHERCHEX "
                 "désigne directement les deux colonnes, dans n'importe quel ordre : la colonne renvoyée peut se "
                 "trouver à gauche de la colonne de recherche.</p>"
                 "<p>La correspondance est exacte par défaut, ce qui évite les résultats approximatifs quand on "
                 "oublie le dernier argument de RECHERCHEV.</p>",
        "sheets": "<p>Google Sheets propose la même fonction, avec les mêmes arguments. Selon la langue des fonctions "
                  "de votre fichier, elle s'écrit RECHERCHEX ou XLOOKUP.</p>",
        "pieges": [
            "RECHERCHEX n'existe pas dans Excel 2019 et les versions plus anciennes : la cellule affiche #NOM?. Dans ce cas, gardez RECHERCHEV ou INDEX et EQUIV.",
            "Les deux colonnes doivent avoir la même hauteur (A2:A100 et C2:C100), sinon la formule renvoie #VALEUR!.",
            "Un nombre stocké comme du texte ne correspond pas au même nombre stocké comme un nombre : vérifiez le format des deux côtés.",
        ],
    },
    {
        "slug": "liste-deroulante", "etapes_excel": True,
        "titre": "Créer une liste déroulante dans une cellule",
        "court": "Créer une liste déroulante",
        "description": "Comment ajouter une liste déroulante dans Excel et dans Google Sheets pour limiter la saisie à "
                       "quelques choix : étapes, source de la liste et erreurs fréquentes.",
        "bref": "Dans Excel : onglet Données, Validation des données, Autoriser « Liste ». Dans Google Sheets : menu "
                "Insertion, Menu déroulant.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-11",
        "etapes": [
            "Sélectionnez les cellules qui doivent proposer la liste.",
            "Dans Excel, ouvrez l'onglet Données puis cliquez sur Validation des données.",
            "Dans le champ Autoriser, choisissez Liste.",
            "Dans le champ Source, tapez vos choix séparés par des points-virgules, ou sélectionnez une plage qui les contient.",
            "Validez : une flèche apparaît à droite de la cellule quand vous cliquez dessus.",
        ],
        "formules": [("Payé;En attente;En retard", "À saisir dans le champ Source, sans signe égal.")],
        "texte": "<p>Si la liste risque d'évoluer, écrivez plutôt vos choix dans une colonne à part, sur un autre "
                 "onglet par exemple, et indiquez cette plage comme source. Vous n'aurez qu'à modifier la colonne "
                 "pour mettre à jour toutes les listes.</p>",
        "sheets": "<p>Dans Google Sheets, sélectionnez les cellules puis ouvrez le menu Insertion et choisissez Menu "
                  "déroulant. Saisissez chaque choix dans le panneau qui s'ouvre à droite ; vous pouvez attribuer une "
                  "couleur à chacun.</p>",
        "pieges": [
            "Une liste déroulante n'empêche pas de coller une autre valeur par-dessus : le collage remplace aussi la règle de validation.",
            "Dans Excel en français, le séparateur des choix est le point-virgule, pas la virgule.",
        ],
    },
    {
        "slug": "figer-premiere-ligne", "etapes_excel": True,
        "titre": "Garder la ligne de titres visible quand on fait défiler",
        "court": "Figer la ligne de titres",
        "description": "Figer la première ligne ou la première colonne dans Excel et Google Sheets pour garder les "
                       "titres à l'écran pendant le défilement, et comment libérer les volets.",
        "bref": "Dans Excel : onglet Affichage, Figer les volets, Figer la ligne supérieure. Dans Google Sheets : menu "
                "Affichage, Figer, 1 ligne.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-11",
        "etapes": [
            "Ouvrez l'onglet Affichage.",
            "Cliquez sur Figer les volets.",
            "Choisissez Figer la ligne supérieure. La ligne 1 reste affichée quand vous descendez dans le tableau.",
        ],
        "formules": [],
        "texte": "<p>Pour figer à la fois des lignes et des colonnes, cliquez d'abord sur la cellule située juste sous "
                 "les lignes et juste à droite des colonnes à garder, par exemple B2 pour conserver la ligne 1 et la "
                 "colonne A. Choisissez ensuite Figer les volets dans le même menu.</p>"
                 "<p>Pour revenir en arrière : Affichage, Figer les volets, Libérer les volets.</p>",
        "sheets": "<p>Dans Google Sheets, ouvrez le menu Affichage, puis Figer, et choisissez 1 ligne ou 1 colonne. "
                  "Vous pouvez aussi faire glisser le trait épais gris situé dans le coin en haut à gauche de la "
                  "grille.</p>",
        "pieges": [
            "Figer les volets ne change rien à l'impression. Pour répéter les titres sur chaque page imprimée dans Excel : onglet Mise en page, Imprimer les titres.",
        ],
    },
    {
        "slug": "supprimer-les-doublons", "etapes_excel": True,
        "titre": "Supprimer les doublons d'une liste en deux clics",
        "court": "Supprimer les doublons",
        "description": "Supprimer les lignes en double dans Excel et Google Sheets avec l'outil intégré, ou obtenir une "
                       "liste sans doublons qui se met à jour avec la fonction UNIQUE.",
        "bref": "Dans Excel : onglet Données, Supprimer les doublons. Dans Google Sheets : menu Données, Nettoyage des "
                "données, Supprimer les doublons.",
        "outils": "Excel, Google Sheets", "niveau": "Débutant", "date": "2026-11-11",
        "etapes": [
            "Faites une copie de votre onglet : la suppression est définitive une fois le fichier enregistré.",
            "Cliquez dans votre tableau.",
            "Dans Excel, ouvrez l'onglet Données et cliquez sur Supprimer les doublons.",
            "Cochez « Mes données ont des en-têtes » si la première ligne contient des titres, puis choisissez les colonnes à comparer.",
            "Validez. Excel indique combien de lignes ont été supprimées et combien il en reste.",
        ],
        "formules": [("=UNIQUE(A2:A100)",
                      "Affiche la liste sans doublons dans une autre colonne, sans toucher aux données d'origine.")],
        "texte": "<p>Le choix des colonnes compte. Si vous cochez seulement la colonne E-mail, deux lignes avec le même "
                 "e-mail sont des doublons, même si le reste diffère. Si vous cochez toutes les colonnes, seules les "
                 "lignes entièrement identiques sont supprimées. Dans tous les cas, c'est la première ligne "
                 "rencontrée qui est conservée.</p>"
                 "<p>La fonction UNIQUE est disponible dans Excel 2021, Microsoft 365 et Google Sheets. Elle se met à "
                 "jour quand la liste d'origine change.</p>",
        "sheets": "<p>Dans Google Sheets, sélectionnez la plage, ouvrez le menu Données, puis Nettoyage des données, "
                  "et choisissez Supprimer les doublons.</p>",
        "pieges": [
            "« Dupont » et « Dupont » suivi d'un espace ne sont pas des doublons pour le tableur. Nettoyez d'abord les espaces avec la fonction SUPPRESPACE.",
        ],
    },
    {
        "slug": "somme-si-ens",
        "titre": "Additionner selon plusieurs critères avec SOMME.SI.ENS",
        "court": "Additionner selon plusieurs critères",
        "description": "SOMME.SI.ENS additionne uniquement les lignes qui respectent une ou plusieurs conditions : total "
                       "par catégorie, par mois, par client. Syntaxe, exemple et erreurs courantes.",
        "bref": "SOMME.SI.ENS prend d'abord la colonne à additionner, puis des paires « colonne à tester ; critère ». "
                "Elle fonctionne à l'identique dans Excel et Google Sheets.",
        "outils": "Excel, Google Sheets", "niveau": "Intermédiaire", "date": "2026-11-11",
        "etapes": [
            "Indiquez d'abord la colonne qui contient les montants à additionner.",
            "Ajoutez la première colonne à tester, puis le critère attendu entre guillemets.",
            "Ajoutez autant de paires colonne et critère que nécessaire, séparées par des points-virgules.",
        ],
        "formules": [
            ('=SOMME.SI.ENS(C2:C100;A2:A100;"Courses";B2:B100;"Janvier")',
             "Additionne les montants de la colonne C pour la catégorie Courses au mois de Janvier."),
            ('=SOMME.SI.ENS(C2:C100;A2:A100;F1;C2:C100;">50")',
             "Le critère peut venir d'une cellule (F1) ou être une comparaison, ici les montants supérieurs à 50."),
        ],
        "texte": "<p>Toutes les conditions doivent être vraies en même temps pour qu'une ligne soit comptée. "
                 "Pour compter des lignes au lieu d'additionner des montants, la fonction NB.SI.ENS suit la même "
                 "logique, sans la première colonne.</p>",
        "sheets": "<p>Même nom et mêmes arguments dans Google Sheets.</p>",
        "pieges": [
            "L'ordre est inversé par rapport à SOMME.SI : ici, la colonne à additionner vient en premier.",
            "Toutes les plages doivent avoir la même taille, sinon la formule renvoie #VALEUR!.",
        ],
    },
]
