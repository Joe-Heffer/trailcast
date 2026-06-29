from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

import trailcast.server.dependencies as deps


def test_get_engine_initializes_when_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(deps, "_engine", None)
    with patch("trailcast.server.dependencies.ForecastEngine") as mock_cls:
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance
        result = next(deps.get_engine())
    assert result is mock_instance
    mock_cls.assert_called_once_with()


def test_get_engine_reuses_existing(monkeypatch: pytest.MonkeyPatch) -> None:
    existing = MagicMock()
    monkeypatch.setattr(deps, "_engine", existing)
    with patch("trailcast.server.dependencies.ForecastEngine") as mock_cls:
        result = next(deps.get_engine())
    assert result is existing
    mock_cls.assert_not_called()
