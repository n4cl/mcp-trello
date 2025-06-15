import os
from trello import TrelloClient

def get_trello_client():
    """
    環境変数からTrello APIキーとトークンを読み込み、TrelloClientインスタンスを返します。
    """
    api_key = os.environ.get("TRELLO_API_KEY")
    api_secret = os.environ.get("TRELLO_API_SECRET")
    token = os.environ.get("TRELLO_TOKEN")

    if not api_key:
        raise ValueError("環境変数 'TRELLO_API_KEY' が設定されていません。")
    if not api_secret:
        raise ValueError("環境変数 'TRELLO_API_SECRET' が設定されていません。")
    if not token:
        raise ValueError("環境変数 'TRELLO_TOKEN' が設定されていません。")

    client = TrelloClient(
        api_key=api_key,
        api_secret=api_secret,
        token=token
    )
    return client

def get_board_by_id():
    """
    環境変数 TRELLO_BOARD_ID で指定されたIDを持つTrelloボードを取得します。
    """
    board_id = os.environ.get("TRELLO_BOARD_ID")
    if not board_id:
        raise ValueError("環境変数 'TRELLO_BOARD_ID' が設定されていません。")

    client = get_trello_client()
    board = client.get_board(board_id)
    return board

def get_lists_from_board(board):
    """
    指定されたTrelloボード内のすべてのリストを取得します。
    """
    if not board:
        raise ValueError("ボードオブジェクトが指定されていません。")
    lists = board.list_lists()
    return lists

def get_list_by_name_or_id(board, list_identifier):
    """
    指定されたTrelloボードから、IDまたは名前で特定のリストを取得します。
    """
    if not board:
        raise ValueError("ボードオブジェクトが指定されていません。")
    if not list_identifier:
        raise ValueError("リストのIDまたは名前が指定されていません。")

    # まずはIDで取得を試みる
    try:
        list_obj = board.get_list(list_identifier)
        return list_obj
    except Exception:
        pass # IDでの取得に失敗した場合は、名前で検索を試みる

    # 名前で検索
    for list_obj in board.list_lists():
        if list_obj.name == list_identifier:
            return list_obj

    raise ValueError(f"指定されたIDまたは名前 '{list_identifier}' のリストはボードに存在しません。")

def create_list_on_board(board, list_name):
    """
    指定されたTrelloボードに新しいリストを作成します。
    """
    if not board:
        raise ValueError("ボードオブジェクトが指定されていません。")
    if not list_name:
        raise ValueError("リスト名が指定されていません。")

    new_list = board.add_list(list_name)
    return new_list

if __name__ == "__main__":
    # このスクリプトを直接実行した場合のテストコード
    # 実際のAPIキーとトークンを設定してください（例: export TRELLO_API_KEY='your_key'）
    try:
        client = get_trello_client()
        print("TrelloClientの初期化に成功しました。")

        # 特定のボードをIDで取得する例
        board = get_board_by_id()
        print(f"取得したボード名: {board.name}, ID: {board.id}")

    except ValueError as e:
        print(f"エラー: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
