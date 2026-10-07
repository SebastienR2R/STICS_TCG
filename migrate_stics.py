"""Importe des images dans `images/` et regenere les donnees du jeu.

Deux modes :

    # Remplace toute la collection (ids 001..N, staging image-stics/)
    python migrate_stics.py --dry-run
    python migrate_stics.py

    # Ajoute les images d'un dossier quelconque a la collection existante
    python migrate_stics.py --append --source "Nouvelles cartes" --dry-run
    python migrate_stics.py --append --source "Nouvelles cartes"

En mode `--append`, les cartes deja publiees ne bougent pas : les nouveaux ids
commencent apres le plus grand id existant, les noms et les raretes deja tires
sont conserves, et la cle de sauvegarde n'est pas bumpee (l'inventaire des
joueurs reste valide). Les nouvelles cartes recoivent un nom, une rarete, une
description et des stats tires a graine fixe.

Codes de sortie : 0 = import fait, 1 = erreur, 3 = rien a importer.
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


def stage_sources(source_dir: str) -> tuple[list[str], list[str]]:
    """Liste les images a importer, avec des noms de fichier propres.

    Les copies de nommage different sont deposees dans le staging, qui sert de
    relais pour la copie finale vers `images/`. Retourne les noms propres et la
    liste des fichiers deposes.
    """
    raw = cardlib.collect_staging(source_dir)
    sources = [cardlib.sanitize_source_name(name) for name in raw]

    # Deux fichiers distincts peuvent se sanitizer vers le meme nom (accents et
    # %XX duplique par le nommage du navigateur) : on suffixe plutot que d'ignorer
    # une image, et on previent.
    seen: set[str] = set()
    for index, name in enumerate(sources):
        unique = name
        suffix = 2
        while unique.lower() in seen:
            stem, extension = os.path.splitext(name)
            unique = f"{stem}-{suffix}{extension}"
            suffix += 1
        if unique != name:
            print(f"  renomme {raw[index]} -> {unique} (doublon apres nettoyage)")
        seen.add(unique.lower())
        sources[index] = unique

    staged: list[str] = []
    if sources:
        staging = cardlib.STAGING_DIR
        os.makedirs(staging, exist_ok=True)
        for raw_name, clean_name in zip(raw, sources):
            if raw_name == clean_name:
                continue
            shutil.copy2(os.path.join(source_dir, raw_name), os.path.join(staging, clean_name))
            staged.append(clean_name)

    return sources, staged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="n'ecrit rien, affiche le plan")
    parser.add_argument("--seed", type=int, help="graine du tirage des noms, raretes et stats")
    parser.add_argument("--set-size", type=int, default=cardlib.ALBUM_SET_SIZE, help="taille des sets d'album")
    parser.add_argument("--keep-staging", action="store_true", help="ne supprime pas le dossier de staging")
    parser.add_argument("--keep-save-key", action="store_true", help="ne bump pas la cle de sauvegarde")
    parser.add_argument("--append", action="store_true",
                        help="ajoute les images a la collection existante au lieu de la remplacer")
    parser.add_argument("--source", metavar="DIR", help="dossier des images a importer (defaut : image-stics/)")
    parser.add_argument("--no-descriptions", action="store_true", help="ne remplit pas le champ `description`")
    parser.add_argument("--force-import", action="store_true",
                        help="avec --append, reimporte meme les images deja references comme source")
    args = parser.parse_args()

    if args.append and args.keep_save_key:
        print("--append ne bump pas la cle de sauvegarde : --keep-save-key est ignore.")
    if args.append and not args.source:
        parser.error("--append exige --source (la collection existante n'est pas remplacee).")

    source_dir = args.source or cardlib.STAGING_DIR
    if not os.path.isdir(source_dir):
        print(f"Dossier '{source_dir}' introuvable.")
        print("Depose les illustrations dans ce dossier puis relance la commande.")
        return 3

    raw = cardlib.collect_staging(source_dir)
    if not raw:
        print(f"Aucune image dans {source_dir}/ : rien a importer.")
        return 3

    previous = cardlib.load_manifest() if os.path.isfile(cardlib.MANIFEST_PATH) else cardlib.default_manifest()

    sources, staged = stage_sources(source_dir)

    if args.append and not args.force_import:
        # Rejouer la meme commande ne doit pas dupliquer les cartes : un fichier
        # deja reference comme `source` d'une carte est considere comme importe.
        imported = {card.get("source") for card in previous.get("cards", [])}
        fresh = [name for name in sources if name not in imported]
        if not fresh:
            print(f"Les {len(sources)} image(s) de {source_dir}/ sont deja importees.")
            print("Utilise --force-import pour les rejouer (nouveaux noms, nouvelles raretes).")
            return 3
        if len(fresh) != len(sources):
            print(f"{len(sources) - len(fresh)} image(s) deja importee(s), ignoree(s).")
        sources = fresh

    existing = previous.get("cards", []) if args.append else []
    seed = args.seed if args.seed is not None else previous.get("seed", 1337)
    emoji = previous.get("default_emoji", "\U0001f3ba")
    weights = previous.get("rarity_weights", cardlib.DEFAULT_RARITY_WEIGHTS)

    new_cards = (cardlib.build_new_cards(sources, existing, seed, weights, emoji)
                 if args.append else
                 cardlib.build_cards_from_staging(sources, seed, weights, emoji))

    manifest = cardlib.default_manifest()
    manifest["seed"] = seed
    manifest["cards"] = existing + new_cards
    # Les albums deja publies sont repris tels quels (ils sont curates a la
    # main) ; les nouvelles cartes rejoignent « Non classé ».
    manifest["albums"] = previous.get("albums", []) if args.append else []
    unclassified = cardlib.sync_albums(manifest, args.set_size)
    manifest["save_key"] = previous.get("save_key", "tma_gacha_v1")
    if not args.keep_save_key and not args.append:
        manifest["save_key"] = next_save_key(manifest["save_key"])
    mode = "Ajout" if args.append else "Migration"
    manifest["note"] = (f"{mode} depuis {source_dir}/ "
                        f"(noms, raretes et stats generes, seed={seed}).")

    if not args.no_descriptions:
        cardlib.apply_descriptions(manifest)
    cardlib.apply_stats(manifest)

    buckets = cardlib.report_sizes(source_dir)
    unexpected = {size: names for size, names in buckets.items() if size != str(EXPECTED_SIZE)}

    kept = {os.path.basename(c["image"]) for c in previous.get("cards", [])}
    incoming = {os.path.basename(c["image"]) for c in manifest["cards"]}
    removed = [] if args.append else sorted(
        name for name in cardlib.list_images(cardlib.IMAGE_DIR) if name not in incoming and name in kept)

    first_id = new_cards[0]["id"]
    last_id = new_cards[-1]["id"]
    print(f"{mode} : {len(sources)} image(s) depuis {source_dir}/ -> "
          f"{len(manifest['cards'])} carte(s) au total, seed={seed}")
    print(f"  ids {first_id}..{last_id} ({len(manifest['cards']) - len(existing)} nouvelles cartes)")
    for size, names in sorted(buckets.items()):
        flag = "" if size == str(EXPECTED_SIZE) else "   <- ratio inattendu"
        print(f"  {size} : {len(names)} image(s){flag}")
    if unexpected and args.dry_run:
        print("  (l'app affiche la photo en entier sur un fond floute : aucun recadrage, "
              "seule la taille des lettres change)")

    counts: dict[str, int] = {}
    for card in manifest["cards"]:
        counts[card["rarity"]] = counts.get(card["rarity"], 0) + 1
    print("Raretes : " + ", ".join(f"{r}={counts.get(r, 0)}" for r in manifest["rarities"]))
    print(f"Albums : {len(manifest['albums'])} categories, "
          f"{sum(len(a['sets']) for a in manifest['albums'])} sets de {args.set_size} "
          f"({unclassified} carte(s) en « {cardlib.UNCLASSIFIED_ALBUM['title']} »)")
    if args.append:
        print(f"Cle de sauvegarde inchangee : {manifest['save_key']} "
              f"({len(existing)} cartes conservees, ids non reutilises)")
    else:
        print(f"Cle de sauvegarde : {previous.get('save_key', 'tma_gacha_v1')} -> {manifest['save_key']}")
    print(f"Images retirees de {cardlib.IMAGE_DIR}/ : {len(removed)}")
    for card in new_cards[:5]:
        print(f"  exemple : {card['id']} {card['name']} ({card['rarity']}) "
              f"[{card['image']}] - {card['description']} | "
              f"{card['attack']['name']} {card['attack']['power']}")
    if len(new_cards) > 5:
        print(f"  ... +{len(new_cards) - 5}")

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

    for card in new_cards:
        origin = os.path.join(source_dir, card["source"])
        if not os.path.isfile(origin):
            origin = os.path.join(cardlib.STAGING_DIR, card["source"])
        if os.path.abspath(origin) != os.path.abspath(card["image"]):
            shutil.copy2(origin, card["image"])

    for name in removed:
        os.remove(os.path.join(cardlib.IMAGE_DIR, name))

    # Le manifeste n'est ecrit qu'une fois les images en place et l'etat du disque
    # valide : un echec laisse donc le manifeste d'avant, relisible tel quel.
    errors = cardlib.validate(manifest)
    if errors:
        print("Validation apres copie : ECHEC (manifeste non ecrit)")
        for error in errors:
            print(f"  - {error}")
        return 1

    cardlib.save_manifest(manifest)

    total = cardlib.write_cards_data(manifest)
    print(f"\n{cardlib.MANIFEST_PATH} et {cardlib.DATA_PATH} regeneres ({total} cartes).")

    if args.append:
        print(f"{source_dir}/ conserve (les images d'origine ne sont pas supprimees).")
        # Toutes les copies de staging de ce run sont temporaires, y compris celles
        # d'images deja importees et donc ecartees de la selection.
        for name in staged:
            os.remove(os.path.join(cardlib.STAGING_DIR, name))
    elif args.keep_staging:
        print(f"{cardlib.STAGING_DIR}/ vide (conserve via --keep-staging).")
        for name in os.listdir(cardlib.STAGING_DIR):
            os.remove(os.path.join(cardlib.STAGING_DIR, name))
    else:
        shutil.rmtree(cardlib.STAGING_DIR, ignore_errors=True)
        print(f"{cardlib.STAGING_DIR}/ supprime.")

    return 0


if __name__ == "__main__":
    sys.exit(main())