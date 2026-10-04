# Plan d'exécution locale de l'application (TCG STICS)

Ce plan explique comment lancer l'application statique localement sans déploiement sur GitHub Pages. L'application est entièrement frontale (HTML + JS + images + données générées), sans backend.

## 1. Connaître l'état du projet

Vérifier les fichiers essentiels :

- `index.html` : application complète (inclut Telegram WebApp SDK)
- `cards_data.js` : données des cartes générées depuis `cards_manifest.json`
- `cards_manifest.json` : source de vérité (cartes, raretés, albums, probabilités, `save_key`)
- `images/` : illustrations au format 630×880
- `generate_cards.py`, `cardlib.py` : outils de génération/migration
- `migrate_stics.py` : migration depuis `image-stics/` vers `images/`

Pas d'installation de dépendances Node/npm obligatoire pour exécuter l'app (seulement pour servir statiquement). Python est suffisant.

## 2. Prérequis

- Python 3.x installé (disponible dans `.venv/bin/python3` dans ce repo)
- Navigateur moderne (Chrome/Firefox/Edge/Safari)
- Connexion internet non requise une fois les fichiers locaux présents (sauf Telegram WebApp SDK qui est chargé depuis `https://telegram.org/js/telegram-web-app.js` — fonctionnel hors ligne uniquement si mis en cache, mais mieux de rester en ligne pour TMA complet ; pour un test basique, SDK se charge sans bloquer le reste)

Remarques :

- L'app utilise `localStorage` en fallback si Telegram WebApp n'est pas disponible (exécution dans navigateur classique). C'est parfait pour un test local.
- Clé de sauvegarde : `tma_gacha_v2` (définie dans `cards_data.js` via `META.saveKey`/manifest). Les données locales sont stockées sous cette clé dans `localStorage`.

## 3. Lancer un serveur HTTP statique

L'application charge des fichiers locaux (JS, images). Il **faut** servir via HTTP (et non ouvrir `index.html` directement en `file://`) pour éviter certains problèmes de chargement selon les navigateurs. Trois options simples :

### Option A : Python (recommandée, disponible dans le repo)

Dans `/home/seb/STICS_TCG` :

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

Ou avec l'environnement virtuel :

```bash
.venv/bin/python -m http.server 8080 --bind 127.0.0.1
```

Le serveur démarre. Laisser le terminal ouvert.

### Option B : Node.js (si disponible)

```bash
npx http-server -p 8080 -a 127.0.0.1
```

### Option C : Python HTTP + accès réseau local (si besoin de tester sur mobile)

```bash
python3 -m http.server 8080 --bind 0.0.0.0
```

Puis accéder via `http://<IP_locale>:8080/` sur le même réseau.

## 4. Ouvrir l'application dans le navigateur

Aller sur [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

Comportement attendu :

- Page se charge (fond Telegram, UI responsive)
- Telegram WebApp SDK tente de s'initialiser (peut rester silencieux hors Telegram)
- Données chargées depuis `cards_data.js` (total cartes visible dynamiquement)
- Sauvegarde : tentera CloudStorage Telegram en priorité, sinon `localStorage`. Hors Telegram, `localStorage` est utilisé.

## 5. Tester rapidement le fonctionnement

L'application expose des commandes URL (cheats/admin) sans console :

| Action | URL (navigateur) | Effet |
| --- | --- | --- |
| Recharger l'énergie | `http://127.0.0.1:8080/?startapp=boosters` | Remet les boosters à 6/6 |
| Donner une carte | `http://127.0.0.1:8080/?startapp=give_001` | Donne 1 exemplaire de la carte N°001 |
| Reset complet | `http://127.0.0.1:8080/?startapp=reset` | Purge inventaire + stats (retour état initial) |

Astuce : ces paramètres fonctionnent aussi via `start_param` dans Telegram Mini App (`t.me/BOT/app?startapp=...`).

## 6. Vérifications rapides (optionnel mais utile)

- Vérifier que les images s'affichent : `http://127.0.0.1:8080/images/001Kraus.jpg` doit retourner HTTP 200
- Vérifier les données : `http://127.0.0.1:8080/cards_data.js` doit être servi (type `application/javascript` ou `text/javascript`)
- Ouvrir DevTools > Console : pas d'erreurs critiques (Telegram SDK peut émettre warnings hors contexte TMA, c'est normal)
- Ouvrir DevTools > Application > Local Storage : clé `tma_gacha_v2` (ou valeur depuis `cards_manifest.json`) apparaît après interaction (ou après reset/give)

## 7. Arrêter le serveur

Dans le terminal où tourne le serveur : `Ctrl+C`.

## 8. Notes importantes

- **Format d'images** : 630×880. Aucun rognage CSS (préserve bordures). Images hors ratio s'étirent (et `migrate_stics.py --dry-run` signale les écarts).
- **Limite CloudStorage** : 4 Ko max par clé dans Telegram. À ~400-450 cartes uniques, prévoir compactage (id array/bitfield) ou segmentation de clé. Voir README §1 pour détails.
- **Synchronisation temps** : l'app fait un `HEAD` sur l'URL courante pour estimer offset serveur/cliente (anti-triche léger). En local, ça fonctionne (retourne Date du serveur HTTP local).
- **Foil/gyroscope** : effet holographique sur Épiques/Légendaires (pointermove + DeviceOrientationEvent sur mobile). Fonctionne en browser standard (pointermove).
- **Manifest-driven** : `index.html` lit tout depuis `cards_data.js` (généré depuis `cards_manifest.json`). Ne pas modifier les listes en dur dans HTML quand le manifest existe.

## 9. Dépannage

| Problème | Cause probable | Solution |
| --- | --- | --- |
| Images ne s'affichent pas (404) | Ouvert en `file://` au lieu de HTTP | Utiliser un serveur HTTP statique (étape 3) |
| JS non chargé / erreurs CORS | Serveur mal configuré | Utiliser `127.0.0.1` (pas `0.0.0.0` dans certains cas) et laisser les chemins relatifs |
| Données absentes | `cards_data.js` manquant/corrompu | Régénérer : `python3 generate_cards.py` (valider d'abord avec `--check`) |
| Sauvegarde ne persiste pas entre onglets | Contexte incognito | Tester dans fenêtre normale |
| Compteurs semblent faux au chargement (flash) | HTML contient valeurs par défaut (normal) | Elles sont écrasées au runtime par JS — comportement attendu |

## 10. Ressources utiles

- README complet : `/home/seb/STICS_TCG/README.md`
- Données actuelles : `cards_manifest.json`, `cards_data.js`
- Génération : `python3 generate_cards.py --help`, `python3 migrate_stics.py --help`
- Graph du codebase : `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md` (peut aider pour comprendre flux load/save)
