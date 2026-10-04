"""Genere cards_data.js a partir de cards_manifest.json.

    python generate_cards.py            # manifest -> cards_data.js
    python generate_cards.py --init     # cree le manifeste depuis images/ (bootstrap)
    python generate_cards.py --check    # valide sans ecrire
    python generate_cards.py --reseed 42 # rejoue le tirage aleatoire des raretes

La repartition des raretes vient du manifeste (cles `rarity_weights`), plus aucune
plage d'ids codee en dur. `--init` est le seul endroit qui connait l'ancienne
convention (rarete deduite de l'id) : il sert a migrer une collection existante
sans rien changer.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys

import cardlib

LEGACY_ALBUMS_RE = re.compile(r"const\s+ALBUMS_DB\s*=\s*(\{.*?\});\s*\n", re.DOTALL)


def extract_legacy_albums(path: str = cardlib.INDEX_PATH) -> list[dict]:
    """Recupere l'ancien ALBUMS_DB code en dur dans index.html."""
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    match = LEGACY_ALBUMS_RE.search(html)
    if not match:
        return []
    # Les cles JavaScript non quotees sont converties en JSON valide.
    raw = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', match.group(1))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []

    albums = []
    for key, group in data.items():
        albums.append({
            "key": key,
            "title": group.get("title", key),
            "icon": group.get("icon", "\U0001f3b7"),
            "sets": [{"name": name, "ids": ids} for name, ids in group.get("sets", {}).items()],
        })
    return albums


def cmd_init(args: argparse.Namespace) -> int:
    if os.path.isfile(cardlib.MANIFEST_PATH) and not args.force:
        print(f"{cardlib.MANIFEST_PATH} existe deja (utilise --force pour l'ecraser).")
        return 0

    cards, skipped = cardlib.build_cards_from_images()
    if not cards:
        print(f"Aucune image trouvee dans {cardlib.IMAGE_DIR}/.")
        return 1
    if skipped:
        print(f"Attention : {len(skipped)} fichier(s) ignores (nom sans id) : {skipped[:5]}")

    manifest = cardlib.default_manifest()
    manifest["cards"] = cards
    manifest["albums"] = extract_legacy_albums(args.from_index) or cardlib.chunk_albums(
        cards, cardlib.DEFAULT_ALBUM_CATEGORIES)
    manifest["note"] = "Bootstrap depuis la collection existante (noms et raretes d'origine)."

    cardlib.save_manifest(manifest)
    counts = count_by_rarity(cards)
    print(f"Manifeste cree : {cardlib.MANIFEST_PATH}")
    print(f"- {len(cards)} cartes ({len(manifest['albums'])} categories d'album, "
          f"{sum(len(a['sets']) for a in manifest['albums'])} sets)")
    for rarity, count in counts.items():
        print(f"- {rarity} : {count}")
    return 0


def cmd_reseed(args: argparse.Namespace) -> int:
    manifest = cardlib.load_manifest()
    cards = manifest["cards"]
    manifest["seed"] = args.seed
    rarities = cardlib.assign_rarities([c["id"] for c in cards],
                                       manifest["rarity_weights"], args.seed + 1)
    for card in cards:
        card["rarity"] = rarities[card["id"]]
    cardlib.save_manifest(manifest)
    print(f"Graine mise a jour : seed={args.seed}")
    for rarity, count in count_by_rarity(cards).items():
        print(f"- {rarity} : {count}")
    return 0


def count_by_rarity(cards: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for card in cards:
        counts[card["rarity"]] = counts.get(card["rarity"], 0) + 1
    return counts


def cmd_generate(args: argparse.Namespace) -> int:
    if not os.path.isfile(cardlib.MANIFEST_PATH):
        print(f"{cardlib.MANIFEST_PATH} introuvable : lance d'abord `python generate_cards.py --init`.")
        return 1

    manifest = cardlib.load_manifest()
    if args.migrate_names:
        manifest["cards"] = cardlib.build_cards_from_staging(
            cardlib.collect_staging(), manifest["seed"],
            manifest["rarity_weights"], manifest["default_emoji"])

    errors = cardlib.validate(manifest, check_disk=not args.skip_disk_check)
    if errors:
        print("Validation du manifeste : ECHEC")
        for error in errors:
            print(f"  - {error}")
        return 1

    if args.check:
        print("Validation du manifeste : OK")
        return 0

    total = cardlib.write_cards_data(manifest)
    print(f"{cardlib.DATA_PATH} genere : {total} cartes")
    for rarity, count in count_by_rarity(manifest["cards"]).items():
        print(f"- {rarity} : {count}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--init", action="store_true", help="cree le manifeste depuis images/")
    parser.add_argument("--force", action="store_true", help="avec --init, ecrase un manifeste existant")
    parser.add_argument("--from-index", default=cardlib.INDEX_PATH, metavar="PATH",
                        help="avec --init, fichier HTML contenant un ALBUMS_DB a recuperer")
    parser.add_argument("--check", action="store_true", help="valide le manifeste sans ecrire")
    parser.add_argument("--reseed", type=int, metavar="N", help="rejoue le tirage des raretes avec la graine N")
    parser.add_argument("--migrate-names", action="store_true",
                        help="regenere noms et raretes depuis le dossier de staging")
    parser.add_argument("--skip-disk-check", action="store_true", help="ne verifie pas la presence des images")
    args = parser.parse_args()

    if args.init:
        return cmd_init(args)
    if args.reseed is not None:
        return cmd_reseed(args)
    return cmd_generate(args)


if __name__ == "__main__":
    sys.exit(main())