# なんなん
misskeyのストリーミングAPIを使ってアンテナに届いたノートをDiscordへ通知を送るやつ

## つかいかた
 1. config.jsonを用意する
```json
{
  "discord_webhook": "https://discord.com/api/webhooks/...",
  "host": "mi.tomadoi.com",
  "token": "Misskeyトークン",
  "antenna_id": "アンテナID",
  "allow_filter": ["通知したいキーワード"],
  "deny_filter": ["通知したくないキーワード"],
  "filter_default_mode": "deny",
  "loglevel": "INFO"
}
```
 2. dockerなどで動かす
 3. できた！

## フィルター機能
 - `allow_filter` キーワードにマッチした場合、通過します
 - `deny_filter` キーワードにマッチした場合、拒否します
 - 両フィルターに当てはまらない場合は`filter_default_mode`によって判断されます

## 免責
 - 使用にあたって発生したいかなる損害（直接的・間接的を問わず）、データの損失、システムの障害、またはその他の不利益について一切の責任を負いません
 - ご利用はすべて自己責任でお願いいたします
