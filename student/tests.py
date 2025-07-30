# import json
# import os
# from django.db import connections
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lsy_website.settings')
# django.setup()
# students = [
#   {
#     "id_student": "DTuE9QBF",
#     "class": "Terminale C1",
#     "summary": "Salut ! Tes résultats en Mathématiques sont vraiment solides, c'est un excellent point pour ta Terminale C. En Physique-Chimie, tu es juste au-dessus de la moyenne, et avec un peu plus de travail, tu pourrais vraiment faire la différence. Il faudrait aussi donner un petit coup de pouce à la Langue Vivante 2 pour assurer sur tous les fronts. Tu es sur une très bonne voie pour le Bac, continue tes efforts !",
#     "matieres": [
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 9.5,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Ta moyenne est juste en dessous de 10. C'est une matière à faible coefficient, mais chaque point compte pour le Bac et pour ta culture générale. Avec un peu de pratique régulière, tu peux facilement gagner des points.",
#         "recommandations": [
#           {
#             "type_ressource": "Application mobile",
#             "titre": "Duolingo",
#             "lien": "https://fr.duolingo.com/",
#             "description": "Une application ludique pour pratiquer la langue 15-20 minutes par jour. Idéale pour revoir le vocabulaire et les bases de la grammaire de manière amusante."
#           }
#         ]
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 13.5,
#         "coefficient": 5,
#         "evaluation_personnalisee": "Excellent travail en Maths ! C'est une matière capitale en Terminale C et ta moyenne est très encourageante. Tu maîtrises bien les notions. Pour viser l'excellence, assure-toi de bien maîtriser la rédaction et la justification de tes raisonnements.",
#         "recommandations": [
#           {
#             "type_ressource": "Site web",
#             "titre": "Annales de Bac - APMEP",
#             "lien": "https://www.apmep.fr/Annales-bac-C-Afrique",
#             "description": "Entraîne-toi sur de vrais sujets de Bac des années précédentes. Cela t'aidera à te familiariser avec le format des épreuves et à gérer ton temps."
#           }
#         ]
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 11.0,
#         "coefficient": 5,
#         "evaluation_personnalisee": "C'est un résultat correct, tu as les bases. Mais comme c'est une matière à fort coefficient, c'est ici que tu peux gagner beaucoup de points. Identifie les chapitres où tu te sens moins à l'aise pour les retravailler en priorité.",
#         "recommandations": [
#           {
#             "type_ressource": "Vidéo YouTube",
#             "titre": "Playlist Terminale S (Physique-Chimie) - Les Bons Profs",
#             "lien": "https://www.youtube.com/playlist?list=PL1BFrh61onZp5u5o54N69k_35rS0A_DOj",
#             "description": "Cette playlist couvre la plupart des chapitres de Terminale. Les vidéos sont courtes et vont droit au but, parfait pour réviser un point précis que tu n'as pas compris."
#           }
#         ]
#       }
#     ],
#     "recommandations_generales": "Bonjour"
#   },
#   {
#     "id_student": "igTdgm8X",
#     "class": "4ème1",
#     "summary": "Félicitations ! Tes résultats sont excellents dans toutes les matières. Tu montres une grande aisance et une maîtrise impressionnante pour ton niveau. C'est un profil très prometteur. Continue sur cette magnifique lancée, ton travail et ta curiosité portent leurs fruits !",
#     "matieres": [
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 14.17,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Excellent ! Tu as un très bon niveau. Pour aller encore plus loin, essaie de lire des petits articles ou de regarder des vidéos dans cette langue pour enrichir ton vocabulaire.",
#         "recommandations": []
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 15.0,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Bravo, c'est un résultat remarquable. Tu as une excellente logique mathématique. N'hésite pas à demander des exercices plus difficiles à ton professeur pour te challenger.",
#         "recommandations": [
#           {
#             "type_ressource": "Site web",
#             "titre": "Khan Academy - Arithmétique",
#             "lien": "https://fr.khanacademy.org/math/arithmetic",
#             "description": "Ce site te permet d'explorer des notions, parfois un peu plus avancées, avec des exercices interactifs. Parfait pour un élève curieux comme toi."
#           }
#         ]
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 15.5,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Superbe moyenne ! Ta compréhension des concepts physiques et chimiques est excellente. Continue de bien soigner tes schémas et tes explications lors des devoirs.",
#         "recommandations": []
#       }
#     ],
#     "recommandations_generales": "Bonjour"
#   },
#   {
#     "id_student": "D5dm4MNV",
#     "class": "Terminale C1",
#     "summary": "Salut ! Tu as un excellent niveau en Langue Vivante 2, c'est un bel atout. Par contre, je vois que tu rencontres des difficultés importantes dans les matières scientifiques, qui sont le cœur de la Terminale C. Il est urgent de réagir, surtout en Physique-Chimie. Ne te décourage pas ! Avec un plan de travail ciblé et de la rigueur, tu peux remonter la pente. Concentrons-nous sur les priorités.",
#     "matieres": [
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 14.5,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Excellent travail, c'est un très bon résultat. Continue ainsi, ces points te seront précieux pour le Bac.",
#         "recommandations": []
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 11.17,
#         "coefficient": 5,
#         "evaluation_personnalisee": "C'est juste au-dessus de la moyenne. Pour une Terminale C, c'est fragile. Il faut absolument consolider tes bases pour ne pas être en difficulté sur les nouveaux chapitres. Reprends les contrôles passés pour comprendre tes erreurs.",
#         "recommandations": [
#           {
#             "type_ressource": "Vidéo YouTube",
#             "titre": "Toutes les vidéos de Maths Terminale - Yvan Monka",
#             "lien": "https://www.youtube.com/playlist?list=PLVUDmbpupCa4j_r0D-01AGg5KAEc-vJ0j",
#             "description": "Yvan Monka est une référence. Ses vidéos expliquent très clairement les concepts. Reprends pas à pas les chapitres où tu as des doutes. C'est une aide précieuse."
#           }
#         ]
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 3.5,
#         "coefficient": 5,
#         "evaluation_personnalisee": "C'est une note très basse qui signale de grandes difficultés. Il est crucial de ne pas laisser ces lacunes s'installer. Il faut reprendre les bases, peut-être même celles des classes précédentes (Seconde, Première).",
#         "recommandations": [
#           {
#             "type_ressource": "Site web",
#             "titre": "Physique-Chimie Lycée - Khan Academy",
#             "lien": "https://fr.khanacademy.org/science/physics",
#             "description": "Khan Academy propose des cours très structurés, partant des bases. N'aie pas peur de revoir des notions de Seconde ou Première si nécessaire. C'est la meilleure façon de reconstruire des fondations solides."
#           },
#           {
#             "type_ressource": "Livre",
#             "titre": "Collection CIAM (ou autre manuel scolaire de Tle C)",
#             "lien": "null",
#             "description": "Procure-toi un manuel avec des exercices corrigés. Refais les exercices d'application de chaque leçon jusqu'à ce que tu les maîtrises parfaitement."
#           }
#         ]
#       }
#     ],
#     "recommandations_generales": "Bonjour"
#   },
#   {
#     "id_student": "pPNdWPcN",
#     "class": "4ème1",
#     "summary": "Salut ! Tes résultats sont bons et très homogènes, c'est super ! Tu as un profil sérieux et équilibré. Tu disposes de bases solides dans toutes les matières, ce qui est idéal pour la suite de ta scolarité. Continue ce travail régulier, c'est la bonne méthode !",
#     "matieres": [
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 12.27,
#         "coefficient": 1,
#         "evaluation_personnalisee": "C'est un bon résultat. Tu as de bonnes bases. Pour progresser, essaie de participer un peu plus à l'oral en classe pour gagner en confiance.",
#         "recommandations": []
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 12.5,
#         "coefficient": 1,
#         "evaluation_personnalisee": "C'est une bonne moyenne qui montre que tu comprends bien les leçons. Pour t'améliorer encore, assure-toi de bien apprendre tes formules et définitions par cœur.",
#         "recommandations": [
#           {
#             "type_ressource": "Site web",
#             "titre": "Exercices de Maths 4ème - SchoolMouv",
#             "lien": "https://www.schoolmouv.fr/quatrieme/mathematiques",
#             "description": "Ce site propose des fiches de cours et des quiz pour réviser de manière interactive. C'est un bon complément à tes cours."
#           }
#         ]
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 12.75,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Très bien ! Tes résultats montrent une bonne compréhension des phénomènes étudiés. Continue d'être précis dans tes observations et tes conclusions.",
#         "recommandations": []
#       }
#     ],
#     "recommandations_generales": "Bonjour"
#   },
#   {
#     "id_student": "DoUaWltF",
#     "class": "Terminale C1",
#     "summary": "Salut ! Tu présentes un profil scientifique très solide avec d'excellents résultats en Physique-Chimie et de bons résultats en Maths. C'est parfait pour une Terminale C ! Ta LV2 est au niveau. Tu as toutes les cartes en main pour réussir brillamment ton Baccalauréat. Félicitations !",
#     "matieres": [
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 10.0,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Tu as juste la moyenne, c'est bien. Tu assures l'essentiel dans cette matière, ce qui te permet de te concentrer sur les matières à fort coefficient.",
#         "recommandations": []
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 12.67,
#         "coefficient": 5,
#         "evaluation_personnalisee": "C'est un bon résultat dans une matière exigeante. Tu as de solides acquis. Vise à gagner en rapidité et en précision lors des devoirs pour aller chercher les points bonus.",
#         "recommandations": [
#            {
#             "type_ressource": "PDF / Annales",
#             "titre": "Sujets de Bac C Côte d'Ivoire",
#             "lien": "https://reviser.ci/sujets-bac-serie-c-cote-divoire/",
#             "description": "Le site Reviser.ci compile de nombreux sujets et corrigés du Bac ivoirien. T'entraîner en conditions réelles est le meilleur moyen de préparer l'examen."
#           }
#         ]
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 14.0,
#         "coefficient": 5,
#         "evaluation_personnalisee": "Excellent travail ! C'est une moyenne qui démontre une très bonne maîtrise de la matière. Continue de bien travailler la méthodologie et la rédaction pour viser encore plus haut le jour de l'épreuve.",
#         "recommandations": []
#       }
#     ],
#     "recommandations_generales": "Bonjour"
#   },
#   {
#     "id_student": "rF2c2lOo",
#     "class": "4ème1",
#     "summary": "Salut. Je vois que tes résultats en matières scientifiques sont très faibles et c'est certainement une source de stress pour toi. Il est très important de comprendre ce qui bloque. En revanche, tu as un bon niveau en Langue Vivante 2. Ne te décourage surtout pas, les difficultés sont faites pour être surmontées. On va trouver des solutions ensemble.",
#     "matieres": [
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 12.92,
#         "coefficient": 1,
#         "evaluation_personnalisee": "C'est très bien ! Tu as des facilités dans cette matière, c'est un point fort sur lequel tu peux t'appuyer. Bravo !",
#         "recommandations": []
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 0.5,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Cette note montre qu'il y a un blocage complet avec la matière. Il faut absolument reprendre les bases des classes précédentes (6ème, 5ème). L'objectif n'est pas de viser 15 tout de suite, mais de comprendre à nouveau le cours et de réussir quelques exercices simples.",
#         "recommandations": [
#           {
#             "type_ressource": "Vidéo YouTube",
#             "titre": "Maths 6ème - Les fondamentaux",
#             "lien": "https://www.youtube.com/playlist?list=PLVUDmbpupCa5dC4vKY4T3j_rfXGZ_3j_3",
#             "description": "N'aie pas honte de revenir aux bases. Cette playlist de Yvan Monka pour la 6ème t'aidera à revoir les opérations, les fractions... C'est essentiel pour reconstruire tes connaissances."
#           },
#            {
#             "type_ressource": "Site web",
#             "titre": "Khan Academy - Mission de démarrage Maths",
#             "lien": "https://fr.khanacademy.org/math",
#             "description": "Le site te propose un test de démarrage pour identifier tes lacunes et te propose ensuite des exercices adaptés. C'est un excellent point de départ."
#           }
#         ]
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 3.75,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Comme en maths, il y a de grandes difficultés. Souvent, les problèmes en physique viennent d'un manque de bases en mathématiques. En travaillant les maths, tu devrais voir des progrès aussi en physique.",
#         "recommandations": [
#           {
#             "type_ressource": "Vidéo YouTube",
#             "titre": "Playlist Physique-Chimie Collège - Les Bons Profs",
#             "lien": "https://www.youtube.com/user/lesbonsprofs/playlists",
#             "description": "Cherche les playlists pour le niveau collège. Les vidéos sont visuelles et aident à comprendre les expériences et les concepts de base."
#           }
#         ]
#       }
#     ],
#     "recommandations_generales": "Bonjour"
#   },
#   {
#     "id_student": "mx4PJ7Yf",
#     "class": "Terminale C1",
#     "summary": "Salut ! Tes résultats en sciences sont spectaculaires, surtout en Physique-Chimie où tu excelles. C'est un profil idéal pour la Terminale C. Ton niveau en Mathématiques est également très bon. Le seul petit point faible est la Langue Vivante 2. En améliorant cette matière, ton bulletin sera quasi parfait. Excellent parcours, tu es promis à un grand succès !",
#     "matieres": [
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 8.0,
#         "coefficient": 1,
#         "evaluation_personnalisee": "C'est ton point faible actuellement. Même si le coefficient est bas, remonter cette note au-dessus de 10 te mettrait à l'abri et te donnerait plus de marge pour le Bac.",
#         "recommandations": [
#           {
#             "type_ressource": "Site web",
#             "titre": "BBC Learning English",
#             "lien": "https://www.bbc.co.uk/learningenglish",
#             "description": "Si ta LV2 est l'anglais, ce site est une mine d'or. Il propose des leçons basées sur l'actualité, des points de grammaire, etc. Très efficace pour progresser."
#           }
#         ]
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 12.58,
#         "coefficient": 5,
#         "evaluation_personnalisee": "Très bon travail en Maths. C'est une base solide pour le Bac. Tu maîtrises les concepts. Pour atteindre le niveau de la Physique, sois intraitable sur la rigueur de tes démonstrations.",
#         "recommandations": []
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 17.25,
#         "coefficient": 5,
#         "evaluation_personnalisee": "Félicitations, c'est un résultat exceptionnel ! Tu as une maîtrise remarquable de la matière. Tu fais sans doute partie des meilleurs. Continue de nourrir ta curiosité, c'est fantastique.",
#         "recommandations": [
#            {
#             "type_ressource": "Livre",
#             "titre": "Physique - Harris Benson",
#             "lien": "null",
#             "description": "Puisque tu as un niveau si élevé, tu pourrais apprécier un livre de niveau supérieur (début post-bac) pour approfondir les concepts. C'est juste pour ta curiosité, si le temps te le permet."
#           }
#         ]
#       }
#     ],
#     "recommandations_generales": "Bonjour"
#   },
#   {
#     "id_student": "qSG0Hf1h",
#     "class": "Terminale C1",
#     "summary": "Salut ! Quel excellent profil pour une Terminale C ! Tu es brillant en Physique-Chimie et très bon en Mathématiques. Ce sont les deux piliers de ta série et tu les maîtrises parfaitement. Ta LV2 est également à un bon niveau. Tu es parfaitement préparé pour les épreuves du Bac. Bravo pour ce parcours exemplaire !",
#     "matieres": [
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 13.75,
#         "coefficient": 1,
#         "evaluation_personnalisee": "Très bien ! C'est un excellent résultat qui montre que tu es un élève complet et sérieux.",
#         "recommandations": []
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 12.5,
#         "coefficient": 5,
#         "evaluation_personnalisee": "C'est un très bon résultat. Tu as de solides compétences. Continue à t'entraîner régulièrement sur des exercices type Bac pour être de plus en plus à l'aise avec le format des épreuves.",
#         "recommandations": []
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 16.0,
#         "coefficient": 5,
#         "evaluation_personnalisee": "Remarquable ! C'est une excellente moyenne qui prouve ta parfaite maîtrise des notions et de la méthode. C'est un atout considérable pour ton dossier et pour le Bac.",
#         "recommandations": [
#           {
#             "type_ressource": "Vidéo YouTube",
#             "titre": "Chaîne 'Professeur Geek'",
#             "lien": "https://www.youtube.com/c/ProfesseurGeek",
#             "description": "Pour un élève de ton niveau, les vidéos de cette chaîne peuvent être intéressantes pour aller un peu plus loin et voir des applications concrètes de ce que tu étudies en cours."
#           }
#         ]
#       }
#     ],
#     "recommandations_generales": "Bonjour"
#   }
# ]
#
# # db_connection = connections["default"]
# # with db_connection.cursor() as cursor:
# #     # Création de la table
# #     cursor.execute("""
# #         CREATE TABLE IF NOT EXISTS students_performances (
# #             id_student TEXT PRIMARY KEY,
# #             summary TEXT,
# #             matieres JSONB,
# #             recommandations_generales TEXT
# #         );
# #     """)
# #
# #     # Insertion des données
# #     for stud in students:
# #         cursor.execute("""
# #             INSERT INTO students_performances (id_student, summary, matieres, recommandations_generales)
# #             VALUES (%s, %s, %s, %s)
# #             ON CONFLICT (id_student) DO UPDATE SET
# #                 summary = EXCLUDED.summary,
# #                 matieres = EXCLUDED.matieres,
# #                 recommandations_generales = EXCLUDED.recommandations_generales;
# #         """, [
# #             stud.get("id_student"),
# #             stud.get("summary"),
# #             json.dumps(stud.get("matieres")),
# #             stud.get("recommandations_generales")
# #         ])
#
#
# text = """```json
# [
#   {
#     "id_student": "DTuE9QBF",
#     "class": "TerminaleC1",
#     "summary": "Salut ! Tes résultats en matières scientifiques sont vraiment bons, surtout en maths. C'est excellent pour une Terminale C ! Tu es sur la bonne voie pour le BAC. Un petit effort en Langue Vivante 2 te permettrait de gagner des points précieux et d'avoir un dossier encore plus solide. Continue comme ça !",
#     "recommendations": [
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 13.5,
#         "coefficient": 5,
#         "type_ressource": "site_web",
#         "titre": "Annales de Maths - BAC C Côte d'Ivoire",
#         "lien": "https://reviser.ci/sujets/mathematiques-terminale-c-cote-divoire/",
#         "description": "Ce site propose des sujets d'anciens examens du BAC C ivoirien avec leurs corrigés. C'est la meilleure façon de te préparer en conditions réelles.",
#         "motivation": "Ta moyenne est déjà bonne. Pour viser l'excellence et t'assurer une mention, t'entraîner sur de vrais sujets de BAC est indispensable."
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 11.0,
#         "coefficient": 5,
#         "type_ressource": "vidéo_youtube",
#         "titre": "Playlists de Terminale - Hedacademy",
#         "lien": "https://www.youtube.com/@Hedacademy/playlists",
#         "description": "Cette chaîne propose des cours très clairs et des exercices corrigés en vidéo sur tout le programme de Terminale. Idéal pour revoir un chapitre que tu n'as pas totalement maîtrisé.",
#         "motivation": "Tu as la moyenne, mais cette matière a un coefficient 5. Renforcer ta compréhension sur certains chapitres peut facilement faire grimper ta moyenne générale."
#       },
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 9.5,
#         "coefficient": 1,
#         "type_ressource": "application",
#         "titre": "Duolingo",
#         "lien": "https://fr.duolingo.com/",
#         "description": "Une application ludique pour pratiquer la langue 10 à 15 minutes par jour. Parfait pour améliorer ton vocabulaire et tes bases en grammaire de manière régulière.",
#         "motivation": "Ta moyenne est juste en dessous de 10. Un peu de pratique quotidienne te permettra de passer ce cap et de sécuriser des points pour le BAC sans que cela ne te prenne trop de temps."
#       }
#     ],
#     "recommandations_generales": "Ta base en sciences est solide, c'est ton plus grand atout. Continue de t'entraîner régulièrement avec des annales du BAC. Pour la LV2, essaie de regarder des films ou des séries en VO sous-titrée, c'est un excellent moyen de progresser sans avoir l'impression de travailler. Tu es bien parti, ne relâche pas tes efforts !"
#   },
#   {
#     "id_student": "igTdgm8X",
#     "class": "4ème1",
#     "summary": "Félicitations ! Tes résultats sont excellents dans toutes les matières. Tu as de grandes facilités et tu es très sérieux/sérieuse dans ton travail. C'est formidable ! Pour aller encore plus loin, tu peux commencer à explorer des sujets un peu plus avancés ou découvrir de nouvelles façons d'apprendre.",
#     "recommendations": [
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 15.0,
#         "coefficient": 1,
#         "type_ressource": "site_web",
#         "titre": "Khan Academy - Niveau 4ème",
#         "lien": "https://fr.khanacademy.org/math/4e",
#         "description": "Cette plateforme gratuite te permet de revoir tes leçons mais aussi d'explorer des notions mathématiques de manière interactive et plus approfondie. Parfait pour nourrir ta curiosité.",
#         "motivation": "Puisque tu maîtrises déjà très bien le programme, Khan Academy te permettra de prendre de l'avance et de satisfaire ta curiosité intellectuelle."
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 15.5,
#         "coefficient": 1,
#         "type_ressource": "vidéo_youtube",
#         "titre": "L'Esprit Sorcier",
#         "lien": "https://www.youtube.com/@LEspritSorcierOfficiel",
#         "description": "Cette chaîne de vulgarisation scientifique de grande qualité explique des phénomènes de physique et de chimie de la vie de tous les jours. C'est une façon passionnante de voir l'application concrète de ce que tu apprends en classe.",
#         "motivation": "Tes excellents résultats montrent que tu aimes les sciences. Cette chaîne te permettra de développer ta culture scientifique au-delà du programme scolaire."
#       }
#     ],
#     "recommandations_generales": "Continue sur cette magnifique lancée ! Ton secret, c'est la régularité. N'hésite pas à poser des questions en classe pour aller plus loin que le cours. Tu peux aussi lire des livres ou des magazines de vulgarisation scientifique pour nourrir ta curiosité. Bravo encore !"
#   },
#   {
#     "id_student": "D5dm4MNV",
#     "class": "TerminaleC1",
#     "summary": "Salut. Je vois que tu as un excellent niveau en Langue Vivante 2, c'est un vrai atout ! Par contre, tes résultats en Physique-Chimie sont très préoccupants, surtout en Terminale C où c'est une matière clé. Il est urgent de te concentrer dessus. En Maths, tu as les bases, mais il faut les renforcer. Ne te décourage pas, avec un plan de travail ciblé, tu peux remonter la pente !",
#     "recommendations": [
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 3.5,
#         "coefficient": 5,
#         "type_ressource": "vidéo_youtube",
#         "titre": "Cours de Physique-Chimie Terminale - Les Bons Profs",
#         "lien": "https://www.youtube.com/playlist?list=PL1BFr2xZgV5FOfY3a5yTf7k2y32u4TjE-",
#         "description": "Cette playlist reprend tout le programme de Terminale, point par point. Les vidéos sont courtes et très claires. Il faut absolument que tu reprennes les bases des chapitres où tu as des difficultés.",
#         "motivation": "Avec une moyenne de 3.5 et un coefficient 5, cette matière met ton année en danger. Il faut une action choc. Reprendre les cours depuis le début avec un support vidéo simple est la première étape indispensable."
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 3.5,
#         "coefficient": 5,
#         "type_ressource": "livre",
#         "titre": "Collection Excellence ou Durande - Physique Chimie Tle C",
#         "lien": "Disponible dans les librairies en Côte d'Ivoire.",
#         "description": "Ces manuels sont des références en Côte d'Ivoire. Ils contiennent des résumés de cours clairs et surtout de très nombreux exercices corrigés, étape par étape. C'est essentiel pour t'entraîner.",
#         "motivation": "Après avoir revu le cours en vidéo, tu dois absolument passer à la pratique. Faire et refaire des exercices est le seul moyen de progresser et de maîtriser les méthodes."
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 11.17,
#         "coefficient": 5,
#         "type_ressource": "site_web",
#         "titre": "Maths et Tiques - Yvan Monka",
#         "lien": "https://www.maths-et-tiques.fr/index.php/cours-maths/niveau-terminale",
#         "description": "Le site du professeur Yvan Monka propose des fiches de cours et des vidéos pour chaque chapitre. C'est une excellente ressource pour consolider tes bases et t'assurer de ne pas perdre de points.",
#         "motivation": "Ta moyenne est juste au-dessus de 10. Comme le coefficient est très élevé, chaque point gagné ici est crucial. Ce site t'aidera à sécuriser tes connaissances."
#       }
#     ],
#     "recommandations_generales": "La priorité absolue est la Physique-Chimie. Consacre-lui au moins une heure de travail chaque jour. Reprends les chapitres depuis le début de l'année. N'aie pas honte d
# e demander de l'aide à ton professeur ou à des camarades. Forme un groupe de travail. Pour le BAC, chaque point en PC et Maths vaudra 5 fois plus que tes points en LV2. Ta réussite dépend de ta capacité à redresser la barre dans les matières scientifiques. Tu peux le faire !"
#   },
#   {
#     "id_student": "pPNdWPcN",
#     "class": "4ème1",
#     "summary": "Bonjour ! Tes résultats sont bons et bien équilibrés. C'est une base solide pour la suite de tes études. Tu montres que tu es capable de réussir dans toutes les matières. Pour passer au niveau supérieur, tu peux chercher à approfondir certains points et à t'assurer que toutes les leçons sont bien maîtrisées.",
#     "recommendations": [
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 12.5,
#         "coefficient": 1,
#         "type_ressource": "site_web",
#         "titre": "Exercices de Maths 4ème - School-CI",
#         "lien": "https://www.school-ci.com/mathematiques-4eme/",
#         "description": "Ce site ivoirien propose des exercices et des devoirs qui correspondent bien au programme. C'est un bon moyen de t'entraîner et de vérifier que tu as bien compris tes leçons.",
#         "motivation": "Tu as une bonne moyenne. Pour la faire progresser, rien de tel que la pratique régulière avec des exercices ciblés sur ton programme."
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 12.75,
#         "coefficient": 1,
#         "type_ressource": "vidéo_youtube",
#         "titre": "Physique-Chimie au Collège",
#         "lien": "https://www.youtube.com/@physique-chimieaucollege/playlists",
#         "description": "Cette chaîne est spécialisée dans le programme de collège. Les vidéos sont très visuelles et peuvent t'aider à mieux comprendre les expériences et les concepts parfois abstraits.",
#         "motivation": "Tes résultats sont bons. Regarder des vidéos peut t'aider à consolider tes acquis et à rendre la matière plus concrète et intéressante."
#       }
#     ],
#     "recommandations_generales": "Continue ton travail régulier. Avant chaque évaluation, assure-toi de refaire les exercices vus en classe. Fais des fiches de résumé pour les leçons importantes. Tu as le potentiel pour atteindre des moyennes de 14 ou 15, ne lâche rien !"
#   },
#   {
#     "id_student": "DoUaWltF",
#     "class": "TerminaleC1",
#     "summary": "Salut ! Tu as un profil scientifique solide et équilibré. Tes moyennes en Maths et Physique-Chimie sont bonnes et te placent sur une excellente trajectoire pour le BAC. C'est très bien ! Continue de travailler régulièrement pour maintenir ce niveau jusqu'à l'examen.",
#     "recommendations": [
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 14.0,
#         "coefficient": 5,
#         "type_ressource": "pdf",
#         "titre": "Sujets Corrigés de Physique-Chimie - BAC C",
#         "lien": "https://reviser.ci/sujets/physique-chimie-terminale-c-cote-divoire/",
#         "description": "Entraîne-toi avec les sujets des années précédentes. Cela te familiarisera avec le format de l'épreuve et les types de questions posées. C'est le meilleur entraînement possible.",
#         "motivation": "Avec 14 de moyenne, tu vises clairement une mention. La maîtrise des annales est ce qui fait la différence entre un bon élève et un excellent candidat au BAC."
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 12.67,
#         "coefficient": 5,
#         "type_ressource": "vidéo_youtube",
#         "titre": "Chaîne d'Yvan Monka",
#         "lien": "https://www.youtube.com/@YvanMonka",
#         "description": "Même avec une bonne moyenne, il y a peut-être un ou deux chapitres que tu maîtrises moins. La chaîne de Yvan Monka est parfaite pour une révision ciblée et efficace sur un point précis.",
#         "motivation": "Transformer ton 12.67 en 14 ou 15 est tout à fait possible. Identifier tes petites faiblesses et les travailler avec ces vidéos te fera gagner de précieux points."
#       }
#     ],
#     "recommandations_generales": "Tu as un très bon profil. L'enjeu pour toi est la régularité et la préparation à l'examen final. Planifie tes révisions, travaille avec les annales et ne fais aucune impasse. Tu as toutes les cartes en main pour une belle réussite au BAC."
#   },
#   {
#     "id_student": "rF2c2lOo",
#     "class": "4ème1",
#     "summary": "Bonjour. Je vois que tes résultats en sciences sont très faibles et c'est certainement une source de difficultés pour toi. Il ne faut surtout pas te décourager ! Ces notes montrent qu'il
#  y a des bases importantes qui ne sont pas acquises. La bonne nouvelle, c'est qu'en reprenant les choses calmement depuis le début, tu peux tout à fait remonter la pente. On va trouver un plan d'action ensemble.",
#     "recommendations": [
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 0.5,
#         "coefficient": 1,
#         "type_ressource": "site_web",
#         "titre": "Khan Academy - Niveau 6ème et 5ème",
#         "lien": "https://fr.khanacademy.org/math",
#         "description": "Il faut être honnête, une note si basse en 4ème signifie que les bases des années précédentes (6ème, 5ème) ne sont pas là. Ce site te permet de revoir les fractions, les opérations, la géométrie de base, de manière simple et à ton rythme.",
#         "motivation": "C'est une urgence. Tu dois reconstruire tes fondations en mathématiques. Oublie le programme de 4ème pour l'instant et passe 2-3 semaines à refaire les exercices de 6ème/5ème. C'est la seule solution pour pouvoir ensuite comprendre les nouveaux cours."
#       },
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 3.75,
#         "coefficient": 1,
#         "type_ressource": "vidéo_youtube",
#         "titre": "Playlists de 5ème/4ème - Physique-Chimie au Collège",
#         "lien": "https://www.youtube.com/@physique-chimieaucollege/playlists",
#         "description": "Cette chaîne explique très simplement les notions de base. Regarde les vidéos pour les niveaux 5ème et 4ème. Le format visuel t'aidera peut-être plus qu'un livre.",
#         "motivation": "Comme pour les maths, il faut revoir les bases. Les vidéos peuvent rendre la matière moins intimidante et t'aider à comprendre les concepts fondamentaux (états de la matière, circuits électriques simples, etc.)."
#       }
#     ],
#     "recommandations_generales": "Ta priorité absolue est de parler à tes professeurs de Mathématiques et de Physique-Chimie. Explique-leur tes difficultés. Ils sont là pour t'aider. Ne reste pas seul(e) avec ce problème. Demande aussi de l'aide à un camarade qui comprend bien. Il faut accepter de revenir en arrière pour mieux avancer. Courage, chaque petite progression sera une grande victoire !"
#   },
#   {
#     "id_student": "mx4PJ7Yf",
#     "class": "TerminaleC1",
#     "summary": "Salut ! Tes résultats en Physique-Chimie sont exceptionnels, bravo ! C'est un atout majeur pour la Terminale C. Ta moyenne en Maths est également bonne. Ton profil scientifique est très prometteur. Le seul point à améliorer est la Langue Vivante 2, où tu peux facilement gagner des points pour viser une très belle mention au BAC.",
#     "recommendations": [
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 17.25,
#         "coefficient": 5,
#         "type_ressource": "livre",
#         "titre": "Physique/Chimie - Enseignement Supérieur (pour la curiosité)",
#         "lien": "Disponible en librairie ou bibliothèque universitaire.",
#         "description": "Vu ton excellent niveau, tu peux commencer à feuilleter des manuels de première année d'études supérieures (Prépa, Licence) pour voir à quoi ressemblent les sciences après le BAC. Cela peut être très motivant.",
#         "motivation": "Ton niveau dépasse déjà les attentes de la Terminale. Nourrir ta curiosité avec des contenus plus avancés te préparera pour la suite et maintiendra ta motivation au plus haut."
#       },
#       {
#         "matiere": "Langue Vivante 2",
#         "moyenne": 8.0,
#         "coefficient": 1,
#         "type_ressource": "site_web",
#         "titre": "Kartable - Fiches de cours et exercices",
#         "lien": "https://www.kartable.fr/",
#         "description": "Ce site propose des fiches de grammaire et de vocabulaire très bien structurées. Fixe-toi l'objectif de revoir un point de grammaire par semaine et d'apprendre 10 mots de vocabulaire.",
#         "motivation": "Avec un coefficient 1, chaque point est facile à prendre. Passer de 8 à 12 est beaucoup plus simple que de passer de 17 à 18 en sciences. C'est une stratégie intelligente pour augmenter ta moyenne générale."
#       }
#     ],
#     "recommandations_generales": "Tu as un profil d'excellence en sciences. Ne change rien à ta méthode de travail dans ces matières. Concentre une petite partie de tes efforts sur la LV2 : 20 minutes, 3 fois par semaine, suffiront à faire une vraie différence. Pense au BAC : ces quelques points 'faciles' peuvent te faire gagner une mention."
#   },
#   {
#     "id_student": "qSG0Hf1h",
#     "class": "TerminaleC1",
#     "summary": "Félicitations ! Tu présentes un excellent dossier de Terminale C, avec de très solides compétences dans les matières scientifiques et un bon niveau en langue. C'est un profil très complet et très recherché. Tu es parfaitement en route pour une mention au BAC. L'objectif est de maintenir ce cap !",
#     "recommendations": [
#       {
#         "matiere": "Physique-Chimie",
#         "moyenne": 16.0,
#         "coefficient": 5,
#         "type_ressource": "pdf",
#         "titre": "Annales Corrigées du BAC C - Reviser.ci",
#         "lien": "https://reviser.ci/sujets/physique-chimie-terminale-c-cote-divoire/",
#         "description": "Avec un tel niveau, la clé est la maîtrise parfaite des épreuves du BAC. Fais un maximum de sujets en conditions réelles (temps limité, sans aide) pour identifier les derniers détails à perfectionner.",
#         "motivation": "Tu ne vises plus seulement la réussite, mais l'excellence. L'entraînement intensif sur des sujets réels est la meilleure préparation pour le jour J et pour viser les meilleures notes."
#       },
#       {
#         "matiere": "Mathématiques",
#         "moyenne": 12.5,
#         "coefficient": 5,
#         "type_ressource": "vidéo_youtube",
#         "titre": "Exercices d'approfondissement - ExoTube",
#         "lien": "https://www.youtube.com/@ExoTube",
#         "description": "Cette chaîne propose des exercices souvent plus difficiles que la moyenne, ce qui est un excellent moyen de te challenger et de t'assurer que tu maîtrises les concepts en profondeur.",
#         "motivation": "Ta moyenne en maths est bonne, mais c'est là que tu as la plus grande marge de progression pour aller chercher une mention Très Bien. Te confronter à des exercices plus durs te rendra plus fort."
#       }
#     ],
#     "recommandations_generales": "Continue ton excellent travail. Ton sérieux et ta régularité paient. Pour la dernière ligne droite avant le BAC, organise bien tes révisions, fais des fiches de synthèse pour les formules et les définitions importantes. Pense aussi à te reposer pour arriver en pleine forme aux examens. Bravo !"
#   }
# ]
# ```"""
#
# import re
# students_performances = text.replace("```", "").replace("json", "")
# cleaned_json = re.sub(r'[\x00-\x1F\x7F]', '', students_performances.strip())
# students_list = json.loads(cleaned_json)
#
# # Maintenant students_list est une liste Python que vous pouvez manipuler
# for student in students_list:
#   print(student.get('recommendations'))
#   break
# print(len(students_list))   # Nombre d'étudiants dans la liste