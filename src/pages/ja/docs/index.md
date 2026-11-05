---
layout: "../../../layouts/DocumentLayout.astro"
title: "ドキュメント"
description: "Project-KISSの理念、検証記録の原則、プロダクト構想、サイトの開発手順を案内します。"
locale: "ja"
eyebrow: "DOCUMENTATION / ドキュメント"
lead: "理念から読み始め、検証結果には条件と限界を添えます。"
---

## はじめに

- [理念](/ja/philosophy/)：KISS、観測、検証、ガバナンス。
- [Project-AceIS](/ja/products/aceis/)：プロダクトの構想と開発目標。
- [ロードマップ](/ja/roadmap/)：このサイトの対象とドキュメント整備案。
- [参加する](/ja/contributing/)：変更提案と不具合報告。

## 検証報告に残すこと

確認する問い、対象のバージョンと環境、手順、観測結果、限界を明記します。測定した動作と、提案や仮定を読み手が区別できる記録にします。

フィクスチャ、モック、実環境の統合検証のどれを使ったかを示します。未実施を成功・失敗に混ぜません。共有前に、秘密情報や無関係な個人情報を除きます。

## このサイトを開発する

以下は**サイトのリポジトリ**を開発するための手順です。Project-AceISのインストールや起動手順ではありません。

必要な環境はGit、Node.js 24（固定したAstroは22.23.4以上が必要）、npm、Python 3です。Astroで静的サイトを生成し、文章ページはMarkdownで管理します。

```sh
git clone https://github.com/i-pp/project-kiss-website.git
cd project-kiss-website
npm ci
npm run dev
```

開発サーバーはローカルアドレスを表示し、`127.0.0.1`で待ち受けます。同じチェックアウトで検査と静的プレビューを実行できます。

```sh
npm run verify
npm run preview
```

`verify`はAstroの型検査、静的ビルド、検査ツールのテスト、ローカルリンク・フラグメント・メタデータ・言語対・ロゴのハッシュ検査を行います。プレビューはビルド済み出力をローカルで表示します。

構成と公開手順は[リポジトリのREADME](https://github.com/i-pp/project-kiss-website#readme)をご覧ください。プロダクト実装の文書は、レビュー済みの資料が整った段階で追加します。
