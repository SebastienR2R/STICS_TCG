# Plan — Remplacer les 222 cartes actuelles par les cartes de `image-stics/`

> **Statut : EXÉCUTÉ le 2026-10-04** (branche `feat/stics-cards`, tag de rollback
> `backup-cards-222`). 10 photos déposées dans `image-stics/` → 10 cartes, 222 retirées,
> `image-stics/` supprimé. Voir « Journal d'exécution » en §8 pour l'écart avec le plan.
>
> **Écart majeur :** le plan prévoyait de recopier des listes en dur (`ALBUMS_DB` régénéré
> une fois, compteurs de stats recopiés dans le HTML, seuils de tirage dans le JS). À la
> demande, tout est passé en **configuration pilotée par les données** : une source de
> vérité unique (`cards_manifest.json`) génère `cards_data.js`, et `index.html` ne
> contient plus aucune carte, rareté, album, probabilité ni clé de sauvegarde en dur.

Date de rédaction : 2026-10-04 · Repo : `/home/seb/STICS_TCG`

---

## 1. Objectif

Le dossier `image-stics/` est un **dossier temporaire** dans lequel les nouvelles
illustrations seront déposées. Une fois la migration faite, le dossier doit être
**supprimé** : son contenu vit alors dans `images/`, seul dossier lu par l'app.

Le but : que `index.html` + `cards_data.js` servent les nouvelles cartes, avec des
**noms aléatoires** et des **raretés aléatoires** attribués automatiquement (le temps
qu'on n'a pas encore les vraies métadonnées STICS).

**Hors périmètre de ce plan** : le renommage des illustrations elles-mêmes (numéro / nom
imprimés sur l'image). Si les images fournies portent déjà un numéro visible, il y aura
désynchronisation entre l'image et `id` — voir §9.

---

## 2. État actuel (vérifié)

| Élément | Fait observé | Référence |
| --- | --- | --- |
| Cartes | 222 illustrations `NNN<Nom>.png` (630x880) | `images/` |
| Données | `const CARDS_DB = { common, rare, epic, legendary }`, 149/50/20/3 | `cards_data.js:1` |
| Génération | `generate_cards.py` scanne `images/` et **déduit la rareté des plages d'id** (1‑148 & 222 → common, 149‑198 → rare, 199‑218 → epic, 219‑221 → legendary) | `generate_cards.py:33-41` |
| Chargement | `<script src="cards_data.js">` avant le code applicatif | `index.html:8` |
| Totaux | `TOTAL_CARDS` calculé dynamiquement sur `CARDS_DB` | `index.html:968-970` |
| Tirage | `drawCardBySlot()` : pools par rareté, seuils 82/98.9/99.9 % (slots 0‑1) et 60/88/99 % (slot 2) | `index.html:1206-1225` |
| **Albums** | `ALBUMS_DB` **code en dur** : 3 catégories (`fanfares`, `promos`, `instruments`) et ~30 sets qui listent **explicitement les ids** de l'ancienne collection | `index.html:982-1026` |
| Catégories albums | 3 boutons **hardcodés dans le HTML** (`selectAlbumCategory('fanfares'\|'promos'\|'instruments')`) | `index.html:792-794` |
| Defaults albums | `currentAlbumCat='fanfares'`, `currentAlbumSet='SZ'` | `index.html:1030-1031` |
| Totaux statiques | « 0 sur 222 cartes collectées », `0 / 149`, `0 / 50`, `0 / 20`, `0 / 3` (écrits en dur, écrasés par le JS au runtime → flash de contenu faux) | `index.html:826,864,872,880,888` |
| Sauvegarde | clé unique `tma_gacha_v1` (CloudStorage Telegram + fallback localStorage) | `index.html:1052,1054,1074,1076,1079` |
| Debug | `?startapp=give_<num>` → `padStart(3,'0')` + `getCardById` | `index.html:1188-1203` |
| Tri / continuité | Aucun `.sort()`, ids non-contigus tolérés, pas d'hypothèse `1..N` → **les ids peuvent être renumérotés librement** | `index.html` (recherche `sort` vide) |
| Rendu | `<img src="${card.image}">` uniquement ; **fallback emoji si `image` est vide** | `index.html:1351-1369` |
| Git | `images/` et `cards_data.js` sont **trackés** (donc récupérables). `.venv` sans PIL | `git status` |

### Conséquences directes

1. **`ALBUMS_DB` est le vrai point bloquant** : toutes les listes d'ids référencent les
   anciennes cartes. Sans mise à jour, la vue Albums affiche des silhouettes
   `#001…#222` pour des cartes qui n'existent plus.
2. **La rareté ne peut pas rester dérivée des ids** : `generate_cards.py:33-41`
   l'écraserait à chaque régénération. Il faut une source de vérité persistante (§4).
3. **La clé de sauvegarde `tma_gacha_v1` doit être bumpée** : les ids `001…` sont
   réutilisés, un inventaire joueur existant attribuerait des cartes au mauvais moment.
4. Le nombre de cartes n'est **pas** coderdifié côté logique (dynamique), mais
   `/home/seb/STICS_TCG/index.html:826` et les 4 tags de rareté le sont dans le HTML.

---

## 3. État cible

```
├── image-stics/           ← SUPPRIMÉ en fin de plan
├── images/                ← uniquement les nouvelles cartes, NNN<NomAléatoire>.png
├── cards_data.js          ← régénéré depuis cards_manifest.json
├── cards_manifest.json    ← NOUVEAU : source de vérité (id, nom, rareté, fichier)
├── generate_cards.py      ← modifié : rareté lue dans le manifest
└── index.html             ← ALBUMS_DB + compteurs statiques + clé de sauvegarde
```

Contraintes d'acceptation :

- `TOTAL_CARDS == nombre de fichiers dans images/`.
- Chaque `card.image` pointe vers un fichier **existant**.
- Raretés : `common/rare/epic/legendary` toutes **non vides**.
- 0 référence résiduelle à un ancien nom de carte ou à un id hors `001..N`.
- `image-stics/` absent du dépôt.

---

## 4. Décisions de conception (valeurs par défaut, à ajuster si besoin)

### 4.1 Noms aléatoires — générateur déterministe

On ne veut pas de noms « tirés au sort » à chaque régénération (le fichier serait
différent à chaque run, donc non reviewable). Donc : **PRNG à graine fixe**.

- Seed par défaut : `STICS_SEED = 1337` (constante en tête de `generate_cards.py`).
- Construction : 2 ou 3 syllabes puisées dans des listes fermées, 1re lettre en
  majuscule, ASCII pur, sans espace ni accent (compatibilité nom de fichier + URL).
  - début : `Ba, Zo, Ki, Lu, Mi, Na, O, Pra, Sé→Se, Ta, Vo, Bra, Cri, Dra, Éli→Eli, Fa, Go, Hé→He, Ja, Kra, Mé→Me, No, Or, Py, Quo, Ré→Re, Sa, Tro, Va, Wa, Za`
  - milieu : `bel, cor, dar, flu, gon, gué→gue, la, mar, nel, pan, quen, rar, sel, tar, ur, val, wé→we, xar, yé→ye, zel`
  - fin : `an, ar, el, ic, in, io, is, ol, on, os, un, us, ix, ys`
- Unicité garantie (set + suffixe numérique si collision) et **longueur ≤ 14 caractères**
  pour rester lisible en vignette.
- Le nom est écrit dans le manifest : il devient du texte **définitif** jusqu'à ce
  qu'on le remplace par les vrais noms STICS.

### 4.2 Raretés aléatoires — quotas puis mélange à graine

On ne veut pas non plus une rareté « purement aléatoire » qui produirait 0 légendaire
ou 90 % de communes (le tirage `drawCardBySlot` présuppose des pools équilibrés).

- Quotas sur N cartes, proportions alignées sur l'existant (149/50/20/3 ≈ 67/22,5/9/1,5 %) :
  - `legendary = max(1, round(N * 0.015))`
  - `epic      = max(1, round(N * 0.09))`
  - `rare      = max(1, round(N * 0.225))`
  - `common    = N - legendary - epic - rare`
  - Si N est petit (ex. 30 cartes) → 19 common / 7 rare / 3 epic / 1 legendary.
- Attribution : `random.Random(SEED + 1).shuffle(ids)` puis distribution par quotas.
  → **équitable et déterministe**, aucune carte n'est favorisée par son id.
- Point d'attention : si N devient petit, les seuils de `drawCardBySlot`
  (`index.html:1208-1220`) suréprésentent les légendaires (1/222 = 0,45 % mais
  pool de 3 → ~15 % du slot 3). **À re-rétuner si N < 100** (hors périmètre par défaut).

### 4.3 `cards_manifest.json` — la source de vérité

```json
{
  "seed": 1337,
  "cards": [
    { "id": "001", "name": "Zolvan", "rarity": "common",   "emoji": "🎺", "source": "IMG_4821.jpg", "image": "images/001Zolvan.png" },
    { "id": "002", "name": "Kirmar", "rarity": "legendary","emoji": "🎺", "source": "IMG_4822.jpg", "image": "images/002Kirmar.png" }
  ]
}
```

Règles :

- **Idempotence** : si le manifest existe, il est réutilisé tel quel (seules les
  nouvelles images non mappées sont ajoutées). Relancer le script ne bouge rien.
- `id` = position dans le tri alphabétique des **noms de fichiers sources** → migration
  déterministe et vérifiable.
- `emoji` : `🎺` par défaut (comme aujourd'hui), modifiable plus tard par carte.
- Le manifest est **versionné dans git** (c'est de la donnée, pas un artefact).

### 4.4 `generate_cards.py` — modifications

1. Supprimer la règle de rareté par plages d'id (`generate_cards.py:33-41`).
2. Nouveau comportement : lire `cards_manifest.json` s'il existe ; sinon le créer
   (noms + raretés aléatoires à graine) puis l'écrire.
3. Warnings au lieu du silence actuel pour les fichiers non conformes au motif
   `^(\d{3})(.+)\.(png|webp|jpg)$` (`generate_cards.py:6`) : aujourd'hui un fichier
   mal nommé est **ignoré silencieusement** et la carte disparaît du jeu.
4. Auto-vérification avant écriture (`sys.exit(1)` si échec) :
   - tous les `image` existent sur disque ;
   - ids uniques, noms uniques, pools de rareté non vides ;
   - `somme des quotas == N`.
5. Le reste du script (structure JSON, `indent=4`, `ensure_ascii=False`) est **conservé**
   tel quel : pas de changement de format de `cards_data.js`.

### 4.5 `ALBUMS_DB` — placeholder généré

Deux options, **recommandation : A** (aucune modification du HTML de navigation).

- **A. Conserver les 3 catégories existantes** (`fanfares`, `promos`, `instruments`)
  pour ne pas toucher `index.html:792-794` ni `1030-1031`, mais regénérer leurs sets
  par **tranches d'ids contiguës** de 12 cartes : `"STICS 1"`, `"STICS 2"`, …
  réparties sur les 3 catégories.-sets vides tolérés (le code gère `total = 0`,
  `index.html:1512`) mais on évite.
- **B. Repenser les albums** (catégories STICS réelles). Plus propre à terme mais
  implique de modifier le HTML de navigation + les libellés.

Les noms/id des sets seront de toute façon remplacés quand les vraies infos STICS
arriveront : c'est un squelette jetable, à garder lisible et facile à réécrire.

### 4.6 Clé de sauvegarde

Bumper `tma_gacha_v1` → **`tma_gacha_v2`** (5 occurrences : `index.html:1052,1054,1074,1076,1079`).
Raison : les ids `001…` étant réutilisés pour des cartes différentes, l'ancien
inventaire designerait les mauvaises cartes. L'ancienne clé est simplement ignorée
(les joueurs repartent à 0 collection). Si l'on préfère garder les joueurs, il faut
une table de correspondance `ancien id → nouveau id` — **hors périmètre**.

### 4.7 Nettoyage du dossier temporaire

`image-stics/` est vidé **en dernier**, après validation complète (§6), puis
`rm -rf image-stics/`. Ne rien supprimer avant que `cards_data.js` soit régénéré et
vérifié : c'est la seule source des images.

---

## 5. Étapes d'exécution

### Étape 0 — Sécurité

```bash
cd /home/seb/STICS_TCG
git status                      # .opencode/, AGENTS.md, graphify-out/ non trackés : OK
git checkout -b feat/stics-cards
git tag backup-cards-222        # point de rollback
```

### Étape 1 — Inventaire des images sources

- Lister `image-stics/` : nombre de fichiers, extensions réelles (`.jpg` ? `.webp` ?),
  fichiers parasites (`__MACOSX`, `.DS_Store`, doublons).
- Vérifier les dimensions **sans dépendance externe** (pas de PIL dans `.venv`) :
  lecture de l'en-tête PNG via `struct`, ou `file image.png`.
  Attendu **630x880** (ratio `aspect-ratio: 630/880` utilisé par le CSS).
  Les images hors ratio ne sont pas rognées par l'app (`border-radius: 0`) → elles
  seront simplement affichées déformées. Signaler, ne pas corriger d'office.
- **Si le dossier est vide** : c'est explicitement accepté (`image-stics/` est vide à
  la rédaction). Le script doit alors **échouer proprement** avec un message clair,
  et le plan s'arrête là.

### Étape 2 — Import + nommage (nouveau script `migrate_stics.py`)

Un script one-shot à la racine (cohérent avec `generate_cards.py`) :

1. Lister `image-stics/`, trier par nom de fichier.
2. Vérifier l'unicité des noms de fichiers sources ; warned sur les collisions.
3. Attribuer `id` = `f"{i+1:03d}"` et copier vers `images/{id}{NameAleatoire}{ext}`
   (copie, **pas** déplacement : `image-stics/` reste intact jusqu'à l'étape 5).
4. Écrire `cards_manifest.json`.
5. Afficher un récapitulatif (N cartes, répartition des raretés, 5 exemples).

### Étape 3 — Régénérer `cards_data.js`

```bash
python generate_cards.py
```

### Étape 4 — Supprimer les 222 anciennes images

- Lister les fichiers **trackés** dans `images/` qui ne sont pas dans le manifest, puis
  `git rm` uniquement ceux-là (ne pas faire `images/*.png` en aveugle : ça supprimerait
  les nouvelles).
- Conserver `images/.gitkeep`.

### Étape 5 — Mettre à jour `index.html`

| Ligne | Action |
| --- | --- |
| `982-1026` | Remplacer `ALBUMS_DB` par la structure générée (§4.5) |
| `1030-1031` | `currentAlbumCat` / `currentAlbumSet` → première catégorie / premier set générés |
| `826` | `0 sur 222 cartes` → `0 sur N cartes` |
| `864,872,880,888` | `0 / 149`, `0 / 50`, `0 / 20`, `0 / 3` → nouveaux quotas |
| `1052,1054,1074,1076,1079` | `tma_gacha_v1` → `tma_gacha_v2` |

### Étape 6 — Vérification

```bash
# 1. Cohérence données <-> disque
python generate_cards.py                 # doit ré-afficher les mêmes quotas (idempotence)

# 2. Aucune référence à une ancienne carte dans le HTML
grep -nE '"(0[0-9][0-9]|1[0-9][0-9]|2[0-2][0-9])"' index.html | grep -v ALBUMS  # à relire
grep -rn "tma_gacha_v1" index.html        # doit être vide

# 3. Comptages
ls images/*.png | wc -l                 # == nombre de cartes
git diff --stat
```

Checklist manuelle (serveur local, `python -m http.server`) :

- [ ] Onglet **Shop** : ouverture de booster, les 3 cartes s'affichent avec images
      (aucune image cassée), badge ✨ « Nouvelle » correct.
- [ ] Onglet **Collection** → vue globale : N cartes, ratios de complétion OK.
- [ ] Onglet **Collection** → **Albums** : les 3 catégories fonctionnent, un set
      s'affiche avec ses silhouettes `#id` et les noms (pas d'« Inconnue »).
- [ ] Onglet **Stats** : compteurs par rareté = quotas, pourcentage global cohérent.
- [ ] `?startapp=give_001` → notifie « 001 — <nom> ».
- [ ] `?startapp=reset` → inventaire purgé.
- [ ] Zoom / modale sur une carte **( foil sur épique/légendaire**.
- [ ] Rechargement de page : l'inventaire persiste.
- [ ] `image-stics/` **supprimé**, `git status` propre.

### Étape 7 — Suppression du dossier temporaire (dernière action)

```bash
rm -rf image-stics/
```

### Étape 8 — Documentation

- `README.md` : section « Ajouter de nouvelles cartes » (`README.md:119-134`) à mettre à
  jour — le texte doit devenir « éditer le manifest », plus « scanner `images/` +
  plages d'id ». Corriger aussi le nombre de cartes et la note plafond 4 Ko
  (`README.md:62-64`).

### Étape 9 — Commit

```bash
git add -A
git commit -m "Remplacement des cartes par le set STICS (noms et raretés aléatoires, manifest)"
```

(tag `backup-cards-222` = rollback ; ne pas merger avant validation.)

---

## 6. Points ouverts (valeurs par défaut proposées)

| # | Question | Défaut proposé |
| --- | --- | --- |
| 1 | Combien de cartes dans `image-stics/` ? | inconnu à la rédaction — quota de rareté calculé sur N automatiquement |
| 2 | Format / ratio des images ? | 630x880 attendu ; sinon signaler |
| 3 | Noms : stics génériques ou noms de fanfare plausibles ? | syllabes aléatoires déterministes |
| 4 | Albums : placeholder ou vraie structure STICS ? | placeholder 3 catégories (A) |
| 5 | Repartir de zéro côté joueurs ? | oui, bump `tma_gacha_v2` |
| 6 | Rééquilibrer `drawCardBySlot` si N < 100 ? | non (hors périmètre) |
| 7 | Numéro imprimé sur l'image vs `id` ? | désynchronisation assumée pour l'instant |

---

## 7. Rollback

```bash
git checkout main
git branch -D feat/stics-cards        # backup-cards-222 conserve l'état 222
```

`images/` et `cards_data.js` étant trackés, `git reset --hard backup-cards-222`
restaure l'intégralité de l'ancienne collection. Le seul élément non récupérable
par git serait `image-stics/` s'il était supprimé **avant** commit → ne jamais
supprimer avant l'étape 7.
---

## 8. Journal d'exécution (2026-10-04)

### Ce qui a été fait

| Étape | Résultat |
| --- | --- |
| Tag `backup-cards-222` | point de rollback sur l'ancienne collection |
| `cardlib.py` (nouveau) | source de vérité partagée : manifest, noms aléatoires à graine, quotas de rareté, albums, validation |
| `generate_cards.py` (réécrit) | piloté par le manifeste ; `--init` (bootstrap), `--check`, `--reseed`, `--migrate-names` |
| `migrate_stics.py` (nouveau) | `--dry-run`, `--seed`, `--set-size`, `--keep-staging`, `--keep-save-key` |
| Bootstrap | manifeste créé depuis les 222 cartes existantes, 25 albums récupérés depuis `index.html`@HEAD ; `CARDS_DB` régénéré **byte-identique** à l'ancien (refactor sans perte) |
| Migration | 10 photos `.jpg` → `images/001Kraus.jpg` … `010Tays.jpg` ; 222 anciennes images retirées ; `image-stics/` supprimé |
| Raretés tirées | 6 communes, 2 rares, 1 épique, 1 légendaire (quotas 67/22,5/9/1,5 %, seed 1337) |
| Clé de sauvegarde | `tma_gacha_v1` → `tma_gacha_v2` (ids `001…` réutilisés) |
| `index.html` | plus aucun code en dur : albums, lignes de stats, pools de tirage, foil, clé de sauvegarde, compteurs totaux |
| Vérification | chargement sans erreur, distribution du tirage conforme au tableau du README (82,0/16,8/1,0/0,1 et 60,0/27,9/10,9/1,0), `?startapp=give_001` fonctionnel, proportions de stats correctes |

### Points de vigilance

- **Ratio des images** : les 10 photos font 1280x960, 960x1280, 720x1280… et non
  630x880. L'app ne rogne pas (`border-radius: 0`, `aspect-ratio` fixe) : elles sont
  affichées **étirées**. Signalé par `migrate_stics.py`, non corrigé d'office (le
  README documente ce comportement).
- **Extension** : les images restent en `.jpg` (le générateur accepte png/webp/jpg).
- **Collection réduite à 10 cartes** : les seuils de tirage sont des pourcentages, pas
  des proportions de pool. Avec 1 seule légendaire, la chance réelle d'en obtenir une
  est nettement supérieure à 0,1 %. À re-rétuner quand le vrai jeu arrive.
- **Albums squelettiques** : `chunk_albums` découpe les ids en sets de 12 répartis
  round-robin sur les catégories. L'attribution d'un set ne dépend que de son index :
  ajouter des cartes ne reshuffle pas les sets existants.
