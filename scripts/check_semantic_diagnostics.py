#!/usr/bin/env python3
"""Validate diagnostic data structure, never infer semantic correctness from labels."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
FILES = ('cases.json', 'additional-cases.json')
READER_CASES = 'reader-cases-2026-09-10.json'
TEXT_FIELDS = ('id', 'focus', 'evidence', 'bad', 'control', 'expected_failure', 'control_boundary')

def validate_catalog(documents):
    identifiers = set()
    for name, document in documents:
        if not isinstance(document, dict):
            raise ValueError(f'{name}: expected object')
        if (type(document.get('schema_version')) is not int or document.get('schema_version') != 1
                or document.get('purpose') != 'diagnostic_only'
                or document.get('labels') != 'author_proposed_uncalibrated'
                or document.get('held_out') is not False
                or document.get('automatic_quality_scoring') is not False):
            raise ValueError(f'{name}: diagnostic-only claim boundary changed')
        cases = document.get('cases')
        if not isinstance(cases, list) or not cases:
            raise ValueError(f'{name}: nonempty cases required')
        for index, case in enumerate(cases):
            if not isinstance(case, dict):
                raise ValueError(f'{name}:{index}: expected case object')
            for key in TEXT_FIELDS:
                if not isinstance(case.get(key), str) or not case[key].strip():
                    raise ValueError(f'{name}:{index}: missing {key}')
            if not re.fullmatch(r'[a-z][a-z0-9_]*', case['id']):
                raise ValueError(f'{name}:{index}: id must be a canonical lowercase identifier')
            if case['id'] in identifiers:
                raise ValueError(f'duplicate diagnostic id: {case["id"]}')
            identifiers.add(case['id'])
            if type(case.get('critical_fact_failure')) is not bool:
                raise ValueError(f'{name}:{index}: critical_fact_failure must be boolean')
            if case['bad'].strip() == case['control'].strip():
                raise ValueError(f'{name}:{index}: identical bad and control excerpts')
    return identifiers

def load_history():
    return [(name, json.loads((ROOT / 'evals/semantic_diagnostics' / name).read_text(encoding='utf-8')))
            for name in FILES]

def case_digest(case):
    return hashlib.sha256(json.dumps(case,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def apply_revisions(documents, revision_document):
    validate_catalog(documents)
    if (type(revision_document.get('schema_version')) is not int or revision_document['schema_version']!=1
        or revision_document.get('purpose')!='diagnostic_only'
        or revision_document.get('labels')!='author_proposed_uncalibrated'
        or revision_document.get('held_out') is not False
        or revision_document.get('automatic_quality_scoring') is not False):
        raise ValueError('Revision claim boundary changed')
    revisions=revision_document.get('revisions')
    if not isinstance(revisions,list) or not revisions: raise ValueError('Missing revisions')
    result=copy.deepcopy(documents)
    lookup={c['id']:c for _,d in result for c in d['cases']}
    seen=set()
    for revision in revisions:
        if not isinstance(revision,dict): raise ValueError('Invalid revision')
        target=revision.get('case_id')
        if target not in lookup or target in seen: raise ValueError('Unknown or duplicate revision target')
        seen.add(target)
        case=lookup[target]
        if case_digest(case)!=revision.get('base_case_sha256'): raise ValueError('Revision base changed')
        identifier=revision.get('revision_id')
        if not isinstance(identifier,str) or not re.fullmatch(re.escape(target)+r'_r[2-9][0-9]*',identifier):
            raise ValueError('Invalid revision identity')
        changes=revision.get('changes')
        if not isinstance(changes,dict) or not changes or set(changes)-{'evidence','bad','control','expected_failure','control_boundary'}:
            raise ValueError('Invalid revision fields')
        if not isinstance(revision.get('reason'),str) or not revision['reason'].strip(): raise ValueError('Missing revision reason')
        case.update(changes)
        case['revision_id']=identifier
    validate_catalog(result)
    return result

def load_revisions():
    return json.loads((ROOT/'evals/semantic_diagnostics/revisions.json').read_text(encoding='utf-8'))

def load_reader_history():
    return [(READER_CASES, json.loads(
        (ROOT / 'evals/semantic_diagnostics' / READER_CASES).read_text(encoding='utf-8')))]


def load_reader_revisions():
    return json.loads((ROOT / 'evals/semantic_diagnostics/reader-revisions-2026-09-11.json')
                      .read_text(encoding='utf-8'))


def load_catalog():
    """Current development view; raw historical files are never overwritten."""
    current = apply_revisions(load_history(), load_revisions())
    current.extend(apply_revisions(load_reader_history(), load_reader_revisions()))
    validate_catalog(current)
    return current

def load_defect_tags():
    taxonomy = json.loads((ROOT / 'evals/rubrics/necessary-defects.v1.json').read_text(encoding='utf-8'))
    tags = json.loads((ROOT / 'evals/semantic_diagnostics/defect-tags.v1.json').read_text(encoding='utf-8'))
    return taxonomy, tags


def validate_defect_tags(documents, taxonomy, overlay):
    """Check label identity and version binding, not the truth of a proposed defect."""
    version = 'necessary-defects-v1'
    if (taxonomy.get('taxonomy_version') != version
            or taxonomy.get('purpose') != 'stable_finding_categories_not_quality_scores'):
        raise ValueError('Defect taxonomy boundary changed')
    identifiers = set()
    for label in taxonomy.get('labels', []):
        identity = label.get('id')
        if not isinstance(identity, str) or not re.fullmatch(r'ND[0-9]{2}', identity) or identity in identifiers:
            raise ValueError('Invalid or duplicate defect label')
        identifiers.add(identity)
        for field in ('name', 'definition', 'boundary'):
            values = label.get(field)
            if not isinstance(values, dict) or any(
                    not isinstance(values.get(lang), str) or not values[lang].strip() for lang in ('en', 'zh')):
                raise ValueError('Defect labels require bilingual definitions and boundaries')
    if not identifiers:
        raise ValueError('Missing defect labels')
    if (overlay.get('taxonomy_version') != version or overlay.get('purpose') != 'diagnostic_only'
            or overlay.get('labels') != 'author_proposed_uncalibrated'
            or overlay.get('held_out') is not False or overlay.get('automatic_quality_scoring') is not False):
        raise ValueError('Defect overlay claim boundary changed')
    validate_catalog(documents)
    lookup = {case['id']: case for _, document in documents for case in document['cases']}
    seen = set()
    for row in overlay.get('cases', []):
        identity = row.get('case_id')
        if identity not in lookup or identity in seen:
            raise ValueError('Unknown or duplicate defect-tag case')
        seen.add(identity)
        if row.get('case_sha256') != case_digest(lookup[identity]):
            raise ValueError('Defect tags refer to a different case version')
        tags = row.get('tags')
        if (not isinstance(tags, list) or not tags or any(not isinstance(t, str) for t in tags)
                or len(tags) != len(set(tags)) or not set(tags) <= identifiers):
            raise ValueError('Unknown, empty or duplicate defect tags')
    if seen != set(lookup):
        raise ValueError('Defect overlay must cover the current catalog')
    return seen


class DiagnosticDataTests(unittest.TestCase):
    def setUp(self):
        self.documents = copy.deepcopy(load_catalog())

    def test_defect_tags_bind_current_cases_without_rewriting_history(self):
        before = copy.deepcopy(self.documents)
        taxonomy, overlay = load_defect_tags()
        self.assertEqual(len(validate_defect_tags(self.documents, taxonomy, overlay)), 23)
        self.assertEqual(self.documents, before)

    def test_defect_tags_reject_stale_unknown_and_efficacy_labels(self):
        taxonomy, original = load_defect_tags()
        changes = (
            lambda doc: doc['cases'][0].update(case_sha256='0' * 64),
            lambda doc: doc['cases'][0].update(tags=['ND99']),
            lambda doc: doc['cases'].append(copy.deepcopy(doc['cases'][0])),
            lambda doc: doc['cases'].pop(),
            lambda doc: doc.update(held_out=True),
            lambda doc: doc.update(labels='independently_verified'),
        )
        for change in changes:
            with self.subTest(change=change):
                overlay = copy.deepcopy(original)
                change(overlay)
                with self.assertRaises(ValueError):
                    validate_defect_tags(self.documents, taxonomy, overlay)
        del taxonomy['labels'][0]['definition']['zh']
        with self.assertRaises(ValueError):
            validate_defect_tags(self.documents, taxonomy, original)

    def test_current_catalog(self):
        self.assertEqual(len(validate_catalog(self.documents)), 23)

    def test_original_six_preserved(self):
        self.assertEqual(len(self.documents[0][1]['cases']), 6)

    def test_duplicate_across_files(self):
        self.documents[1][1]['cases'][0]['id'] = self.documents[0][1]['cases'][0]['id']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_missing_control(self):
        del self.documents[1][1]['cases'][0]['control']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_missing_evidence(self):
        self.documents[1][1]['cases'][0]['evidence'] = ' '
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_identical_excerpts(self):
        case = self.documents[1][1]['cases'][0]
        case['control'] = case['bad']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_no_automatic_quality_promotion(self):
        self.documents[0][1]['automatic_quality_scoring'] = True
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_no_heldout_promotion(self):
        self.documents[0][1]['held_out'] = True
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_string_boolean_rejected(self):
        self.documents[0][1]['cases'][0]['critical_fact_failure'] = 'false'
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_count_does_not_establish_quality(self):
        self.documents[0][1]['cases'][0]['control'] = 'An author-proposed label can still be wrong.'
        self.assertEqual(len(validate_catalog(self.documents)), 23)

    def test_boolean_schema_rejected(self):
        self.documents[0][1]['schema_version'] = True
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_nonlist_cases_rejected(self):
        self.documents[0][1]['cases'] = {'id': 'not_a_case_list'}
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_noncanonical_identifier_rejected(self):
        self.documents[0][1]['cases'][0]['id'] += ' '
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_missing_boundary_rejected(self):
        del self.documents[0][1]['cases'][0]['control_boundary']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_history_unchanged_by_materialization(self):
        history=load_history(); before=copy.deepcopy(history)
        current=apply_revisions(history,load_revisions())
        self.assertEqual(history,before)
        self.assertIn('4次可用结果',history[0][1]['cases'][0]['control'])
        self.assertIn('不等于4个整体可用结果',current[0][1]['cases'][0]['control'])

    def test_revision_parent_tamper_rejected(self):
        history=load_history(); history[0][1]['cases'][0]['control']+='changed'
        with self.assertRaises(ValueError): apply_revisions(history,load_revisions())

    def test_unknown_revision_target_rejected(self):
        revisions=load_revisions(); revisions['revisions'][0]['case_id']='not_an_existing_case'
        with self.assertRaises(ValueError): apply_revisions(load_history(),revisions)

    def test_duplicate_revision_rejected(self):
        revisions=load_revisions(); revisions['revisions'].append(copy.deepcopy(revisions['revisions'][0]))
        with self.assertRaises(ValueError): apply_revisions(load_history(),revisions)

    def test_revision_cannot_change_case_identity(self):
        revisions=load_revisions(); revisions['revisions'][0]['changes']['id']='new_case'
        with self.assertRaises(ValueError): apply_revisions(load_history(),revisions)

    def test_revision_cannot_claim_calibration(self):
        revisions=load_revisions(); revisions['labels']='human_calibrated'
        with self.assertRaises(ValueError): apply_revisions(load_history(),revisions)

    def test_unchanged_cases_preserved(self):
        history={c['id']:c for _,d in load_history() for c in d['cases']}
        current={c['id']:c for _,d in load_catalog() for c in d['cases']}
        revised={r['case_id'] for r in load_revisions()['revisions']}
        self.assertTrue(set(history) <= set(current))
        self.assertEqual(len(set(current) - set(history)), 3)
        for identifier in history.keys()-revised: self.assertEqual(history[identifier],current[identifier])

    def test_reader_pairs_are_separate_from_twenty_historical_inputs(self):
        self.assertEqual(len(validate_catalog(load_history())), 20)
        self.assertEqual(self.documents[-1][0], READER_CASES)
        self.assertEqual(len(self.documents[-1][1]['cases']), 3)
        self.assertTrue(all(c['critical_fact_failure'] is False for c in self.documents[-1][1]['cases']))

    def test_reader_pair_cannot_reuse_historical_identity(self):
        self.documents[-1][1]['cases'][0]['id'] = self.documents[0][1]['cases'][0]['id']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_reader_pairs_cannot_be_promoted_to_heldout_or_measured_quality(self):
        for key in ('held_out', 'automatic_quality_scoring'):
            documents = copy.deepcopy(self.documents)
            documents[-1][1][key] = True
            with self.assertRaises(ValueError): validate_catalog(documents)

    def test_reader_revision_parent_tamper_rejected_by_current_loader(self):
        history = load_reader_history()
        history[0][1]['cases'][1]['evidence'] += ' Changed source scope.'
        with mock.patch(__name__ + '.load_reader_history', return_value=history):
            with self.assertRaisesRegex(ValueError, 'Revision base changed'):
                load_catalog()

    def test_reader_revision_preserves_history_and_other_pairs(self):
        history = load_reader_history()
        before = copy.deepcopy(history)
        with mock.patch(__name__ + '.load_reader_history', return_value=history):
            current = load_catalog()[-1][1]['cases']
        self.assertEqual(history, before)
        self.assertEqual(len(current), len(before[0][1]['cases']))
        for original, revised in zip(before[0][1]['cases'], current):
            if original['id'] == 'editorial_voice_crowds_out_argument_zh':
                self.assertEqual(revised['revision_id'], original['id'] + '_r2')
                self.assertEqual(revised['critical_fact_failure'], original['critical_fact_failure'])
                self.assertNotEqual(revised['evidence'], original['evidence'])
            else:
                self.assertEqual(revised, original)

if __name__ == '__main__':
    if sys.argv[1:]==['--show-current']:
        print(json.dumps({'notice':'Current author-proposed development cases, not calibrated labels',
                          'cases':[c for _,d in load_catalog() for c in d['cases']]},ensure_ascii=False,indent=2))
        raise SystemExit(0)
    current = load_catalog()
    ids = validate_catalog(current)
    validate_defect_tags(current, *load_defect_tags())
    print(f'{len(ids)} development pairs parsed; semantic correctness and research quality NOT evaluated.')
    unittest.main()
