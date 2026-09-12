import json
from pathlib import Path


# Input: MITRE ATT&CK Enterprise STIX data
INPUT_FILE = Path(
    "ai-rag/data/attack-stix-data/enterprise-attack/enterprise-attack.json"
)

# Output: Clean data for our RAG pipeline
OUTPUT_FILE = Path(
    "ai-rag/data/processed/mitre_techniques.json"
)


def main():
    print("Loading MITRE ATT&CK data...")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    objects = data.get("objects", [])

    print(f"Total STIX objects found: {len(objects)}")

    techniques = []

    for obj in objects:

        # We only want attack-pattern objects
        if obj.get("type") != "attack-pattern":
            continue

        # Ignore deprecated or revoked techniques
        if obj.get("deprecated", False):
            continue

        if obj.get("revoked", False):
            continue

        technique_id = None

        # Find the MITRE ATT&CK technique ID
        for reference in obj.get("external_references", []):
            source_name = reference.get("source_name", "")

            if source_name == "mitre-attack":
                external_id = reference.get("external_id", "")

                if external_id.startswith("T"):
                    technique_id = external_id
                    break

        # Skip objects without a MITRE technique ID
        if not technique_id:
            continue

        technique = {
            "id": technique_id,
            "name": obj.get("name", ""),
            "description": obj.get("description", ""),
            "url": ""
        }

        # Get the official MITRE URL
        for reference in obj.get("external_references", []):
            if reference.get("source_name") == "mitre-attack":
                technique["url"] = reference.get("url", "")
                break

        techniques.append(technique)

    # Make sure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save extracted techniques
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(techniques, file, indent=2, ensure_ascii=False)

    print(f"\nExtracted techniques: {len(techniques)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()