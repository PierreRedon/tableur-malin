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
