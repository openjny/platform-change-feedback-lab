import json
import unittest
from unittest.mock import patch

from scripts.feedback import candidate, event_pr, evidence_url, model_proposal, publish, render

REPO = "example/platform-change-feedback-lab"
PR = f"https://github.com/{REPO}/pull/3"
DATA = {
    "category": "lint-ci",
    "title": "Validate every profile in CI",
    "finding": "A new checked-in profile was not covered by the smoke check.",
    "suggestion": "Run the validator on every checked-in profile.",
}


class FeedbackTests(unittest.TestCase):
    def test_model_can_abstain(self):
        self.assertIsNone(model_proposal({"candidate": None}, [{"url": PR}]))

    def test_model_must_cite_collected_evidence(self):
        evidence = [{"url": PR + "#discussion_r9"}]
        proposal = model_proposal({"candidate": {**DATA, "evidence": 1}}, evidence)
        self.assertEqual(proposal, {"candidate": DATA, "evidence": evidence[0]["url"]})
        with self.assertRaisesRegex(ValueError, "outside"):
            model_proposal({"candidate": {**DATA, "evidence": 2}}, evidence)

    def test_reject_content_that_would_ping_or_link(self):
        with self.assertRaises(ValueError):
            candidate({**DATA, "finding": "@somebody please check"})
        with self.assertRaises(ValueError):
            evidence_url("https://github.com/elsewhere/project/pull/3", REPO, 3)

    def test_reject_fork_or_unmerged_pr(self):
        pr = {"merged": True, "base": {"ref": "main"}, "head": {"repo": {"full_name": REPO}}}
        event = {"action": "closed", "pull_request": pr, "sender": {"login": "example"}}
        self.assertEqual(event_pr(event, REPO), pr)
        pr["head"]["repo"]["full_name"] = "fork/project"
        with self.assertRaises(ValueError):
            event_pr(event, REPO)
        pr["head"]["repo"]["full_name"] = REPO
        pr["merged"] = False
        with self.assertRaises(ValueError):
            event_pr(event, REPO)

    @patch("scripts.feedback.gh")
    def test_repeated_publication_reuses_existing_closed_issue(self, gh):
        title, body = render(DATA, PR, "pr:3", PR + "#discussion_r9")
        url = f"https://github.com/{REPO}/issues/5"
        gh.side_effect = ["[[]]", url, json.dumps([[{"body": body, "html_url": url, "state": "closed"}]])]
        publish(REPO, title, body)
        publish(REPO, title, body)
        creates = [call for call in gh.call_args_list if call.args[:2] == ("issue", "create")]
        self.assertEqual(len(creates), 1)
        self.assertIn("improvement-candidate", creates[0].args)
        self.assertIn(PR + "#discussion_r9", creates[0].kwargs["body"])
