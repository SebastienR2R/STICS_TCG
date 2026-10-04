"""Migre le dossier de staging image-stics/ vers images/ et regenere les donnees.

    python migrate_stics.py --dry-run    # preview, n'ecrit rien
    python migrate_stics.py              # migration complete
    python migrate_stics.py --seed 42    # autre tirage pour noms et raretes

Deroulement : les images de `image-stics/` sont copiees dans `images/` sous la
nomenclature `NNN<Nom>.png`, un `cards_manifest.json` est ecrit (noms et raretes
aleatoires a graine fixe), les anciennes images non referencees sont retirees, puis
`cards_data.js` est regenere. Le dossier de staging est supprime en dernier.

Codes de sortie : 0 = migration faite, 1 = erreur, 3 = rien a migrer.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys

import cardlib

EXPECTED_SIZE = (630, 880)


def dirty_paths() -> list[str]:
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--", cardlib.IMAGE_DIR, cardlib.DATA_PATH, cardlib.MANIFEST_PATH],
            capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    return [line for line in out.splitlines() if line.strip()]


def next_save_key(current: str) -> str:
    """Bump la version de la cle : tma_gacha_v1 -> tma_gacha_v2."""
    match = re.match(r"^(.*)_v(\d+)$", current)
    if match:
        return f"{match.group(1)}_v{int(match.group(2)) + 1}"
    return f"{current}_v2"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="n'ecrit rien, affiche le plan")
    parser.add_argument("--seed", type=int, help="graine du tirage des noms et raretes")
    parser.add_argument("--set-size", type=int, default=cardlib.ALBUM_SET_SIZE, help="taille des sets d'album")
    parser.add_argument("--keep-staging", action="store_true", help="ne supprime pas image-stics/")
    parser.add_argument("--keep-save-key", action="store_true", help="ne bump pas la cle de sauvegarde")
    args = parser.parse_args()

    sources = cardlib.collect_staging()
    if not sources:
        print(f"Aucune image dans {cardlib.STAGING_DIR}/ : rien a migrer.")
        print(f"Depose les illustrations dans {cardlib.STAGING_DIR}/ puis relance la commande.")
        return 3

    previous = cardlib.load_manifest() if os.path.isfile(cardlib.MANIFEST_PATH) else cardlib.default_manifest()
    seed = args.seed if args.seed is not None else previous.get("seed", 1337)
    emoji = previous.get("default_emoji", "\U0001f3ba")
    weights = previous.get("rarity_weights", cardlib.DEFAULT_RARITY_WEIGHTS)

    cards = cardlib.build_cards_from_staging(sources, seed, weights, emoji)
    manifest = cardlib.default_manifest()
    manifest["seed"] = seed
    manifest["cards"] = cards
    manifest["albums"] = cardlib.chunk_albums(cards, cardlib.DEFAULT_ALBUM_CATEGORIES, args.set_size)
    manifest["save_key"] = previous.get("save_key", "tma_gacha_v1") if args.keep_save_key else next_save_key(previous.get("save_key", "tma_gacha_v1"))
    manifest["note"] = f"Migration STICS depuis {cardlib.STAGING_DIR}/ (noms et raretes generes, seed={seed})."

    buckets = cardlib.report_sizes(cardlib.STAGING_DIR)
    unexpected = {size: names for size, names in buckets.items() if size != str(EXPECTED_SIZE)}

    kept = {os.path.basename(c["image"]) for c in previous.get("cards", [])}
    incoming = {os.path.basename(c["image"]) for c in cards}
    removed = sorted(name for name in cardlib.list_images(cardlib.IMAGE_DIR)
                     if name not in incoming and name in kept)

    print(f"Staging : {len(sources)} image(s) -> {len(cards)} carte(s), seed={seed}")
    for size, names in sorted(buckets.items()):
        flag = "" if size == str(EXPECTED_SIZE) else "   <- ratio inattendu"
        print(f"  {size} : {len(names)} image(s){flag}")
    if unexpected and args.dry_run:
        print("  (l'app ne rogne pas : ces images seront affichees deformees)")

    counts: dict[str, int] = {}
    for card in cards:
        counts[card["rarity"]] = counts.get(card["rarity"], 0) + 1
    print("Raretes : " + ", ".join(f"{r}={counts.get(r, 0)}" for r in manifest["rarities"]))
    print(f"Albums : {len(manifest['albums'])} categories, "
          f"{sum(len(a['sets']) for a in manifest['albums'])} sets de {args.set_size}")
    print(f"Cle de sauvegarde : {previous.get('save_key', 'tma_gacha_v1')} -> {manifest['save_key']}")
    print(f"Images retirees de {cardlib.IMAGE_DIR}/ : {len(removed)}")
    for card in cards[:5]:
        print(f"  exemple : {card['id']} {card['name']} ({card['rarity']}) <- {card['source']}")
    if len(cards) > 5:
        print(f"  ... +{len(cards) - 5}")

    if args.dry_run:
        print("\nDry run : rien n'a ete ecrit.")
        return 0

    dirty = dirty_paths()
    if dirty:
        print(f"\nAttention : {len(dirty)} fichier(s) versionne(s) deja modifie(s). "
              f"Commit ou stash avant de migrer pour pouvoir rollback.")

    errors = cardlib.validate(manifest, check_disk=False)
    if errors:
        print("Validation du manifeste : ECHEC")
        for error in errors:
            print(f"  - {error}")
        return 1

    for card in cards:
        source = os.path.join(cardlib.STAGING_DIR, card["source"])
        if os.path.abspath(source) != os.path.abspath(card["image"]):
            shutil.copy2(source, card["image"])

    for name in removed:
        os.remove(os.path.join(cardlib.IMAGE_DIR, name))

    cardlib.save_manifest(manifest)

    errors = cardlib.validate(manifest)
    if errors:
        print("Validation apres copie : ECHEC")
        for error in errors:
            print(f"  - {error}")
        return 1

    total = cardlib.write_cards_data(manifest)
    print(f"\n{cardlib.MANIFEST_PATH} et {cardlib.DATA_PATH} regeneres ({total} cartes).")

    if not args.keep_staging:
        shutil.rmtree(cardlib.STAGING_DIR)
        print(f"{cardlib.STAGING_DIR}/ supprime.")
    else:
        for source in sources:
            os.remove(os.path.join(cardlib.STAGING_DIR, source))
        print(f"{cardlib.STAGING_DIR}/ vide (conservee via --keep-staging).")

    return 0


if __name__ == "__main__":
    sys.exit(main())