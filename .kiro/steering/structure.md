# ストラクチャ・ステアリング

- レイアウトパターン: リポジトリ直下にフラット配置。`main.py` がMCPエントリポイント、`trello_client.py` がTrelloラッパー、`test_trello_client.py` がヘルパー関数を鏡写しにテスト。実行手順はルートのDocker Compose設定とREADMEに集約。
- フロー: `main.py` が `.env` を読み込み、識別子をマスクしてログ出力後にFastMCPを起動。Trelloヘルパーは純粋関数としてdotenvに依存せず、呼び出し元が環境変数を用意する前提。ツールはまず `get_board_by_id` でボードを確定し、その上でリスト操作を行う構成を基本とする。
- 命名規則: 関数は動詞先行（`get_*`, `create_*`）。必須入力欠如は日本語メッセージ付き `ValueError` で統一。テストは関数単位でクラスを分けて整理。
- 設定パターン: `docker-compose.yml` が最小サービス（ポート8000, env_file）を定義し、`docker-compose.override.yml` が開発用のボリュームマウントと常駐コマンドを上乗せする二層構成。
- 拡張指針: 新しいMCPツールはpy-trello呼び出しを小さな関数で包み、環境変数検証の流儀を再利用。モジュールは肥大化させず短く保ち、新挙動にはpytest + monkeypatchのモックを揃えて対にする。
