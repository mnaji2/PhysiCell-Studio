import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict

@dataclass
class RuleGORecord:
    rule_id: str
    cell_type: str
    signal: str
    behavior: str
    direction: str

    go_term_id: str
    go_term_name: str

    gene_ratio: str
    bg_ratio: str

    rich_factor: float
    fold_enrichment: float
    z_score: float

    p_value: float
    p_adjust: float
    q_value: float


def load_rules_from_csv(file_path: str) -> List[RuleGORecord]:
    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip().str.lower()

    records = []

    for _, row in df.iterrows():

        if pd.isna(row.get("rule_id")):
            continue

        record = RuleGORecord(
            rule_id=row["rule_id"],
            cell_type=row["cell_type"],
            signal=row["signal"],
            behavior=row["behavior"],
            direction=str(row.get("direction", "non-directional")).strip(),
            go_term_id=row["go_id"],
            go_term_name=row["go_name"],
            gene_ratio=row["gene_ratio"],
            bg_ratio=row["bg_ratio"],
            rich_factor=float(row["rich_factor"]),
            fold_enrichment=float(row["fold_enrichment"]),
            z_score=float(row["z_score"]),
            p_value=float(row["p_value"]),
            p_adjust=float(row["p_adjust"]),
            q_value=float(row["q_value"]),
        )

        records.append(record)

    print(f"[BIWT] Loaded {len(records)} rule-GO records.")
    return records


def build_candidate_rule_index(records: List[RuleGORecord]) -> Dict[Tuple[str, str], List[RuleGORecord]]:
    candidate_index = defaultdict(list)

    for r in records:
        key = (r.cell_type, r.signal)
        candidate_index[key].append(r)

    print(f"[BIWT] Built candidate index with {len(candidate_index)} entries.")
    return candidate_index


def get_candidate_rules(candidate_index, cell_type: str, signal: str) -> List[RuleGORecord]:
    return candidate_index.get((cell_type, signal), [])


def group_by_rule(records: List[RuleGORecord]) -> Dict[str, List[RuleGORecord]]:
    grouped = defaultdict(list)

    for r in records:
        grouped[r.rule_id].append(r)

    return grouped


def score_rule(go_records: List[RuleGORecord]) -> float:

    if not go_records:
        return 0.0

    avg_z = sum(r.z_score for r in go_records) / len(go_records)
    avg_p = sum(r.p_value for r in go_records) / len(go_records)
    avg_fe = sum(r.fold_enrichment for r in go_records) / len(go_records)

    score = 0.0

    return score


def rank_rules(records: List[RuleGORecord]) -> List[Tuple[str, float]]:
    grouped = group_by_rule(records)

    scores = []

    for rule_id, go_records in grouped.items():
        score = score_rule(go_records)
        scores.append((rule_id, score))

    return sorted(scores, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":

    records = load_rules_from_csv("biwt_protype_rules.csv")

    candidate_index = build_candidate_rule_index(records)

    cell_type = "cd4 t cell"
    signal = "interferon gradient"

    candidate_records = get_candidate_rules(candidate_index, cell_type, signal)

    print(f"\n[BIWT] Found {len(candidate_records)} GO records for candidate set.")

    rankings = rank_rules(candidate_records)

    print("\n[BIWT] Rule Rankings:\n")

    for rule_id, score in rankings:
        print(f"{rule_id}: {score:.4f}")