// Fichier genere par generate_cards.py - ne pas editer a la main.
// Source de verite : cards_manifest.json
const CARDS_DB = {
    "common": [
        {
            "id": "001",
            "name": ">",
            "emoji": "🎺",
            "image": "images/>_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Roulade de poignet",
                "power": 30
            },
            "description": "Répétition du kiosque, immobile depuis toujours."
        },
        {
            "id": "002",
            "name": "2BD0D",
            "emoji": "🎺",
            "image": "images/2BD0D_Peu commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Montée de poignet",
                "power": 20
            },
            "description": "Bord du parvis, verni depuis toujours."
        },
        {
            "id": "004",
            "name": "Arbre mort",
            "emoji": "🎺",
            "image": "images/Arbre mort_Commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Coup de manche",
                "power": 60
            },
            "description": "Bravoure immobile sur la dernière marche."
        },
        {
            "id": "005",
            "name": "Attention Grand V",
            "emoji": "🎺",
            "image": "images/Attention Grand V_Peu commun.jpg",
            "hp": 130,
            "attack": {
                "name": "Longue tenue",
                "power": 80
            },
            "description": "Silence du toit, trempé depuis toujours."
        },
        {
            "id": "006",
            "name": "Attention Y",
            "emoji": "🎺",
            "image": "images/Attention Y_Peu commun.jpg",
            "hp": 160,
            "attack": {
                "name": "Tempo tenu",
                "power": 100
            },
            "description": "Contretemps sec, Bâton de chef doré et Silence trempé."
        },
        {
            "id": "007",
            "name": "Aventurier",
            "emoji": "🎺",
            "image": "images/Aventurier_Commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Contretems de rue",
                "power": 30
            },
            "description": "Répétition dorée, Bravoure sèche et Tempo fier."
        },
        {
            "id": "009",
            "name": "Bambou",
            "emoji": "🎺",
            "image": "images/Bambou_Commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Cascade de coups",
                "power": 20
            },
            "description": "Bord du bateau, verni depuis toujours."
        },
        {
            "id": "010",
            "name": "Baton Apéro",
            "emoji": "🎺",
            "image": "images/Baton Apéro_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Sortie de manche",
                "power": 40
            },
            "description": "Rebond trempé à l'aube."
        },
        {
            "id": "012",
            "name": "Baton bien trié",
            "emoji": "🎺",
            "image": "images/Baton bien trié_Commun.jpg",
            "hp": 120,
            "attack": {
                "name": "Final au poignet",
                "power": 50
            },
            "description": "Fouet verni sur les toits."
        },
        {
            "id": "013",
            "name": "Baton coincé",
            "emoji": "🎺",
            "image": "images/Baton coincé_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Reprise de tempo",
                "power": 20
            },
            "description": "Bord usé les jours de fête."
        },
        {
            "id": "014",
            "name": "Baton croco dans l'eau",
            "emoji": "🎺",
            "image": "images/Baton croco dans l'eau_Commun.jpg",
            "hp": 70,
            "attack": {
                "name": "Point d'appui",
                "power": 40
            },
            "description": "Marche légère, Coup rêveur et Ronde fêlée."
        },
        {
            "id": "015",
            "name": "Baton D'anniversaire",
            "emoji": "🎺",
            "image": "images/Baton D'anniversaire_Peu commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Final au poignet",
                "power": 40
            },
            "description": "Passe usée sur les quais."
        },
        {
            "id": "018",
            "name": "Baton en cage",
            "emoji": "🎺",
            "image": "images/Baton en cage_Commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Bâton levé",
                "power": 30
            },
            "description": "Montée têtue du quai."
        },
        {
            "id": "019",
            "name": "Baton en soirée",
            "emoji": "🎺",
            "image": "images/Baton en soirée_Peu commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Tempo de bâton",
                "power": 30
            },
            "description": "Manche immobile après le dernier coup."
        },
        {
            "id": "020",
            "name": "Baton gris",
            "emoji": "🎺",
            "image": "images/Baton gris_Commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Montée de poignet",
                "power": 30
            },
            "description": "Tempo usé, Tempo trempé et Balancement muet."
        },
        {
            "id": "022",
            "name": "Baton magnum",
            "emoji": "🎺",
            "image": "images/Baton magnum_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Croisière des mains",
                "power": 20
            },
            "description": "Montée qui tourne le bateau à l'aube."
        },
        {
            "id": "024",
            "name": "Baton sur Yvette",
            "emoji": "🎺",
            "image": "images/ Baton sur Yvette_Peu commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Coup de manche",
                "power": 30
            },
            "description": "Balade vernie du faubourg."
        },
        {
            "id": "025",
            "name": "Baton table",
            "emoji": "🎺",
            "image": "images/Baton table_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Frappe de dos",
                "power": 20
            },
            "description": "Montée fêlée, Manche fêlé et Montée fêlée."
        },
        {
            "id": "027",
            "name": "Batonzooka",
            "emoji": "🎺",
            "image": "images/Batonzooka_Peu commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Frappe de dos",
                "power": 40
            },
            "description": "Cadence du canal, endormie depuis toujours."
        },
        {
            "id": "029",
            "name": "Belle bite",
            "emoji": "🎺",
            "image": "images/Belle bite_Peu commmun.jpg",
            "hp": 90,
            "attack": {
                "name": "Relance",
                "power": 30
            },
            "description": "Répétition trempée sur les portails."
        },
        {
            "id": "030",
            "name": "Bello bito",
            "emoji": "🎺",
            "image": "images/Bello bito_Peu commun.jpg",
            "hp": 70,
            "attack": {
                "name": "Final au poignet",
                "power": 40
            },
            "description": "Tempo du toit, endormi depuis toujours."
        },
        {
            "id": "031",
            "name": "Béquille en route",
            "emoji": "🎺",
            "image": "images/Béquille en route_Commun.jpg",
            "hp": 110,
            "attack": {
                "name": "Point final",
                "power": 40
            },
            "description": "Cadence du portail, endormie depuis toujours."
        },
        {
            "id": "032",
            "name": "Béquilles",
            "emoji": "🎺",
            "image": "images/Béquilles_commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Rebond sec",
                "power": 40
            },
            "description": "Coup qui claque le canal à la nuit tombée."
        },
        {
            "id": "033",
            "name": "Bien Armé",
            "emoji": "🎺",
            "image": "images/Bien Armé_Peu commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Contretems de rue",
                "power": 20
            },
            "description": "Passe du trottoir, vernie depuis toujours."
        },
        {
            "id": "034",
            "name": "Bof",
            "emoji": "🎺",
            "image": "images/Bof_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Roulade de poignet",
                "power": 30
            },
            "description": "Marche qui ravive le pont avant le passage."
        },
        {
            "id": "036",
            "name": "Branche morte",
            "emoji": "🎺",
            "image": "images/Branche morte_Commun.jpg",
            "hp": 100,
            "attack": {
                "name": "Double frappe",
                "power": 40
            },
            "description": "Cadence claire, Frappe solennelle et Contretemps endormi."
        },
        {
            "id": "040",
            "name": "Criix",
            "emoji": "🎺",
            "image": "images/009Criix.jpg",
            "hp": 80,
            "attack": {
                "name": "Frappe de dos",
                "power": 30
            },
            "description": "Bâton de chef du faubourg, solennel depuis toujours."
        },
        {
            "id": "041",
            "name": "Criterium",
            "emoji": "🎺",
            "image": "images/Criterium_Commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Roulade d'épaule",
                "power": 50
            },
            "description": "Balade qui balance le kiosque à la nuit tombée."
        },
        {
            "id": "042",
            "name": "Cuillère suspendu",
            "emoji": "🎺",
            "image": "images/Cuillère suspendu_Commun.jpg",
            "hp": 70,
            "attack": {
                "name": "Silence imposé",
                "power": 20
            },
            "description": "Frappe du parvis, nocturne depuis toujours."
        },
        {
            "id": "044",
            "name": "Diablotin",
            "emoji": "🎺",
            "image": "images/Diablotin_Peu commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Roulade d'épaule",
                "power": 40
            },
            "description": "Contretemps clair tout le long de la rue."
        },
        {
            "id": "046",
            "name": "Duo au bord du lac",
            "emoji": "🎺",
            "image": "images/Duo au bord du lac_Commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Fouet du chef",
                "power": 40
            },
            "description": "Bâton qui danse le parvis après le dernier coup."
        },
        {
            "id": "050",
            "name": "Epee wtf",
            "emoji": "🎺",
            "image": "images/Epee wtf_Peu commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Roulade de poignet",
                "power": 30
            },
            "description": "Manche solennel, Passe fêlée et Cadence claire."
        },
        {
            "id": "051",
            "name": "Feu de bois",
            "emoji": "🎺",
            "image": "images/Feu de bois_peu commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Point d'appui",
                "power": 20
            },
            "description": "Rebond clair du trottoir."
        },
        {
            "id": "052",
            "name": "Flou artistique",
            "emoji": "🎺",
            "image": "images/081Flou artistique_Commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Coup de manche",
                "power": 20
            },
            "description": "Silence qui balance le toit sur la dernière marche."
        },
        {
            "id": "053",
            "name": "Flou sur Yvette",
            "emoji": "🎺",
            "image": "images/Flou sur Yvette_Commun.jpg",
            "hp": 70,
            "attack": {
                "name": "Relance",
                "power": 30
            },
            "description": "Bord du kiosque, fêlé depuis toujours."
        },
        {
            "id": "054",
            "name": "Forêt",
            "emoji": "🎺",
            "image": "images/Forêt_Commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Ostinato de bâton",
                "power": 30
            },
            "description": "Fouet qui signale le parvis après le dernier coup."
        },
        {
            "id": "057",
            "name": "Gamma",
            "emoji": "🎺",
            "image": "images/Gamma_Peu commun.jpg",
            "hp": 120,
            "attack": {
                "name": "Coup de manche",
                "power": 60
            },
            "description": "Silence sec du trottoir."
        },
        {
            "id": "059",
            "name": "Gif sur Baton",
            "emoji": "🎺",
            "image": "images/083 Gif sur Baton_Peu commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Rebond sec",
                "power": 40
            },
            "description": "Contretemps endormi, Tempo fêlé et Tempo rêveur."
        },
        {
            "id": "060",
            "name": "Gingembre ?",
            "emoji": "🎺",
            "image": "images/Gingembre ?_Commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Huit battements",
                "power": 20
            },
            "description": "Balade qui accélère le faubourg au milieu du silence."
        },
        {
            "id": "061",
            "name": "Gourdin",
            "emoji": "🎺",
            "image": "images/Gourdin_Peu Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Tempo tenu",
                "power": 40
            },
            "description": "Ronde claire du quai."
        },
        {
            "id": "065",
            "name": "Homme armé",
            "emoji": "🎺",
            "image": "images/Homme armé_Peu commun.jpg",
            "hp": 110,
            "attack": {
                "name": "Frappe de dos",
                "power": 50
            },
            "description": "Montée claire du quai."
        },
        {
            "id": "068",
            "name": "Le bout du bout",
            "emoji": "🎺",
            "image": "images/Le bout du bout_Commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Rebond sec",
                "power": 20
            },
            "description": "Rebond léger sur les bateaus."
        },
        {
            "id": "069",
            "name": "Le bucheron est passé",
            "emoji": "🎺",
            "image": "images/Le bucheron est passé_Commun.jpg",
            "hp": 100,
            "attack": {
                "name": "Coup de manche",
                "power": 50
            },
            "description": "Ronde du toit, sèche depuis toujours."
        },
        {
            "id": "070",
            "name": "Le chiffre 4",
            "emoji": "🎺",
            "image": "images/082 Le chiffre 4_Commun.jpg",
            "hp": 100,
            "attack": {
                "name": "Frappe sèche",
                "power": 40
            },
            "description": "Fouet têtu du trottoir."
        },
        {
            "id": "072",
            "name": "Le penseur",
            "emoji": "🎺",
            "image": "images/Le penseur_Peu Commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Final au poignet",
                "power": 30
            },
            "description": "Passe rêveuse à la nuit tombée."
        },
        {
            "id": "074",
            "name": "Long baton",
            "emoji": "🎺",
            "image": "images/Long baton_Peu commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Bâton en avant",
                "power": 40
            },
            "description": "Bâton têtu sur les trottoirs."
        },
        {
            "id": "077",
            "name": "MiniGun",
            "emoji": "🎺",
            "image": "images/MiniGun_Peu commun.jpg",
            "hp": 120,
            "attack": {
                "name": "Tempo tenu",
                "power": 80
            },
            "description": "Silence immobile au milieu du silence."
        },
        {
            "id": "078",
            "name": "Monsieur Crabe",
            "emoji": "🎺",
            "image": "images/Monsieur Crabe_Peu commun.jpg",
            "hp": 110,
            "attack": {
                "name": "Cascade de coups",
                "power": 60
            },
            "description": "Balancement endormi, Manche doré et Ronde immobile."
        },
        {
            "id": "079",
            "name": "Mouais...",
            "emoji": "🎺",
            "image": "images/Mouais..._Commun.jpg",
            "hp": 120,
            "attack": {
                "name": "Huit battements",
                "power": 60
            },
            "description": "Silence qui frappe le bateau quand la pluie tombe."
        },
        {
            "id": "081",
            "name": "Museum",
            "emoji": "🎺",
            "image": "images/Museum_Commun.jpg",
            "hp": 70,
            "attack": {
                "name": "Huit battements",
                "power": 30
            },
            "description": "Coup du faubourg, fêlé depuis toujours."
        },
        {
            "id": "083",
            "name": "Perche",
            "emoji": "🎺",
            "image": "images/Perche_Commun.jpg",
            "hp": 100,
            "attack": {
                "name": "Descente d'aile",
                "power": 40
            },
            "description": "Répétition dorée sur les trottoirs."
        },
        {
            "id": "084",
            "name": "Petit baton joyeux",
            "emoji": "🎺",
            "image": "images/Petit baton joyeux_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Frappe sèche",
                "power": 20
            },
            "description": "Montée du canal, sèche depuis toujours."
        },
        {
            "id": "085",
            "name": "Petit troncs gros troncs",
            "emoji": "🎺",
            "image": "images/Petit troncs gros troncs_Commun.jpg",
            "hp": 70,
            "attack": {
                "name": "Tempo tenu",
                "power": 40
            },
            "description": "Reprise fière, Cadence rêveuse et Bâton doré."
        },
        {
            "id": "086",
            "name": "Phasme",
            "emoji": "🎺",
            "image": "images/Phasme_peu commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Sortie de manche",
                "power": 30
            },
            "description": "Balancement doré, Bravoure lourde et Bord lourd."
        },
        {
            "id": "087",
            "name": "Pistolet",
            "emoji": "🎺",
            "image": "images/Pistolet_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Relance",
                "power": 40
            },
            "description": "Répétition du trottoir, claire depuis toujours."
        },
        {
            "id": "088",
            "name": "Pistolet de poche",
            "emoji": "🎺",
            "image": "images/Pistolet de poche_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Balancement lent",
                "power": 40
            },
            "description": "Silence immobile du parvis."
        },
        {
            "id": "090",
            "name": "Ptit bout d'bois",
            "emoji": "🎺",
            "image": "images/Ptit bout d'bois_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Double frappe",
                "power": 40
            },
            "description": "Bravoure claire, Répétition patiente et Rebond clair."
        },
        {
            "id": "091",
            "name": "Ptite branche",
            "emoji": "🎺",
            "image": "images/Ptite branche_Commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Rebond sec",
                "power": 20
            },
            "description": "Reprise qui danse le faubourg à la nuit tombée."
        },
        {
            "id": "095",
            "name": "Stick Minecraft",
            "emoji": "🎺",
            "image": "images/012Stick Minecraft_Commun.png",
            "hp": 100,
            "attack": {
                "name": "Double frappe",
                "power": 60
            },
            "description": "Bord patient sur les quais."
        },
        {
            "id": "100",
            "name": "Tas de buches",
            "emoji": "🎺",
            "image": "images/Tas de buches_Commun.jpg",
            "hp": 100,
            "attack": {
                "name": "Passage des mains",
                "power": 60
            },
            "description": "Contretemps du kiosque, endormi depuis toujours."
        },
        {
            "id": "101",
            "name": "Tout petit baton",
            "emoji": "🎺",
            "image": "images/005Tout petit baton_Commun.jpg",
            "hp": 80,
            "attack": {
                "name": "Relance",
                "power": 40
            },
            "description": "Montée du escalier, têtue depuis toujours."
        },
        {
            "id": "104",
            "name": "Tronc farfelue sur caillou",
            "emoji": "🎺",
            "image": "images/Tronc farfelue sur caillou_Commun.jpg",
            "hp": 100,
            "attack": {
                "name": "Coup de manche",
                "power": 60
            },
            "description": "Bâton de chef du portail, têtu depuis toujours."
        },
        {
            "id": "105",
            "name": "Tronc mort supplément feuille",
            "emoji": "🎺",
            "image": "images/Tronc mort supplément feuille_Commun.jpg",
            "hp": 60,
            "attack": {
                "name": "Reprise de tempo",
                "power": 30
            },
            "description": "Ronde qui ouvre le trottoir les jours de fête."
        },
        {
            "id": "109",
            "name": "Virgule",
            "emoji": "🎺",
            "image": "images/Virgule_Peu commun.jpg",
            "hp": 90,
            "attack": {
                "name": "Cascade de coups",
                "power": 60
            },
            "description": "Reprise sèche du trottoir."
        }
    ],
    "rare": [
        {
            "id": "003",
            "name": "Allemand tordu",
            "emoji": "🎺",
            "image": "images/Allemand tordu_Rare.jpg",
            "hp": 70,
            "attack": {
                "name": "Redoublement",
                "power": 40
            },
            "description": "Bord usé du toit."
        },
        {
            "id": "011",
            "name": "Baton artistique",
            "emoji": "🎺",
            "image": "images/Baton artistique_Rare.jpg",
            "hp": 60,
            "attack": {
                "name": "Croisière des mains",
                "power": 20
            },
            "description": "Contretemps qui frappe le portail quand la pluie tombe."
        },
        {
            "id": "016",
            "name": "Baton d'Asclépios",
            "emoji": "🎺",
            "image": "images/Baton d'Asclépios_Rare.jpg",
            "hp": 60,
            "attack": {
                "name": "Cascade de coups",
                "power": 30
            },
            "description": "Tempo clair à l'aube."
        },
        {
            "id": "023",
            "name": "Baton randonneur",
            "emoji": "🎺",
            "image": "images/Baton randonneur_Rare.jpg",
            "hp": 70,
            "attack": {
                "name": "Rebond croisé",
                "power": 40
            },
            "description": "Bâton de chef qui signale le square après le dernier coup."
        },
        {
            "id": "028",
            "name": "Batteur sous baton",
            "emoji": "🎺",
            "image": "images/Batteur sous baton_Rare.jpg",
            "hp": 70,
            "attack": {
                "name": "Balancement lent",
                "power": 40
            },
            "description": "Balancement nocturne pendant la descente."
        },
        {
            "id": "035",
            "name": "Bois de cerf",
            "emoji": "🎺",
            "image": "images/Bois de cerf_Rare.jpg",
            "hp": 60,
            "attack": {
                "name": "Silence imposé",
                "power": 40
            },
            "description": "Montée qui ferme le square quand la pluie tombe."
        },
        {
            "id": "037",
            "name": "Buche Rez 2",
            "emoji": "🎺",
            "image": "images/Buche Rez 2_Rare.jpg",
            "hp": 90,
            "attack": {
                "name": "Fouet du chef",
                "power": 40
            },
            "description": "Cadence vernie du trottoir."
        },
        {
            "id": "049",
            "name": "Entrepot",
            "emoji": "🎺",
            "image": "images/Entrepot_Rare.jpg",
            "hp": 60,
            "attack": {
                "name": "Roulade d'épaule",
                "power": 40
            },
            "description": "Coup trempé sur les trottoirs."
        },
        {
            "id": "056",
            "name": "Fresco loin",
            "emoji": "🎺",
            "image": "images/Fresco loin_Rare.jpg",
            "hp": 70,
            "attack": {
                "name": "Passage des mains",
                "power": 30
            },
            "description": "Passe du parvis, trempée depuis toujours."
        },
        {
            "id": "058",
            "name": "Gardien des bois",
            "emoji": "🎺",
            "image": "images/Gardien des bois_Rare.jpg",
            "hp": 90,
            "attack": {
                "name": "Rebond sec",
                "power": 30
            },
            "description": "Coup rêveur après le dernier coup."
        },
        {
            "id": "062",
            "name": "Grand baton de l'espoir",
            "emoji": "🎺",
            "image": "images/Grand baton de l'espoir_Rare.jpg",
            "hp": 80,
            "attack": {
                "name": "Tempo de bâton",
                "power": 40
            },
            "description": "Ronde immobile du escalier."
        },
        {
            "id": "063",
            "name": "Grand baton menaçant",
            "emoji": "🎺",
            "image": "images/Grand baton menaçant_rare.jpg",
            "hp": 60,
            "attack": {
                "name": "Passage des mains",
                "power": 20
            },
            "description": "Passe claire du quai."
        },
        {
            "id": "064",
            "name": "Grand Singe",
            "emoji": "🎺",
            "image": "images/Grand Singe_Rare.jpg",
            "hp": 80,
            "attack": {
                "name": "Huit battements",
                "power": 40
            },
            "description": "Silence léger sur la dernière marche."
        },
        {
            "id": "067",
            "name": "La triplette",
            "emoji": "🎺",
            "image": "images/La triplette_Rare.jpg",
            "hp": 150,
            "attack": {
                "name": "Cascade de coups",
                "power": 60
            },
            "description": "Fouet fêlé, Bravoure nocturne et Fouet lourd."
        },
        {
            "id": "073",
            "name": "Les habitants du Larzac",
            "emoji": "🎺",
            "image": "images/Les habitants du Larzac_Rare.jpg",
            "hp": 60,
            "attack": {
                "name": "Bâton en avant",
                "power": 30
            },
            "description": "Bord léger du parvis."
        },
        {
            "id": "075",
            "name": "Magie sur Yvette",
            "emoji": "🎺",
            "image": "images/Magie sur Yvette_Rare.jpg",
            "hp": 90,
            "attack": {
                "name": "Huit battements",
                "power": 20
            },
            "description": "Frappe trempée du faubourg."
        },
        {
            "id": "076",
            "name": "Mais dis donc bo baton",
            "emoji": "🎺",
            "image": "images/Mais dis donc bo baton_Rare.jpg",
            "hp": 120,
            "attack": {
                "name": "Reprise de tempo",
                "power": 60
            },
            "description": "Contretemps qui ouvre le trottoir après le dernier coup."
        },
        {
            "id": "080",
            "name": "Muni d'une grande arme",
            "emoji": "🎺",
            "image": "images/Muni d'une grande arme_Rare.jpg",
            "hp": 70,
            "attack": {
                "name": "Coup de manche",
                "power": 40
            },
            "description": "Bord nocturne, Passe fêlée et Montée sèche."
        },
        {
            "id": "089",
            "name": "Pistolet enneigé",
            "emoji": "🎺",
            "image": "images/Pistolet enneigé_Rare.jpg",
            "hp": 90,
            "attack": {
                "name": "Balancement lent",
                "power": 40
            },
            "description": "Répétition nocturne, Répétition lourde et Montée solennelle."
        },
        {
            "id": "092",
            "name": "Sceptre Doré",
            "emoji": "🎺",
            "image": "images/Sceptre Doré_Rare.jpg",
            "hp": 120,
            "attack": {
                "name": "Passage des mains",
                "power": 60
            },
            "description": "Balade vernie sur les canals."
        },
        {
            "id": "093",
            "name": "Seb Marathonien",
            "emoji": "🎺",
            "image": "images/Seb Marathonien_Rare.jpg",
            "hp": 110,
            "attack": {
                "name": "Bâton levé",
                "power": 60
            },
            "description": "Cadence dorée du canal."
        },
        {
            "id": "094",
            "name": "Smiley",
            "emoji": "🎺",
            "image": "images/Smiley_Rare.jpg",
            "hp": 60,
            "attack": {
                "name": "Coup de manche",
                "power": 40
            },
            "description": "Marche trempée sur les squares."
        },
        {
            "id": "096",
            "name": "Stick Minecraft 2",
            "emoji": "🎺",
            "image": "images/013 Stick Minecraft_Rare.png",
            "hp": 140,
            "attack": {
                "name": "Croisière des mains",
                "power": 60
            },
            "description": "Reprise endormie, Poignée fêlé et Poignée nocturne."
        },
        {
            "id": "097",
            "name": "Stock (Munich)",
            "emoji": "🎺",
            "image": "images/Stock (Munich)_Rare.jpg",
            "hp": 60,
            "attack": {
                "name": "Passage des mains",
                "power": 30
            },
            "description": "Bâton de chef solennel sur les trottoirs."
        },
        {
            "id": "098",
            "name": "Sun Wukong et son baton",
            "emoji": "🎺",
            "image": "images/Sun Wukong et son baton_Rare.jpg",
            "hp": 90,
            "attack": {
                "name": "Passage des mains",
                "power": 40
            },
            "description": "Bâton endormi, Marche rêveuse et Bâton de chef nocturne."
        },
        {
            "id": "099",
            "name": "T ancestral",
            "emoji": "🎺",
            "image": "images/T ancestral_Rare.jpg",
            "hp": 120,
            "attack": {
                "name": "Rebond sec",
                "power": 70
            },
            "description": "Répétition immobile, Coup nocturne et Cadence sèche."
        },
        {
            "id": "106",
            "name": "Troncs",
            "emoji": "🎺",
            "image": "images/Troncs_Rare.jpg",
            "hp": 100,
            "attack": {
                "name": "Montée de poignet",
                "power": 60
            },
            "description": "Bord doré sur les trottoirs."
        },
        {
            "id": "107",
            "name": "Troncs 2BD0D",
            "emoji": "🎺",
            "image": "images/Troncs 2BD0D_Rare.jpg",
            "hp": 110,
            "attack": {
                "name": "Redoublement",
                "power": 60
            },
            "description": "Marche nocturne, Répétition têtue et Bravoure claire."
        },
        {
            "id": "108",
            "name": "Troncs escalier bloqué",
            "emoji": "🎺",
            "image": "images/Troncs escalier bloqué_Rare.jpg",
            "hp": 90,
            "attack": {
                "name": "Roulade d'épaule",
                "power": 40
            },
            "description": "Bravoure fière du kiosque."
        }
    ],
    "epic": [
        {
            "id": "008",
            "name": "Baguette de Sorcier",
            "emoji": "🎺",
            "image": "images/112Baguette de Sorcier_Epique.jpg",
            "hp": 90,
            "attack": {
                "name": "Contretems de rue",
                "power": 40
            },
            "description": "Bravoure muette, Poignée nocturne et Bâton immobile."
        },
        {
            "id": "017",
            "name": "Baton de la cascade",
            "emoji": "🎺",
            "image": "images/Baton de la cascade_Epique.jpg",
            "hp": 60,
            "attack": {
                "name": "Ostinato de bâton",
                "power": 20
            },
            "description": "Bravoure solennelle, Marche nocturne et Bravoure rêveuse."
        },
        {
            "id": "021",
            "name": "Baton Magique",
            "emoji": "🎺",
            "image": "images/Baton Magique_Epique.jpg",
            "hp": 90,
            "attack": {
                "name": "Frappe sèche",
                "power": 40
            },
            "description": "Bâton lourd, Répétition usée et Montée sèche."
        },
        {
            "id": "026",
            "name": "Baton victorieux",
            "emoji": "🎺",
            "image": "images/Baton victorieux_Epique.jpg",
            "hp": 90,
            "attack": {
                "name": "Descente d'aile",
                "power": 40
            },
            "description": "Balade solennelle du kiosque."
        },
        {
            "id": "038",
            "name": "Capture epique",
            "emoji": "🎺",
            "image": "images/Capture epique_Epique.jpg",
            "hp": 60,
            "attack": {
                "name": "Reprise de tempo",
                "power": 30
            },
            "description": "Fouet immobile sur les quais."
        },
        {
            "id": "045",
            "name": "Dragon oriental",
            "emoji": "🎺",
            "image": "images/Dragon oriental_Epique.jpg",
            "hp": 150,
            "attack": {
                "name": "Sortie de manche",
                "power": 60
            },
            "description": "Cadence nocturne sur les portails."
        },
        {
            "id": "047",
            "name": "Duo Mystérieux",
            "emoji": "🎺",
            "image": "images/Duo Mystérieux_Epique.jpg",
            "hp": 70,
            "attack": {
                "name": "Rebond croisé",
                "power": 20
            },
            "description": "Fouet du faubourg, verni depuis toujours."
        },
        {
            "id": "048",
            "name": "Enfant ramassant biere",
            "emoji": "🎺",
            "image": "images/Enfant ramassant biere_Epique.jpg",
            "hp": 80,
            "attack": {
                "name": "Reprise de tempo",
                "power": 30
            },
            "description": "Frappe endormie du bateau."
        },
        {
            "id": "066",
            "name": "Jean Baton",
            "emoji": "🎺",
            "image": "images/Jean Baton_Epique.jpg",
            "hp": 70,
            "attack": {
                "name": "Roulade de poignet",
                "power": 20
            },
            "description": "Montée du square, patiente depuis toujours."
        },
        {
            "id": "082",
            "name": "Nyoï Bo (dragon ball)",
            "emoji": "🎺",
            "image": "images/111Nyoï Bo (dragon ball)_Epique.jpg",
            "hp": 70,
            "attack": {
                "name": "Descente d'aile",
                "power": 30
            },
            "description": "Contretemps endormi sur les canals."
        },
        {
            "id": "102",
            "name": "Tres grand baton (974)",
            "emoji": "🎺",
            "image": "images/Tres grand baton (974)_Epique.jpg",
            "hp": 120,
            "attack": {
                "name": "Montée de poignet",
                "power": 40
            },
            "description": "Tempo têtu quand la pluie tombe."
        },
        {
            "id": "103",
            "name": "Tres Tres Grand",
            "emoji": "🎺",
            "image": "images/Tres Tres Grand_Epique.jpg",
            "hp": 90,
            "attack": {
                "name": "Croisière des mains",
                "power": 30
            },
            "description": "Reprise du parvis, trempée depuis toujours."
        }
    ],
    "legendary": [
        {
            "id": "039",
            "name": "Christian Baton de Noël",
            "emoji": "🎺",
            "image": "images/088Christian Baton de Noël_Légendaire.jpg",
            "hp": 90,
            "attack": {
                "name": "Balancement lent",
                "power": 30
            },
            "description": "Cadence fière du portail."
        },
        {
            "id": "043",
            "name": "Daronne de Seb",
            "emoji": "🎺",
            "image": "images/Daronne de Seb_Légendaire.jpg",
            "hp": 90,
            "attack": {
                "name": "Rebond sec",
                "power": 40
            },
            "description": "Frappe dorée avant le passage."
        },
        {
            "id": "055",
            "name": "Fresco",
            "emoji": "🎺",
            "image": "images/087Fresco_Legendaire.jpg",
            "hp": 130,
            "attack": {
                "name": "Cascade de coups",
                "power": 90
            },
            "description": "Passe immobile sur les escaliers."
        },
        {
            "id": "071",
            "name": "Le Daron de Seb",
            "emoji": "🎺",
            "image": "images/016Le Daron de Seb_Légendaire.jpg",
            "hp": 120,
            "attack": {
                "name": "Passage des mains",
                "power": 90
            },
            "description": "Coup verni à la nuit tombée."
        }
    ]
};

const CARDS_META = {
    "version": 1,
    "saveKey": "tma_gacha_v3",
    "rarities": [
        "common",
        "rare",
        "epic",
        "legendary"
    ],
    "rarityLabels": {
        "common": "Commune",
        "rare": "Rare",
        "epic": "Épique",
        "legendary": "Légendaire"
    },
    "raritySymbols": {
        "common": "◆",
        "rare": "◆◆",
        "epic": "◆◆★",
        "legendary": "◆◆★★"
    },
    "rarityCss": {
        "common": "c",
        "rare": "r",
        "epic": "e",
        "legendary": "l"
    },
    "drawTable": {
        "standard": {
            "common": 82.0,
            "rare": 98.9,
            "epic": 99.9,
            "legendary": 100.0
        },
        "bonus": {
            "common": 60.0,
            "rare": 88.0,
            "epic": 99.0,
            "legendary": 100.0
        }
    },
    "albums": {
        "non_classe": {
            "title": "Non classé",
            "icon": "🗂",
            "sets": {
                "Non classé 1": [
                    "001",
                    "002",
                    "003",
                    "004",
                    "005",
                    "006",
                    "007",
                    "008",
                    "009",
                    "010",
                    "011",
                    "012"
                ],
                "Non classé 2": [
                    "013",
                    "014",
                    "015",
                    "016",
                    "017",
                    "018",
                    "019",
                    "020",
                    "021",
                    "022",
                    "023",
                    "024"
                ],
                "Non classé 3": [
                    "025",
                    "026",
                    "027",
                    "028",
                    "029",
                    "030",
                    "031",
                    "032",
                    "033",
                    "034",
                    "035",
                    "036"
                ],
                "Non classé 4": [
                    "037",
                    "038",
                    "039",
                    "040",
                    "041",
                    "042",
                    "043",
                    "044",
                    "045",
                    "046",
                    "047",
                    "048"
                ],
                "Non classé 5": [
                    "049",
                    "050",
                    "051",
                    "052",
                    "053",
                    "054",
                    "055",
                    "056",
                    "057",
                    "058",
                    "059",
                    "060"
                ],
                "Non classé 6": [
                    "061",
                    "062",
                    "063",
                    "064",
                    "065",
                    "066",
                    "067",
                    "068",
                    "069",
                    "070",
                    "071",
                    "072"
                ],
                "Non classé 7": [
                    "073",
                    "074",
                    "075",
                    "076",
                    "077",
                    "078",
                    "079",
                    "080",
                    "081",
                    "082",
                    "083",
                    "084"
                ],
                "Non classé 8": [
                    "085",
                    "086",
                    "087",
                    "088",
                    "089",
                    "090",
                    "091",
                    "092",
                    "093",
                    "094",
                    "095",
                    "096"
                ],
                "Non classé 9": [
                    "097",
                    "098",
                    "099",
                    "100",
                    "101",
                    "102",
                    "103",
                    "104",
                    "105",
                    "106",
                    "107",
                    "108"
                ],
                "Non classé 10": [
                    "109"
                ]
            }
        }
    }
};
