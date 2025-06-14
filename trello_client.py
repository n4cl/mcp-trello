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

if __name__ == "__main__":
    # このスクリプトを直接実行した場合のテストコード
    # 実際のAPIキーとトークンを設定してください（例: export TRELLO_API_KEY='your_key'）
    try:
        client = get_trello_client()
        print("TrelloClientの初期化に成功しました。")

        # すべてのボードを取得する例 (コメントアウト)
        # boards = get_boards()
        # for board in boards:
        #     print(f"- {board.name} ({board.id})")

        # 特定のボードをIDで取得する例
        board = get_board_by_id()
        print(f"取得したボード名: {board.name}, ID: {board.id}")

    except ValueError as e:
        print(f"エラー: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
