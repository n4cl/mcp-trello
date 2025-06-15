import pytest
import os
from trello import TrelloClient
from trello_client import get_trello_client, get_board_by_id, get_lists_from_board, get_list_by_name_or_id, create_list_on_board


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

        mock_board_obj = type("Board", (object,), {"id": "test_board_id", "name": "Test Board"})()

        class MockTrelloClient:
            def get_board(self, board_id):
                if board_id == "test_board_id":
                    return mock_board_obj
                raise Exception('board not found')

        monkeypatch.setattr("trello_client.get_trello_client", lambda: MockTrelloClient())

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

    def test_get_lists_from_board_success(self, monkeypatch):
        """
        指定されたボードからリストが正しく取得できることをテストします。
        """
        # モックのListインスタンスを作成
        mock_list_1 = type("List", (object,), {"id": "list1_id", "name": "To Do"})()
        mock_list_2 = type("List", (object,), {"id": "list2_id", "name": "Done"})()
        mock_lists = [mock_list_1, mock_list_2]

        # モックのBoardインスタンスとそのlist_listsメソッドを作成
        mock_board = type("Board", (object,), {"list_lists": lambda *args, **kwargs: mock_lists})()

        # get_lists_from_board関数を呼び出し
        lists = get_lists_from_board(mock_board)

        # 結果を検証
        assert len(lists) == 2
        assert lists[0].name == "To Do"
        assert lists[0].id == "list1_id"
        assert lists[1].name == "Done"
        assert lists[1].id == "list2_id"

    def test_get_lists_from_board_no_board(self):
        """
        ボードオブジェクトが指定されていない場合にValueErrorが発生することをテストします。
        """
        with pytest.raises(ValueError, match="ボードオブジェクトが指定されていません。"):
            get_lists_from_board(None)


class TestGetListByNameOrId:
    def test_get_list_by_id_success(self, monkeypatch):
        """
        IDでリストが正しく取得できることをテストします。
        """
        mock_list = type("List", (object,), {"id": "test_list_id", "name": "Test List"})()
        class MockBoardGetList:
            def get_list(self, list_id):
                if list_id == "test_list_id":
                    return mock_list
                raise Exception('list not found')
        mock_board = MockBoardGetList()

        list_obj = get_list_by_name_or_id(mock_board, "test_list_id")
        assert list_obj.id == "test_list_id"
        assert list_obj.name == "Test List"

    def test_get_list_by_name_success(self, monkeypatch):
        """
        名前でリストが正しく取得できることをテストします。
        """
        mock_list_1 = type("List", (object,), {"id": "list1_id", "name": "List One"})()
        mock_list_2 = type("List", (object,), {"id": "list2_id", "name": "Test List Name"})()
        mock_lists = [mock_list_1, mock_list_2]

        class MockBoardListLists:
            def get_list(self, list_id):
                raise Exception('list not found')
            def list_lists(self, *args, **kwargs):
                return mock_lists
        mock_board = MockBoardListLists()

        list_obj = get_list_by_name_or_id(mock_board, "Test List Name")
        assert list_obj.id == "list2_id"
        assert list_obj.name == "Test List Name"

    def test_get_list_by_name_or_id_not_found(self, monkeypatch):
        """
        指定されたIDまたは名前のリストが見つからない場合にValueErrorが発生することをテストします。
        """
        mock_list_1 = type("List", (object,), {"id": "list1_id", "name": "List One"})()
        mock_lists = [mock_list_1]

        class MockBoardNotFound:
            def get_list(self, list_id):
                raise Exception('list not found')
            def list_lists(self, *args, **kwargs):
                return mock_lists
        mock_board = MockBoardNotFound()

        with pytest.raises(ValueError, match="指定されたIDまたは名前 'NonExistent' のリストはボードに存在しません。"):
            get_list_by_name_or_id(mock_board, "NonExistent")

    def test_get_list_by_name_or_id_no_board(self):
        """
        ボードオブジェクトが指定されていない場合にValueErrorが発生することをテストします。
        """
        with pytest.raises(ValueError, match="ボードオブジェクトが指定されていません。"):
            get_list_by_name_or_id(None, "some_id_or_name")

    def test_get_list_by_name_or_id_no_identifier(self, monkeypatch):
        """
        リストのIDまたは名前が指定されていない場合にValueErrorが発生することをテストします。
        """
        mock_board = type("Board", (object,), {})()
        with pytest.raises(ValueError, match="リストのIDまたは名前が指定されていません。"):
            get_list_by_name_or_id(mock_board, None)


class TestCreateListOnBoard:
    def test_create_list_on_board_success(self, monkeypatch):
        """
        Trelloボードに新しいリストが正常に作成されることをテストします。
        """
        mock_new_list = type("List", (object,), {"id": "new_list_id", "name": "New Test List"})()

        class MockBoardAddList:
            def add_list(self, list_name):
                if list_name == "New Test List":
                    return mock_new_list
                return None
        mock_board = MockBoardAddList()

        new_list = create_list_on_board(mock_board, "New Test List")
        assert new_list.id == "new_list_id"
        assert new_list.name == "New Test List"

    def test_create_list_on_board_no_board(self):
        """
        ボードオブジェクトが指定されていない場合にValueErrorが発生することをテストします。
        """
        with pytest.raises(ValueError, match="ボードオブジェクトが指定されていません。"):
            create_list_on_board(None, "New List")

    def test_create_list_on_board_no_list_name(self, monkeypatch):
        """
        リスト名が指定されていない場合にValueErrorが発生することをテストします。
        """
        mock_board = type("Board", (object,), {})()
        with pytest.raises(ValueError, match="リスト名が指定されていません。"):
            create_list_on_board(mock_board, None)
