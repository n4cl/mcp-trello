# mcp-trello

## Docker Composeの利用

このプロジェクトでは、Dockerコンテナの起動と管理のために `docker-compose.yml` と `docker-compose.override.yml` を使用します。それぞれのファイルは以下の役割を持ちます。

- `docker-compose.yml`: 運用環境でのアプリケーションの起動設定を定義します。これはアプリケーションのコアサービスと依存関係を含み、`tail -f /dev/null` などの開発用コマンドは含みません。
- `docker-compose.override.yml`: 開発環境での追加設定を定義します。これには、ソースコードのボリュームマウントや、コンテナを継続的に稼働させるためのコマンド（例: `tail -f /dev/null`）などが含まれます。開発時に `docker compose up` を実行すると、このファイルが `docker-compose.yml` に自動的に適用されます。

## 開発環境セットアップ

このプロジェクトを開発環境でセットアップする手順は以下の通りです。

### 1. Dockerコンテナの起動 (開発モード)
開発モードでは、`docker-compose.override.yml` が自動的に読み込まれ、ホストのコード変更がコンテナに即座に反映されます。また、コンテナは継続的に稼働し続けます。

以下のコマンドを実行して、Dockerコンテナをビルドして起動してください。

```bash
docker compose up --build -d
```

## 運用環境での起動

運用環境では、`docker-compose.override.yml` を使用せず、`docker-compose.yml` のみを使用してFastMCPサーバーを起動します。このモードでは、アプリケーションのログが直接ターミナルに表示されます。

```bash
docker compose -f docker-compose.yml up --build
```
