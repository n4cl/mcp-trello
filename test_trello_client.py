import pytest
import os
from trello import TrelloClient
from trello_client import get_trello_client, get_board_by_id


class TestGetTrelloClient:
    def test_get_trello_client_success(self, monkeypatch):
        """
        環境変数が正しく設定されている場合にTrelloClientが正常に初期化されることをテストします。
        """
        monkeypatch.setenv("TRELLO_API_KEY", "test_key")
        monkeypatch.setenv("TRELLO_API_SECRET", "test_secret")
        monkeypatch.setenv("TRELLO_TOKEN", "test_token")

        client = get_trello_client()
        assert isinstance(client, TrelloClient)
        assert client.api_key == "test_key"

    def test_get_trello_client_no_api_key(self, monkeypatch):
        """
        TRELLO_API_KEYが設定されていない場合にValueErrorが発生することをテストします。
        """
        monkeypatch.delenv("TRELLO_API_KEY", raising=False)
        monkeypatch.setenv("TRELLO_API_SECRET", "test_secret")
        monkeypatch.setenv("TRELLO_TOKEN", "test_token")

        with pytest.raises(ValueError, match="環境変数 'TRELLO_API_KEY' が設定されていません。"):
            get_trello_client()

    def test_get_trello_client_no_api_secret(self, monkeypatch):
        """
        TRELLO_API_SECRETが設定されていない場合にValueErrorが発生することをテストします。
        """
        monkeypatch.setenv("TRELLO_API_KEY", "test_key")
        monkeypatch.delenv("TRELLO_API_SECRET", raising=False)
        monkeypatch.setenv("TRELLO_TOKEN", "test_token")

        with pytest.raises(ValueError, match="環境変数 'TRELLO_API_SECRET' が設定されていません。"):
            get_trello_client()

    def test_get_trello_client_no_token(self, monkeypatch):
        """
        TRELLO_TOKENが設定されていない場合にValueErrorが発生することをテストします。
        """
        monkeypatch.setenv("TRELLO_API_KEY", "test_key")
        monkeypatch.setenv("TRELLO_API_SECRET", "test_secret")
        monkeypatch.delenv("TRELLO_TOKEN", raising=False)

        with pytest.raises(ValueError, match="環境変数 'TRELLO_TOKEN' が設定されていません。"):
            get_trello_client()


class TestGetBoardById:
    def test_get_board_by_id_success(self, monkeypatch):
        """
        環境変数 TRELLO_BOARD_ID が正しく設定されている場合に特定のボードが取得できることをテストします。
        """
        monkeypatch.setenv("TRELLO_BOARD_ID", "test_board_id")
        monkeypatch.setenv("TRELLO_API_KEY", "test_key")
        monkeypatch.setenv("TRELLO_API_SECRET", "test_secret")
        monkeypatch.setenv("TRELLO_TOKEN", "test_token")

        mock_board = type("Board", (object,), {"id": "test_board_id", "name": "Test Board"})()
        mock_client = type("TrelloClient", (object,), {"get_board": lambda *args, **kwargs: mock_board})()
        monkeypatch.setattr("trello_client.get_trello_client", lambda: mock_client)

        board = get_board_by_id()
        assert board.id == "test_board_id"
        assert board.name == "Test Board"

    def test_get_board_by_id_no_env_var(self, monkeypatch):
        """
        TRELLO_BOARD_ID が設定されていない場合にValueErrorが発生することをテストします。
        """
        monkeypatch.delenv("TRELLO_BOARD_ID", raising=False)

        with pytest.raises(ValueError, match="環境変数 'TRELLO_BOARD_ID' が設定されていません。"):
            get_board_by_id()
