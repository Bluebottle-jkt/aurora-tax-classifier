from __future__ import annotations
import json, re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any

@dataclass
class LabelResult:
    invoice_side: str
    primary_label_id: str
    ancestor_path: List[str]
    facets_resolved: Dict[str, Any]
    confidence_0_100: int
    evidence_terms: List[str]
    leaf_generator_rule_id: Optional[str] = None
    suggested_new_leaf_node: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class Ontology:
    def __init__(self, ontology_json: Dict[str, Any]):
        self.ontology = ontology_json
        self.nodes = {n["id"]: n for n in ontology_json["nodes"]}
        self.children = {}
        for n in ontology_json["nodes"]:
            p = n.get("parent")
            if p:
                self.children.setdefault(p, []).append(n["id"])

    @classmethod
    def load(cls, path: str) -> "Ontology":
        with open(path, "r", encoding="utf-8") as f:
            return cls(json.load(f))

    def get_ancestors(self, node_id: str) -> List[str]:
        path = []
        cur = node_id
        while cur:
            path.append(cur)
            cur = self.nodes.get(cur, {}).get("parent")
        return list(reversed(path))

    def merge_facets(self, node_id: str) -> Dict[str, Any]:
        # Merge facets from ancestors to leaf (leaf wins)
        facets = {}
        for nid in self.get_ancestors(node_id):
            f = self.nodes.get(nid, {}).get("facets", {})
            if isinstance(f, dict):
                facets.update(f)
        return facets

def _compile_patterns(node: Dict[str, Any]) -> List[re.Pattern]:
    pats = []
    cw = node.get("crosswalk", {}) or {}
    for p in cw.get("patterns", []) or []:
        pats.append(re.compile(p))
    # synonyms -> simple word boundary contains
    for s in cw.get("synonyms", []) or []:
        # treat as substring search; compile case-insensitive
        pats.append(re.compile(re.escape(s), re.IGNORECASE))
    return pats

class InvoiceLabeler:
    def __init__(self, ontology: Ontology):
        self.onto = ontology
        # Precompile patterns for all nodes
        self.node_patterns: Dict[str, List[re.Pattern]] = {nid: _compile_patterns(n) for nid, n in self.onto.nodes.items()}
        self.leaf_rules = ontology.ontology.get("leaf_generator", {}).get("rules", [])

    def _match_best_existing_leaf(self, text: str, invoice_side: str) -> Tuple[Optional[str], List[str], int]:
        """
        Returns (best_node_id, evidence_terms, score).
        Score: simple heuristic count of matched patterns; prefer deeper nodes.
        """
        best = None
        best_score = 0
        best_evidence = []
        for nid, node in self.onto.nodes.items():
            # Restrict to side roots
            if invoice_side == "output":
                if "PPN_OUTPUT" not in self.onto.get_ancestors(nid):
                    continue
            elif invoice_side == "input":
                if "PPN_INPUT" not in self.onto.get_ancestors(nid):
                    continue
            else:
                continue

            pats = self.node_patterns.get(nid, [])
            if not pats:
                continue
            matches = []
            for pat in pats:
                m = pat.search(text)
                if m:
                    matches.append(m.group(0))
            if matches:
                depth = len(self.onto.get_ancestors(nid))
                score = len(matches) * 10 + depth  # pattern count dominates, depth breaks ties
                if score > best_score:
                    best = nid
                    best_score = score
                    best_evidence = list(dict.fromkeys([x.strip() for x in matches if x.strip()]))[:8]
        return best, best_evidence, best_score

    def _apply_leaf_generator(self, text: str, invoice_side: str) -> Tuple[Optional[str], Optional[Dict[str, Any]], Optional[str], List[str]]:
        """
        If rule matches, suggest a new leaf node under chosen parent.
        Returns (parent_leaf_or_group_id, suggested_new_leaf_node, rule_id, evidence_terms)
        """
        for rule in self.leaf_rules:
            if rule.get("scope") != invoice_side:
                continue
            if not re.search(rule["if_text_matches"], text):
                continue

            rule_id = rule["id"]
            evidence = [m.group(0) for m in re.finditer(rule["if_text_matches"], text, flags=re.IGNORECASE)]
            # decide parent
            parent = rule.get("default_parent") or rule.get("then_assign_parent")
            cand = rule.get("then_assign_parent_candidates")
            if cand:
                chosen = None
                for c in cand:
                    if any(k.lower() in text.lower() for k in c.get("if_contains_any", [])):
                        chosen = c["parent"]
                        break
                parent = chosen or parent

            # create leaf id key (very conservative: do not include dates)
            key = re.sub(r"(?i)\b(periode|period|jan|feb|mar|apr|mei|jun|jul|aug|agu|sep|oct|okt|nov|dec|des)\b", " ", text)
            key = re.sub(r"\b20\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{1,2}-\d{1,2}-\d{2,4}\b", " ", key)
            key = re.sub(r"[^0-9A-Za-z]+", "_", key).strip("_")
            key = "_".join([t for t in key.split("_") if len(t) > 2][:6]) or "GENERIC"
            leaf_id = f"{'REV' if invoice_side=='output' else 'COST'}_AUTO_{rule_id}_{key}".upper()[:80]

            suggested = {
                "id": leaf_id,
                "type": "object",
                "label": f"AutoLeaf ({invoice_side}) - {key}",
                "parent": parent,
                "crosswalk": { "patterns": [rf"(?i){re.escape(text[:80])}"] },
                "facets": {
                    "evidence_strength": "low"
                }
            }
            return parent, suggested, rule_id, list(dict.fromkeys([e.strip() for e in evidence if e.strip()]))[:8]
        return None, None, None, []

    def label_one(self, text: str, invoice_side: str) -> LabelResult:
        best, evidence, score = self._match_best_existing_leaf(text, invoice_side)

        if best:
            conf = min(95, max(55, score))  # heuristic
            return LabelResult(
                invoice_side=invoice_side,
                primary_label_id=best,
                ancestor_path=self.onto.get_ancestors(best),
                facets_resolved=self.onto.merge_facets(best),
                confidence_0_100=int(conf),
                evidence_terms=evidence
            )

        # if nothing matched, use generator
        parent, suggested, rid, ev2 = self._apply_leaf_generator(text, invoice_side)
        if suggested:
            return LabelResult(
                invoice_side=invoice_side,
                primary_label_id=suggested["id"],  # provisional
                ancestor_path=self.onto.get_ancestors(parent) + [suggested["id"]],
                facets_resolved=self.onto.merge_facets(parent),
                confidence_0_100=40,
                evidence_terms=ev2,
                leaf_generator_rule_id=rid,
                suggested_new_leaf_node=suggested,
                notes="No existing leaf matched; suggested new leaf node."
            )

        # fallback catch-all
        fallback = "REV_PLATFORM" if invoice_side == "output" else "COST_GENERAL"
        return LabelResult(
            invoice_side=invoice_side,
            primary_label_id=fallback,
            ancestor_path=self.onto.get_ancestors(fallback),
            facets_resolved=self.onto.merge_facets(fallback),
            confidence_0_100=25,
            evidence_terms=[],
            notes="Fallback due to no match."
        )
