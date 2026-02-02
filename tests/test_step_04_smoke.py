"""Smoke tests for the step 04 Flask application."""

from __future__ import annotations


def test_index_get_ok(client_step_04):
    """The index route renders successfully."""
    resp = client_step_04.get("/")
    assert resp.status_code == 200


def test_data_get_ok(client_step_04):
    """The data page renders successfully."""
    resp = client_step_04.get("/data")
    assert resp.status_code == 200


def test_questions_get_ok(client_step_04):
    """The questions page renders successfully."""
    resp = client_step_04.get("/questions")
    assert resp.status_code == 200
