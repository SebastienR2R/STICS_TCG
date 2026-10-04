"""Boîte à outils de la collection de cartes.

Source de vérité unique : `cards_manifest.json`. Tout le reste
(`cards_data.js`, albums, probabilités, clé de sauvegarde) en découle,
ce qui évite d'écrire des listes de cartes en dur dans le code.

CLI :
    python generate_cards.py            # manifest -> cards_data.js
    python generate_cards.py --init     # crée le manifest depuis images/ (bootstrap)
    python generate_cards.py --check    # valide sans rien écrire
    python migrate_stics.py             # image-stics/ -> images/ + manifest
"""

from __future__ import annotations

import json
import os
import random
import re
import struct
from typing import Any

IMAGE_DIR = "images"
STAGING_DIR = "image-stics"
MANIFEST_PATH = "cards_manifest.json"
DATA_PATH = "cards_data.js"
INDEX_PATH = "index.html"

IMAGE_EXTS = (".png", ".webp", ".jpg", ".jpeg")
FILENAME_RE = re.compile(r"^(\d{3})(.+)$")

RARITIES = ["common", "rare", "epic", "legendary"]

DEFAULT_RARITY_LABELS = {
    "common": "Commune",
    "rare": "Rare",
    "epic": "Épique",
    "legendary": "Légendaire",
}

DEFAULT_RARITY_SYMBOLS = {
    "common": "◆",
    "rare": "◆◆",
    "epic": "◆◆★",
    "legendary": "◆◆★★",
}

DEFAULT_RARITY_CSS = {
    "common": "c",
    "rare": "r",
    "epic": "e",
    "legendary": "l",
}

# Proportions cible, alignées sur la collection historique (149/50/20/3).
DEFAULT_RARITY_WEIGHTS = {
    "common": 0.670,
    "rare": 0.225,
    "epic": 0.090,
    "legendary": 0.015,
}

# Tables de tirage (seuils cumulés en %) : slots 0-1 puis slot 2 (carte rare).
DEFAULT_DRAW_TABLE = {
    "standard": {"common": 82.0, "rare": 98.9, "epic": 99.9, "legendary": 100.0},
    "bonus": {"common": 60.0, "rare": 88.0, "epic": 99.0, "legendary": 100.0},
}

# Plages legacy, utilisées uniquement pour retrouver la rareté d'une collection
# existante lors d'un bootstrap (generate_cards.py --init).
LEGACY_RARITY_RANGES = [
    (1, 148, "common"),
    (149, 198, "rare"),
    (199, 218, "epic"),
    (219, 221, "legendary"),
    (222, 222, "common"),
]

NAME_HEADS = [
    "Ba", "Zo", "Ki", "Lu", "Mi", "Na", "O", "Pra", "Se", "Ta", "Vo", "Bra",
    "Cri", "Dra", "Eli", "Fa", "Go", "He", "Ja", "Kra", "Me", "No", "Or",
    "Py", "Quo", "Re", "Sa", "Tro", "Va", "Wa", "Za",
]
NAME_MIDS = [
    "bel", "cor", "dar", "flu", "gon", "gue", "la", "mar", "nel", "pan",
    "quen", "rar", "sel", "tar", "ur", "val", "we", "xar", "ye", "zel",
]
NAME_TAILS = ["an", "ar", "el", "ic", "in", "io", "is", "ol", "on", "os", "un", "us", "ix", "ys"]

ALBUM_SET_SIZE = 12
DEFAULT_ALBUM_CATEGORIES = [
    {"key": "stics_a", "title": "STICS", "icon": "\U0001f3ba"},
    {"key": "stics_b", "title": "STICS Promos", "icon": "\U0001f393"},
    {"key": "stics_c", "title": "STICS Archives", "icon": "\U0001f3b7"},
]


# --------------------------------------------------------------------------- #
# Manifeste
# --------------------------------------------------------------------------- #

def default_manifest() -> dict[str, Any]:
    return {
        "version": 1,
        "seed": 1337,
        "save_key": "tma_gacha_v1",
        "default_emoji": "\U0001f3ba",
        "rarities": list(RARITIES),
        "rarity_labels": dict(DEFAULT_RARITY_LABELS),
        "rarity_symbols": dict(DEFAULT_RARITY_SYMBOLS),
        "rarity_css": dict(DEFAULT_RARITY_CSS),
        "rarity_weights": dict(DEFAULT_RARITY_WEIGHTS),
        "draw_table": json.loads(json.dumps(DEFAULT_DRAW_TABLE)),
        "foil_rarities": ["epic", "legendary"],
        "albums": [],
        "cards": [],
    }


def load_manifest(path: str = MANIFEST_PATH) -> dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    base = default_manifest()
    base.update(manifest)
    return base


def save_manifest(manifest: dict[str, Any], path: str = MANIFEST_PATH) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


# --------------------------------------------------------------------------- #
# Images
# --------------------------------------------------------------------------- #

def is_image(name: str) -> bool:
    return name.lower().endswith(IMAGE_EXTS)


def list_images(directory: str) -> list[str]:
    if not os.path.isdir(directory):
        return []
    return sorted(f for f in os.listdir(directory) if is_image(f))


def png_size(path: str) -> tuple[int, int] | None:
    """Dimensions d'un PNG sans dépendance externe (PIL absent de l'env)."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(24)
        if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
            return None
        width, height = struct.unpack(">II", head[16:24])
        return int(width), int(height)
    except OSError:
        return None


def jpeg_size(path: str) -> tuple[int, int] | None:
    """Dimensions d'un JPEG sans dépendance externe."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    if data[:2] != b"\xff\xd8":
        return None

    index = 2
    while index < len(data) - 9:
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            index += 2
            continue
        length = struct.unpack(">H", data[index + 2:index + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack(">HH", data[index + 5:index + 9])
            return int(width), int(height)
        index += 2 + length
    return None


def image_size(path: str) -> tuple[int, int] | None:
    return png_size(path) or jpeg_size(path)


def report_sizes(directory: str) -> dict[str, list[str]]:
    """Regroupe les images par dimensions pour repérer les ratios inattendus."""
    buckets: dict[str, list[str]] = {}
    for name in list_images(directory):
        size = image_size(os.path.join(directory, name))
        buckets.setdefault(str(size) if size else "illisible", []).append(name)
    return buckets


# --------------------------------------------------------------------------- #
# Génération aléatoire déterministe
# --------------------------------------------------------------------------- #

def random_name(rng: random.Random) -> str:
    name = rng.choice(NAME_HEADS)
    if rng.random() < 0.55:
        name += rng.choice(NAME_MIDS)
    name += rng.choice(NAME_TAILS)
    return name[0].upper() + name[1:]


def unique_names(count: int, rng: random.Random) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    while len(names) < count:
        candidate = random_name(rng)
        base = candidate
        suffix = 2
        while candidate in seen:
            candidate = f"{base}{suffix}"
            suffix += 1
        seen.add(candidate)
        names.append(candidate)
    return names


def rarity_quotas(total: int, weights: dict[str, float]) -> dict[str, int]:
    """Répartit `total` cartes selon les poids, avec au moins 1 carte par rareté."""
    rarities = [r for r in RARITIES if r in weights]
    if total < len(rarities):
        return {r: 1 for r in rarities}

    quotas = {r: 0 for r in rarities}
    assigned = 0
    for rarity in rarities:
        count = max(1, round(total * weights[rarity]))
        quotas[rarity] = count
        assigned += count

    # Réajuste le surplus sur la rareté la plus pondérée (common en pratique).
    order = sorted(rarities, key=lambda r: weights[r], reverse=True)
    index = 0
    while assigned > total:
        for rarity in order:
            if quotas[rarity] > 1:
                quotas[rarity] -= 1
                assigned -= 1
                break
        else:
            break
        index += 1
        if index > len(rarities) * total:  # garde-fou
            break

    while assigned < total:
        quotas[order[0]] += 1
        assigned += 1

    return quotas


def assign_rarities(ids: list[str], weights: dict[str, float], seed: int) -> dict[str, str]:
    quotas = rarity_quotas(len(ids), weights)
    shuffled = list(ids)
    random.Random(seed).shuffle(shuffled)

    mapping: dict[str, str] = {}
    cursor = 0
    for rarity in RARITIES:
        for _ in range(quotas.get(rarity, 0)):
            mapping[shuffled[cursor]] = rarity
            cursor += 1
    return mapping


# --------------------------------------------------------------------------- #
# Albums
# --------------------------------------------------------------------------- #

def chunk_albums(cards: list[dict[str, Any]], categories: list[dict[str, str]],
                 set_size: int = ALBUM_SET_SIZE) -> list[dict[str, Any]]:
    """Découpe les ids en sets de `set_size` cartes, répartis sur les catégories."""
    ids = [c["id"] for c in cards]
    chunks = [ids[i:i + set_size] for i in range(0, len(ids), set_size)]

    albums: list[dict[str, Any]] = []
    for position, category in enumerate(categories):
        mine = [chunk for index, chunk in enumerate(chunks) if index % len(categories) == position]
        if not mine:
            continue
        title = category.get("title", category["key"])
        albums.append({
            "key": category["key"],
            "title": title,
            "icon": category.get("icon", "\U0001f3b7"),
            "sets": [
                {"name": f"{title} {index + 1}", "ids": chunk}
                for index, chunk in enumerate(mine)
            ],
        })
    return albums


def albums_to_js_object(albums: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        album["key"]: {
            "title": album.get("title", album["key"]),
            "icon": album.get("icon", "\U0001f3b7"),
            "sets": {s["name"]: s["ids"] for s in album.get("sets", [])},
        }
        for album in albums
    }


# --------------------------------------------------------------------------- #
# Import
# --------------------------------------------------------------------------- #

def collect_staging(staging_dir: str = STAGING_DIR) -> list[str]:
    if not os.path.isdir(staging_dir):
        return []
    ignored = {".ds_store", "thumbs.db", ".gitkeep"}
    return sorted(
        f for f in os.listdir(staging_dir)
        if is_image(f) and f.lower() not in ignored and not f.startswith(".")
    )


def build_cards_from_staging(sources: list[str], seed: int, weights: dict[str, float],
                             emoji: str, keep_source_extension: bool = True) -> list[dict[str, Any]]:
    names = unique_names(len(sources), random.Random(seed))
    ids = [f"{index + 1:03d}" for index in range(len(sources))]
    rarities = assign_rarities(ids, weights, seed + 1)

    cards = []
    for card_id, source, name in zip(ids, sources, names):
        extension = os.path.splitext(source)[1].lower() if keep_source_extension else ".png"
        cards.append({
            "id": card_id,
            "name": name,
            "rarity": rarities[card_id],
            "emoji": emoji,
            "image": f"{IMAGE_DIR}/{card_id}{name}{extension}",
            "source": source,
        })
    return cards


def legacy_rarity(card_id: str) -> str:
    number = int(card_id)
    for low, high, rarity in LEGACY_RARITY_RANGES:
        if low <= number <= high:
            return rarity
    return "common"


def build_cards_from_images(image_dir: str = IMAGE_DIR, emoji: str = "\U0001f3ba") -> tuple[list[dict[str, Any]], list[str]]:
    """Reconstruit des entrées de carte depuis les noms de fichiers existants."""
    cards: list[dict[str, Any]] = []
    skipped: list[str] = []
    for name in list_images(image_dir):
        match = FILENAME_RE.match(os.path.splitext(name)[0])
        if not match:
            skipped.append(name)
            continue
        card_id, card_name = match.group(1), match.group(2)
        cards.append({
            "id": card_id,
            "name": card_name,
            "rarity": legacy_rarity(card_id),
            "emoji": emoji,
            "image": f"{image_dir}/{name}",
            "source": name,
        })
    return cards, skipped


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #

def validate(manifest: dict[str, Any], image_dir: str = IMAGE_DIR, check_disk: bool = True) -> list[str]:
    errors: list[str] = []
    cards = manifest.get("cards", [])
    if not cards:
        return ["Le manifeste ne contient aucune carte."]

    rarities = manifest.get("rarities") or RARITIES
    ids: set[str] = set()
    names: set[str] = set()
    images: set[str] = set()

    for card in cards:
        for field in ("id", "name", "rarity", "image"):
            if not card.get(field):
                errors.append(f"Carte incomplète, champ '{field}' manquant : {card}")
        card_id = card.get("id", "?")
        if card_id in ids:
            errors.append(f"id dupliqué : {card_id}")
        ids.add(card_id)
        if card.get("name") in names:
            errors.append(f"nom dupliqué : {card.get('name')}")
        names.add(card.get("name"))
        if card.get("rarity") not in rarities:
            errors.append(f"rareté inconnue pour {card_id} : {card.get('rarity')}")
        image = card.get("image", "")
        if image in images:
            errors.append(f"image dupliquée : {image}")
        images.add(image)
        if check_disk and image and not os.path.isfile(image):
            errors.append(f"image manquante sur le disque : {image}")

    if rarities:
        for rarity in rarities:
            pool = [c for c in cards if c.get("rarity") == rarity]
            if not pool:
                errors.append(f"pool de rareté vide : {rarity}")

    for album in manifest.get("albums", []):
        for card_set in album.get("sets", []):
            unknown = [i for i in card_set.get("ids", []) if i not in ids]
            if unknown:
                errors.append(f"album '{album.get('key')}' / set '{card_set.get('name')}' : ids inconnus {unknown}")

    if check_disk:
        on_disk = set(list_images(image_dir))
        referenced = {os.path.basename(c.get("image", "")) for c in cards}
        for orphan in sorted(on_disk - referenced):
            errors.append(f"image orpheline dans {image_dir}/ (non référencée) : {orphan}")

    return errors


# --------------------------------------------------------------------------- #
# Génération de cards_data.js
# --------------------------------------------------------------------------- #

def build_cards_db(manifest: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    db: dict[str, list[dict[str, Any]]] = {r: [] for r in manifest.get("rarities", RARITIES)}
    for card in sorted(manifest["cards"], key=lambda c: c["id"]):
        entry = {
            "id": card["id"],
            "name": card["name"],
            "emoji": card.get("emoji", manifest.get("default_emoji", "\U0001f3ba")),
            "image": card["image"],
        }
        db.setdefault(card["rarity"], []).append(entry)
    return db


def build_cards_meta(manifest: dict[str, Any]) -> dict[str, Any]:
    rarities = manifest.get("rarities", RARITIES)
    labels = manifest.get("rarity_labels", DEFAULT_RARITY_LABELS)
    symbols = manifest.get("rarity_symbols", DEFAULT_RARITY_SYMBOLS)
    css = manifest.get("rarity_css", DEFAULT_RARITY_CSS)
    return {
        "version": manifest.get("version", 1),
        "saveKey": manifest.get("save_key", "tma_gacha_v1"),
        "rarities": rarities,
        "rarityLabels": {r: labels.get(r, r) for r in rarities},
        "raritySymbols": {r: symbols.get(r, "") for r in rarities},
        "rarityCss": {r: css.get(r, "") for r in rarities},
        "drawTable": manifest.get("draw_table", DEFAULT_DRAW_TABLE),
        "foilRarities": manifest.get("foil_rarities", ["epic", "legendary"]),
        "albums": albums_to_js_object(manifest.get("albums", [])),
    }


def render_cards_data(manifest: dict[str, Any]) -> str:
    db = build_cards_db(manifest)
    meta = build_cards_meta(manifest)
    return (
        "// Fichier genere par generate_cards.py - ne pas editer a la main.\n"
        "// Source de verite : " + MANIFEST_PATH + "\n"
        "const CARDS_DB = " + json.dumps(db, ensure_ascii=False, indent=4) + ";\n\n"
        "const CARDS_META = " + json.dumps(meta, ensure_ascii=False, indent=4) + ";\n"
    )


def write_cards_data(manifest: dict[str, Any], path: str = DATA_PATH) -> int:
    content = render_cards_data(manifest)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return sum(len(v) for v in build_cards_db(manifest).values())