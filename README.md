# STICS_TCG
site de tcg pour Telegram
Voici le fichier `README.md` complet et documenté, prêt à être placé à la racine de ton dépôt GitHub pour guider le projet et tout futur développeur.

---

```markdown
# 🎺 TCG STICS — Telegram Mini App (TMA)

Jeu de cartes à collectionner (TCG / Gacha) 100 % Serverless conçu pour être exécuté nativement dans l'écosystème Telegram sous forme de **Telegram Mini App (TMA)** ou directement dans un navigateur moderne.

---

## 📁 Architecture du Dépôt

Le projet repose sur une architecture sans backend ("zero-backend"), hébergée directement via **GitHub Pages**.

```text
├── index.html          # Application complète (UI, logique gacha, shaders foil, stats)
├── cards_data.js       # FICHIER GÉNÉRÉ : CARDS_DB (cartes) + CARDS_META (config)
├── cards_manifest.json # SOURCE DE VÉRITÉ : ids, noms, raretés, albums, probas
├── cardlib.py          # Bibliothèque partagée (noms aléatoires, quotas, validation)
├── generate_cards.py   # cards_manifest.json -> cards_data.js
├── migrate_stics.py    # image-stics/ -> images/ + manifeste (migration de set)
├── image-stics/        # Dossier de staging temporaire (ignoré par git, supprimé après migration)
├── images/             # Illustrations, nommage NNN<Nom>.<ext> (ratio 630x880)
│   ├── 001Kraus.jpg
│   ├── 002Braus.jpg
│   └── 010Tays.jpg
└── README.md           # Documentation technique du projet

```

### Principe : aucune liste en dur

Ni les cartes, ni les raretés, ni les albums, ni les probabilités, ni la clé de
sauvegarde ne sont écrits dans `index.html`. Tout est lu depuis `cards_data.js`,
lui-même généré depuis `cards_manifest.json`. `index.html` contient des conteneurs
vids (`#album-categories-bar`, `#rarity-stats-list`) remplis au démarrage, et chaque
valeur a un repli si `cards_data.js` est absent ou ancien. Conséquence : ajouter une
carte, une rareté ou un album = éditer le manifeste, pas le HTML.

Clés de `cards_manifest.json` :

| Clé | Rôle |
| --- | --- |
| `cards[]` | `{id, name, rarity, emoji, image, source}` — la collection |
| `save_key` | clé de sauvegarde CloudStorage / localStorage |
| `rarities`, `rarity_labels`, `rarity_symbols`, `rarity_css` | libellés, symboles ◆, classes CSS |
| `rarity_weights` | quotas utilisés pour le tirage aléatoire des raretés |
| `draw_table` | seuils cumulés du tirage gacha (`standard` = slots 1‑2, `bonus` = carte 3) |
| `foil_rarities` | raretés qui recoivent l'effet holographique |
| `albums[]` | `{key, title, icon, sets:[{name, ids}]}` |

---

## ⚙️ Spécifications Techniques

### 1. Stockage & Persistance des Données

* **Clé de sauvegarde :** `tma_gacha_v2` (versionnée dans `cards_manifest.json`, clé `save_key`)
* **Mécanisme :**
1. Utilisation prioritaire de l'API cloud Telegram : `window.Telegram.WebApp.CloudStorage`.
2. Fallback automatique sur `window.localStorage` en cas d'exécution hors Telegram ou d'échec réseau.


* **Structure de l'objet d'état (`state`) :**
```json
{
  "packs": 6,
  "lastUpdate": 1711370000000,
  "inventory": {
    "001": 2,
    "149": 1
  },
  "stats": {
    "packsOpened": 14,
    "cardsDrawn": 42,
    "firstOpenedAt": 1711369000000
  }
}

```



> ⚠️ **Alerte Développeur (Plafond 4 Ko) :**
> Telegram impose une limite stricte de **4 096 octets** par clé dans `CloudStorage`.
> L'inventaire actuel consomme environ 1,8 Ko pour 222 cartes. Si le jeu dépasse les **400 à 450 cartes uniques**, il faudra compacter le stockage (ex: tableau d'identifiants ou bitfield) ou segmenter les clés (`tma_gacha_v2_set1`, `tma_gacha_v2_set2`).
>
> La clé est versionnée dans `cards_manifest.json` (`save_key`). `migrate_stics.py` la bump automatiquement quand la collection change : les ids `001…` étant réutilisés, un ancien inventariat désignerait les mauvaises cartes.

---

### 2. Économie & Système d'Énergie

* **Boosters max en réserve :** 6 boosters.
* **Taux de régénération :** 1 booster toutes les 10 minutes (`10 * 60 * 1000` ms).
* **Composition d'un pack :** 3 cartes tirées séquentiellement.

---

### 3. Moteur de Tirage & Probabilités

Le tirage implémente une logique par emplacement (**Slot-based RNG**) pour garantir un équilibre entre progression fluide et préservation de la rareté des cartes fortes :

| Emplacement dans le booster | Commune (◆) | Rare (◆◆) | Épique (◆◆★) | Légendaire (◆◆★★) |
| --- | --- | --- | --- | --- |
| **Cartes 1 & 2** (Slots 0 & 1) | **82.0 %** | **16.9 %** | **1.0 %** | **0.1 %** |
| **Carte 3** (Slot 2 — "Carte Rare") | **60.0 %** | **28.0 %** | **11.0 %** | **1.0 %** |

Ces seuils sont **des données, pas du code** : ils sont lus dans
`CARDS_META.drawTable` (source : `draw_table` du manifeste). Modifier une probabilité
= éditer le manifeste puis `python generate_cards.py`. `rollRarity()` retombe sur les
seuils historiques si le manifeste n'en fournit pas.

> ⚠️ Les pourcentages sont indépendants du nombre de cartes : avec un pool de 1 seule
> carte légendaire, la chance réelle d'en tirer une est bien plus élevée que le
> pourcentage affiché. À re-rétuner si la collection reste sous ~100 cartes.

---

### 4. Rendu Visuel & Effets Graphiques

* **Format des cartes :** Ratio officiel TCG $630 \times 880$ (`aspect-ratio: 630 / 880`).
* **Intégrité graphique :** Aucun rognage CSS (`border-radius: 0` sur l'image) afin de préserver les bordures noires, numéros et symboles de rareté d'origine. Une image qui n'est pas au ratio 630x880 est donc affichée **étirée**, pas rognée : `migrate_stics.py --dry-run` signale les ratios inattendus avant migration.
* **Performance :** Attribut `loading="lazy"` actif sur les images de la grille pour minimiser l'empreinte mémoire initiale.
* **Effet Foil / Holographique interactif :**
* Appliqué exclusivement sur les cartes **Épiques** et **Légendaires**.
* Coordonnées dynamiques via CSS Variables (`--foil-x`, `--foil-y`).
* Piloté en temps réel par :
* Les événements tactiles (`pointermove`).
* L'API Gyroscope mobile (`DeviceOrientationEvent` sur `gamma` et `beta`).





---

## 🛠️ Outils Développeur & Commandes URL (Cheats)

Des commandes administratives permettent de tester l'application sans console, via le paramètre Telegram `startapp` ou les paramètres URL classiques :

| Commande | URL Telegram (TMA) | URL Navigateur standard | Action |
| --- | --- | --- | --- |
| **Recharger l'énergie** | `t.me/BOT/app?startapp=boosters` | `https://site.io/?startapp=boosters` | Remet les boosters à 6/6 |
| **Donner une carte** | `t.me/BOT/app?startapp=give_001` | `https://site.io/?startapp=give_001` | Attribue 1 exemplaire de la carte (format 3 chiffres) |
| **Reset complet** | `t.me/BOT/app?startapp=reset` | `https://site.io/?startapp=reset` | Purge intégrale de la sauvegarde (inventaire + stats) |

---

## 📖 Guide de Contribution pour le Prochain Développeur

### Remplacer tout le jeu de cartes

```bash
# 1. Déposer les nouvelles illustrations dans image-stics/
# 2. Vérifier ce qui va se passer (noms et raretés tirés au sort, rien n'est écrit)
python migrate_stics.py --dry-run

# 3. Migrer : copie vers images/, retire les anciennes images, régénère le manifeste
#    et cards_data.js, bump la clé de sauvegarde, supprime image-stics/
python migrate_stics.py
```

Options utiles : `--seed N` (autre tirage de noms/raretés), `--set-size N` (taille des
albums), `--keep-staging` (conserve `image-stics/`), `--keep-save-key` (ne purge pas
l'inventaire des joueurs).

Les noms et les raretés sont générés par `cardlib.py` à partir d'une **graine fixe** :
relancer la migration sur le même contenu avec la même graine donne le même résultat.
Les vraies métadonnées STICS remplaceront ces valeurs dans `cards_manifest.json`.

### Ajouter ou modifier des cartes à la main

1. Éditer `cards_manifest.json` (jamais `cards_data.js`, jamais `index.html`).
2. Ajouter l'illustration dans `images/` en respectant la nomenclature `IDNom.<ext>`
   (ex : `011Saxophone.png`), ou laisser une entrée avec une image existante.
3. Régénérer et valider :

```bash
python generate_cards.py --check   # valide ids, noms, raretés, albums, images
python generate_cards.py           # écrit cards_data.js
```

`generate_cards.py` refuse d'écrire si une carte n'a pas d'image sur le disque, si un id
ou un nom est dupliqué, si un pool de rareté est vide, ou si un album référence un id
inexistant. L'application recalcule ensuite automatiquement le total des cartes et les
barres de progression.

### Modifier les probabilités de tirage

Éditer `draw_table` dans `cards_manifest.json` puis `python generate_cards.py` :

```json
"draw_table": {
    "standard": { "common": 82.0, "rare": 98.9, "epic": 99.9, "legendary": 100.0 },
    "bonus":    { "common": 60.0, "rare": 88.0, "epic": 99.0, "legendary": 100.0 }
}
```

Ce sont des seuils cumulés : une carte est `rare` si le roll est >= `common` et <
`rare`. La dernière valeur doit valoir 100.

### Retirer le code en dur restant

`index.html` ne contient plus aucune liste de cartes, de raretés ni d'albums. Si tu
ajoutes une rareté (ex. `mythic`), il faut : l'ajouter dans `rarities` **et** dans
`rarity_labels` / `rarity_symbols` / `rarity_css` du manifeste, ajouter les variables
CSS `--color-<cle>` et `--halo-<cle>`, puis `python generate_cards.py`.

### Déploiement et liaison Telegram

1. Commiter et pousser les modifications sur la branche principale (`main`).
2. Vérifier que GitHub Pages est actif dans **Settings > Pages** (Source : `Deploy from a branch` -> `/root`).
3. Dans Telegram, ouvrir **[@BotFather](https://t.me/BotFather?utm_source=gemini)** :
* `/myapps` > Sélectionner l'application.
* `Edit App` > `Edit URL` > Renseigner l'adresse HTTPS fournie par GitHub Pages.



```

```
