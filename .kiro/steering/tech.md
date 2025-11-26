# テック・ステアリング

- スタック: Python + FastMCP (2.7.1)、py-trello (0.20.1)、python-dotenv (1.1.0)、pytest (8.4.0)。`requirements.txt`でバージョン固定。
- 実行時設定パターン: `.env`は`main.py`で読み込み、以降のTrelloヘルパーは `TRELLO_API_KEY`, `TRELLO_API_SECRET`, `TRELLO_TOKEN`, `TRELLO_BOARD_ID` の存在を前提にする。欠如時は黙ってデフォルトせず `ValueError` で即座に失敗。
- MCP統合: `FastMCP("Trello MCP Server")` で `@mcp.tool` を定義。ツール本体はTrelloヘルパーの薄いラッパーに留め、MCPクライアントが扱いやすいシンプルな文字列/オブジェクトを返す。
- デプロイ: ベースの `docker-compose.yml` がビルドと環境変数ロードを担い、`docker-compose.override.yml` はリポジトリを `/app` にマウントし `tail -f /dev/null` で開発用に常駐させる。
- 可観測性と安全性: ロギングは `basicConfig(level=INFO)`。シークレットは先頭・末尾4文字のみ表示し、トークンの永続化を避けて環境変数注入を優先。
- テストパターン: pytest + `monkeypatch` で環境変数セットとTrelloクライアントのスタブを作成し、小さなモックで実APIに触れず振る舞いを検証。
