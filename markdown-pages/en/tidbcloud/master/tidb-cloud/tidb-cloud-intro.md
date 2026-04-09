---
title: What is TiDB Cloud
summary: TiDB Cloudとそのアーキテクチャについて学びましょう。
category: intro
---

# TiDB Cloudとは何ですか？ {#what-is-tidb-cloud}

[TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 、オープンソースのハイブリッドトランザクションおよび分析処理（HTAP）データベースである[TiDB](https://docs.pingcap.com/tidb/stable/overview)をベースとした、フルマネージドのクラウドネイティブなデータベース・アズ・ア・サービス（DBaaS）です。TiDB TiDB Cloudは、データベース<CustomContent language="en,zh">デプロイと管理を容易にし、データベースの複雑さではなくアプリケーションの開発に集中できるようにします。4 TiDB Cloudクラスタを作成することで、Amazon Web Services（AWS）、Google Cloud、Microsoft Azure、およびAlibaba Cloud上にミッションクリティカルなアプリケーションを迅速に構築できます。6 </CustomContent> TiDB Cloudクラスタを作成することで、Amazon Web Services（AWS）、Google Cloud、およびMicrosoft Azure上にミッションクリティカルなアプリケーションを迅速に<CustomContent language="ja">できます</CustomContent>

![TiDB Cloud Overview](/media/tidb-cloud/tidb-cloud-overview.png)

## TiDB Cloudを選ぶ理由 {#why-tidb-cloud}

TiDB Cloudを使用すれば、ほとんど、あるいは全くトレーニングを受けなくても、インフラストラクチャ管理やクラスタ展開といった複雑なタスクを容易に処理できます。

-   開発者やデータベース管理者（DBA）は、大量のオンライントラフィックを容易に処理し、複数のデータセットにわたる大量のデータを迅速に分析することができます。

-   あらゆる規模の企業が、前払いなしでTiDB Cloudを簡単に導入・管理し、ビジネスの成長に合わせて柔軟に対応できます。

TiDB Cloudの詳細については、以下のビデオをご覧ください。

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="Why TiDB Cloud?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

TiDB Cloudでは、以下の主要機能をご利用いただけます。

-   **高速かつカスタマイズ可能なスケーリング**

    重要なワークロード向けに、 ACIDトランザクションを維持しながら、数百ノードまで柔軟かつ透過的に拡張できます。シャーディングについて悩む必要はありません。また、ビジネスニーズに応じて、コンピューティングノードとstorageノードを個別に拡張することも可能です。

-   **MySQLとの互換性**

    TiDBのMySQL互換性により、アプリケーションの生産性を向上させ、市場投入までの時間を短縮できます。既存のMySQLインスタンスからデータを簡単に移行でき、コードの書き換えは不要です。

-   **高可用性と高信頼性**

    設計段階から高い可用性を実現。複数の可用性ゾーンにわたるデータレプリケーション、日々のバックアップ、自動フェイルオーバーにより、ハードウェア障害、ネットワーク分断、データセンターの障害発生時でも、事業継続性を確保します。

-   **リアルタイム分析**

    内蔵の分析エンジンにより、リアルタイムの分析クエリ結果を取得できます。TiDB TiDB Cloudは、ミッションクリティカルなアプリケーションに影響を与えることなく、最新データに対して一貫した分析クエリを実行します。

-   **エンタープライズグレードのSecurity**

    専用ネットワークと専用マシンでデータをセキュリティ。転送中および保存時の暗号化にも対応しています。TiDB TiDB Cloudは、SOC 2 Type 2、ISO 27001:2013、ISO 27701の認証を取得しており、GDPRにも完全に準拠しています。

-   **フルマネージドサービス**

    使いやすいWebベースの管理プラットフォームを通じて、数回のクリックでTiDBクラスタのデプロイ、スケーリング、監視、管理を行うことができます。

-   **マルチクラウド対応**

<CustomContent language="en,zh">

    クラウドベンダーに縛られることなく、柔軟性を維持できます。TiDB TiDB Cloudは現在、AWS、Azure、Google Cloud、およびAlibaba Cloudで利用可能です。

</CustomContent>

    <CustomContent language="ja">

    クラウドベンダーに縛られることなく、柔軟性を維持できます。TiDB TiDB Cloudは現在、AWS、Azure、Google Cloudで利用可能です。

    </CustomContent>

-   **シンプルな料金プラン**

    使った分だけ支払う、透明性の高い明瞭な料金体系で、隠れた料金は一切ありません。

-   **世界クラスのサポート**

    サポートポータル、<a href="mailto:tidbcloud-support@pingcap.com">メール</a>、チャット、ビデオ会議を通じて、世界最高水準のサポートをご利用いただけます。

## 展開オプション {#deployment-options}

TiDB Cloudは、以下の導入オプションを提供します。

-   TiDB Cloud Starter

    {{{ .starter }}}は、フルマネージド型のマルチテナントTiDBサービスです。MySQL互換の自動スケーリング対応データベースを即座に提供し、十分な無料クォータと、無料制限を超えた場合の従量課金制を採用しています。

    <CustomContent language="en,zh">

    現在、{{{ .starter }}} は AWS で一般提供されており、Alibaba Cloud ではパブリックプレビューとして提供されています。

    </CustomContent>

-   {{{ 。不可欠 }}}

    ワークロードが増加し、リアルタイムでのスケーラビリティが必要なアプリケーションに対して、{{{ .essential }}} は、ビジネスの成長に追随できる柔軟性とパフォーマンスを提供します。

    <CustomContent language="en,zh">

    現在、{{{ .essential }}} は AWS および Alibaba Cloud でパブリックプレビュー中です。

    Alibaba Cloud 上の {{{ .starter }}} と {{{ .essential }}} の機能の比較については、 [Alibaba Cloud 上の TiDB](https://www.pingcap.com/partners/alibaba-cloud/)参照してください。

    </CustomContent>

    <CustomContent language="ja">

    現在、{{{ .essential }}} は AWS でパブリックプレビュー中です。

    </CustomContent>

<CustomContent plan="premium">

-   {{{ .premium }}}

    {{{ .premium }}} は、無制限のリアルタイム拡張性を必要とするミッションクリティカルなビジネス向けに設計されています。ワークロードを考慮した自動スケーリングと包括的なエンタープライズ機能を提供します。

    現在、{{{ .premium }}} は AWS および Alibaba Cloud でプライベートプレビュー中です。

</CustomContent>

-   TiDB Cloud Dedicated

    TiDB Cloud Dedicatedは、ミッションクリティカルなビジネス向けに設計されており、複数のアベイラビリティゾーンにわたる高可用性、水平スケーリング、および完全な[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)機能を提供します。

    現在、 TiDB Cloud DedicatedはAWSとGoogle Cloudで一般提供されており、Azureではパブリックプレビュー版が提供されています。詳細については、 [TiDB Cloud Dedicated](https://www.pingcap.com/tidb-cloud-dedicated)ドキュメントを参照してください。

## アーキテクチャ {#architecture}

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

-   TiDB VPC（仮想プライベートクラウド）

    各TiDB Cloudクラスタにおいて、 TiDB Operatorノードやログ記録ノードを含むすべてのTiDBノードおよび補助ノードは、同一のVPC内にデプロイされます。

-   TiDB Cloudセントラルサービス

    課金、アラート、メタstorage、ダッシュボードUIなどの中央サービスは、それぞれ独立してデプロイされます。ダッシュボードUIにはインターネット経由でアクセスでき、TiDBクラスタを操作できます。

-   あなたのVPC

    プライベート エンドポイント接続または VPC ピアリング接続を介して TiDB クラスターに接続できます。詳細については[プライベートエンドポイント接続を設定する](/tidb-cloud/set-up-private-endpoint-connections.md)または[VPCピアリング接続の設定](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。
