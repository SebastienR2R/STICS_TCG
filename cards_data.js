// Fichier genere par generate_cards.py - ne pas editer a la main.
// Source de verite : cards_manifest.json
const CARDS_DB = {
    "common": [
        {
            "id": "001",
            "name": "Kraus",
            "emoji": "🎺",
            "image": "images/001Kraus.jpg"
        },
        {
            "id": "002",
            "name": "Braus",
            "emoji": "🎺",
            "image": "images/002Braus.jpg"
        },
        {
            "id": "003",
            "name": "Naio",
            "emoji": "🎺",
            "image": "images/003Naio.jpg"
        },
        {
            "id": "007",
            "name": "Drais",
            "emoji": "🎺",
            "image": "images/007Drais.jpg"
        },
        {
            "id": "009",
            "name": "Criix",
            "emoji": "🎺",
            "image": "images/009Criix.jpg"
        },
        {
            "id": "010",
            "name": "Tays",
            "emoji": "🎺",
            "image": "images/010Tays.jpg"
        }
    ],
    "rare": [
        {
            "id": "004",
            "name": "Criio",
            "emoji": "🎺",
            "image": "images/004Criio.jpg"
        },
        {
            "id": "008",
            "name": "Vararis",
            "emoji": "🎺",
            "image": "images/008Vararis.jpg"
        }
    ],
    "epic": [
        {
            "id": "005",
            "name": "Wais",
            "emoji": "🎺",
            "image": "images/005Wais.jpg"
        }
    ],
    "legendary": [
        {
            "id": "006",
            "name": "Orrarar",
            "emoji": "🎺",
            "image": "images/006Orrarar.jpg"
        }
    ]
};

const CARDS_META = {
    "version": 1,
    "saveKey": "tma_gacha_v2",
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
    "foilRarities": [
        "epic",
        "legendary"
    ],
    "albums": {
        "stics_a": {
            "title": "STICS",
            "icon": "🎺",
            "sets": {
                "STICS 1": [
                    "001",
                    "002",
                    "003",
                    "004",
                    "005",
                    "006",
                    "007",
                    "008",
                    "009",
                    "010"
                ]
            }
        }
    }
};
