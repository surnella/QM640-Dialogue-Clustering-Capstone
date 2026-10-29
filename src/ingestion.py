"""
Ingestion Pipeline for Dialogue Datasets:
1. Microsoft Frames (Wizard-of-Oz holiday travel negotiation)
2. MultiWOZ 2.2 (Multi-domain task-oriented benchmark)
3. Enterprise Golden Travel Counseling Benchmark
"""

import os
import sys
import json
import re
import glob
import pandas as pd
from typing import List, Dict, Any

try:
    from src.canonical_schema import (
        Tier1UniversalSlots,
        Tier2EnterpriseSlots,
        CanonicalTurn,
        CanonicalDialogueTrajectory,
    )
except ModuleNotFoundError:
    from canonical_schema import (
        Tier1UniversalSlots,
        Tier2EnterpriseSlots,
        CanonicalTurn,
        CanonicalDialogueTrajectory,
    )


HESITATION_KEYWORDS = set([
    "maybe", "perhaps", "not sure", "thinking", "might", "could",
    "wondering", "flexible", "options", "cheaper", "alternate",
    "recommend", "suggest", "any other", "budget", "expensive", "change"
])


def extract_hesitation_count(text: str) -> int:
    text_lower = text.lower()
    return sum(1 for kw in HESITATION_KEYWORDS if kw in text_lower)


def parse_frames_dataset(frames_json_path: str, max_records: int = None) -> List[CanonicalDialogueTrajectory]:
    """
    Parses the Microsoft Frames corpus into CanonicalDialogueTrajectory objects.
    """
    if not os.path.exists(frames_json_path):
        raise FileNotFoundError(f"Frames JSON not found at: {frames_json_path}")

    with open(frames_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    trajectories = []
    if max_records:
        data = data[:max_records]

    for d in data:
        dialogue_id = d.get('id', 'unknown')
        turns_data = d.get('turns', [])
        
        canonical_t1 = Tier1UniversalSlots()
        canonical_t2 = Tier2EnterpriseSlots()
        
        user_turns = 0
        wizard_turns = 0
        canonical_turns = []
        revisions_count = 0
        total_hesitations = 0
        seen_slots = {}

        for idx, t in enumerate(turns_data):
            author = t.get('author', 'user')
            text = t.get('text', '')
            if author == 'user':
                user_turns += 1
                total_hesitations += extract_hesitation_count(text)
            else:
                wizard_turns += 1

            turn_slots = {}
            acts_list = []
            turn_revisions = []

            labels = t.get('labels', {})
            for act in labels.get('acts', []):
                act_name = act.get('name', '')
                acts_list.append(act_name)
                for arg in act.get('args', []):
                    key = arg.get('key')
                    val = arg.get('val')
                    if key and val:
                        turn_slots[key] = val
                        # Check revision
                        if key in seen_slots and seen_slots[key] != val:
                            revisions_count += 1
                            turn_revisions.append(key)
                        seen_slots[key] = val

                        # Map to Tier 1
                        if key == 'or_city' and not canonical_t1.origin_city:
                            canonical_t1.origin_city = str(val)
                        elif key == 'dst_city' and not canonical_t1.destination_city:
                            canonical_t1.destination_city = str(val)
                        elif key == 'str_date' and not canonical_t1.departure_date:
                            canonical_t1.departure_date = str(val)
                        elif key == 'end_date' and not canonical_t1.return_date:
                            canonical_t1.return_date = str(val)
                        elif key in ['n_adults', 'n_adult']:
                            try:
                                canonical_t1.traveler_count_adults = int(val)
                            except (ValueError, TypeError):
                                pass
                        elif key in ['n_children', 'n_child']:
                            try:
                                canonical_t1.traveler_count_children = int(val)
                            except (ValueError, TypeError):
                                pass
                        elif key == 'budget':
                            try:
                                clean_val = re.sub(r'[^\d.]', '', str(val))
                                if clean_val:
                                    canonical_t1.budget_amount = float(clean_val)
                            except (ValueError, TypeError):
                                pass

            canonical_turns.append(CanonicalTurn(
                turn_id=idx + 1,
                speaker=author,
                utterance=text,
                acts=acts_list,
                slots_mentioned=turn_slots,
                revisions=turn_revisions
            ))

        traj = CanonicalDialogueTrajectory(
            dialogue_id=f"frames_{dialogue_id}",
            source_dataset="frames",
            total_turns=len(turns_data),
            user_turns=user_turns,
            wizard_turns=wizard_turns,
            canonical_tier1=canonical_t1,
            canonical_tier2=canonical_t2,
            turns=canonical_turns,
            revisions_count=revisions_count,
            budget_specified=(canonical_t1.budget_amount is not None),
            hesitation_markers_count=total_hesitations
        )
        trajectories.append(traj)

    print(f"Parsed {len(trajectories)} dialogues from Microsoft Frames.")
    return trajectories


def parse_multiwoz_dataset(multiwoz_dir: str, max_records: int = 1500) -> List[CanonicalDialogueTrajectory]:
    """
    Parses MultiWOZ 2.2 dialogues across hotel, attraction, flight, and taxi domains.
    """
    json_files = glob.glob(os.path.join(multiwoz_dir, '**', 'dialogues_*.json'), recursive=True)
    if not json_files:
        print(f"No MultiWOZ files found in {multiwoz_dir}")
        return []

    trajectories = []
    count = 0

    for jf in sorted(json_files):
        with open(jf, 'r', encoding='utf-8') as f:
            dialogues = json.load(f)

        for d in dialogues:
            if max_records and count >= max_records:
                break

            dialogue_id = d.get('dialogue_id', 'unknown')
            services = d.get('services', [])
            
            # Focus on travel domains
            travel_services = [s for s in services if s in ['hotel', 'attraction', 'train', 'taxi']]
            if not travel_services:
                continue

            turns_data = d.get('turns', [])
            canonical_t1 = Tier1UniversalSlots()
            canonical_t2 = Tier2EnterpriseSlots()

            user_turns = 0
            sys_turns = 0
            canonical_turns = []
            revisions_count = 0
            total_hesitations = 0
            seen_slots = {}

            for idx, t in enumerate(turns_data):
                speaker = t.get('speaker', 'USER').lower()
                utterance = t.get('utterance', '')
                if speaker == 'user':
                    user_turns += 1
                    total_hesitations += extract_hesitation_count(utterance)
                else:
                    sys_turns += 1

                turn_slots = {}
                frames_list = t.get('frames', [])
                for frame in frames_list:
                    service = frame.get('service', '')
                    slots = frame.get('slots', [])
                    for s in slots:
                        slot_name = f"{service}-{s.get('slot', '')}"
                        val = s.get('value', '')
                        turn_slots[slot_name] = val
                        if slot_name in seen_slots and seen_slots[slot_name] != val:
                            revisions_count += 1
                        seen_slots[slot_name] = val

                        # Canonical Tier 1 mapping
                        if 'destination' in slot_name and not canonical_t1.destination_city:
                            canonical_t1.destination_city = str(val)
                        elif 'departure' in slot_name and not canonical_t1.origin_city:
                            canonical_t1.origin_city = str(val)
                        elif 'day' in slot_name and not canonical_t1.departure_date:
                            canonical_t1.departure_date = str(val)
                        elif 'stars' in slot_name:
                            canonical_t1.accommodation_tier = f"{val}-star"
                        elif 'pricerange' in slot_name:
                            canonical_t1.accommodation_tier = str(val)

                canonical_turns.append(CanonicalTurn(
                    turn_id=idx + 1,
                    speaker=speaker,
                    utterance=utterance,
                    slots_mentioned=turn_slots
                ))

            traj = CanonicalDialogueTrajectory(
                dialogue_id=f"mwoz_{dialogue_id}",
                source_dataset="multiwoz",
                total_turns=len(turns_data),
                user_turns=user_turns,
                wizard_turns=sys_turns,
                canonical_tier1=canonical_t1,
                canonical_tier2=canonical_t2,
                turns=canonical_turns,
                revisions_count=revisions_count,
                budget_specified=(canonical_t1.accommodation_tier is not None),
                hesitation_markers_count=total_hesitations
            )
            trajectories.append(traj)
            count += 1

    print(f"Parsed {len(trajectories)} dialogues from MultiWOZ 2.2.")
    return trajectories


def export_canonical_dataset(
    trajectories: List[CanonicalDialogueTrajectory],
    output_json_path: str = "data/canonical/canonical_dialogues.json",
    output_summary_csv: str = "data/canonical/dialogue_summary.csv"
):
    """
    Serializes canonical dialogue trajectories to JSON and exports tabular summary CSV.
    """
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    # Save JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump([t.model_dump() for t in trajectories], f, indent=2)
    print(f"Saved full canonical trajectories to {output_json_path}")

    # Create summary DataFrame for statistical EDA
    records = []
    for t in trajectories:
        records.append({
            "dialogue_id": t.dialogue_id,
            "source_dataset": t.source_dataset,
            "total_turns": t.total_turns,
            "user_turns": t.user_turns,
            "wizard_turns": t.wizard_turns,
            "revisions_count": t.revisions_count,
            "hesitation_markers_count": t.hesitation_markers_count,
            "budget_specified": t.budget_specified,
            "budget_amount": t.canonical_tier1.budget_amount,
            "origin_city": t.canonical_tier1.origin_city,
            "destination_city": t.canonical_tier1.destination_city,
            "adults": t.canonical_tier1.traveler_count_adults,
            "children": t.canonical_tier1.traveler_count_children,
            "turn_ratio": t.user_turns / max(1, t.wizard_turns),
            "avg_utterance_len": sum(len(turn.utterance) for turn in t.turns) / max(1, len(t.turns))
        })

    df = pd.DataFrame(records)
    df.to_csv(output_summary_csv, index=False)
    print(f"Saved dataset summary to {output_summary_csv} (Shape: {df.shape})")
    return df


if __name__ == "__main__":
    frames_path = "data/raw/frames/Frames-dataset/frames.json"
    multiwoz_path = "data/raw/multiwoz22"

    all_trajectories = []
    if os.path.exists(frames_path):
        all_trajectories.extend(parse_frames_dataset(frames_path))
    
    if os.path.exists(multiwoz_path):
        all_trajectories.extend(parse_multiwoz_dataset(multiwoz_path, max_records=1500))

    df_summary = export_canonical_dataset(all_trajectories)
    print("Ingestion pipeline completed successfully.")
