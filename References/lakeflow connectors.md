# Ingesting Enterprise Data with Lakeflow Connect - Summary

## 1. 개요 (Overview)
지금까지는 클라우드 스토리지에서 Databricks로 데이터를 적재하는 방법(CREATE TABLE, COPY INTO, Auto Loader)을 다뤘다. 이번 강의에서는 데이터베이스나 엔터프라이즈 애플리케이션처럼 다른 유형의 소스에서 데이터를 적재하는 방법을 소개한다.

## 2. Lakeflow Connect Managed Connectors
Databricks에 내장된 커넥터로, 다양한 엔터프라이즈 데이터베이스와 애플리케이션에서의 데이터 적재를 단순화한다.

- UI(포인트 앤 클릭) 또는 API로 손쉽게 설정 가능
- Databricks가 완전히 관리하여 수동 설정/커스텀 코드 불필요
- 지원 소스 예시: Workday, Salesforce, PostgreSQL, SQL Server, Dynamics 365, Google Analytics, Oracle NetSuite, ServiceNow, SharePoint 등
- 커넥터는 Public Preview, GA 등 다양한 릴리스 상태이므로 최신 문서 확인 필요 (docs.databricks.com/aws/en/release-notes/release-types)

## 3. SaaS 소스 적재 아키텍처
Managed Ingestion 파이프라인(Serverless Declarative Pipelines)을 통해 외부 SaaS(예: Salesforce, Workday)에서 Streaming Delta Table로 데이터를 적재한다.

동작 방식:
1. Serverless Declarative Pipelines 작업이 Unity Catalog에서 자격 증명(credentials)을 가져온다.
2. 공개적으로 접근 가능한 데이터 소스(API, OLAP 포트 등)에 접속한다.
3. 데이터를 변환하여 Streaming Delta Table에 저장한다.

이 파이프라인은 공개 SaaS 소스 전용으로 미리 정의되어 있으며, 데이터 이동은 모두 데이터 플레인에서 이뤄지고 컨트롤 플레인은 설정/모니터링/관리 용도로만 사용된다.
(참고 문서: docs.databricks.com/aws/en/ingestion/lakeflow-connect/#saas-connector-components)

## 4. 데이터베이스 소스 적재 아키텍처
SaaS와 달리 데이터베이스는 보통 방화벽 뒤에 있어 직접 접근이 어렵기 때문에 두 가지 컴포넌트가 추가된다.

흐름: Users → WebUI/API/CLI → **Ingestion Gateway**(Classic Compute Declarative Pipeline) → **Staging & State Management**(Unity Catalog Volume) → **Managed Ingestion**(Serverless Declarative Pipeline) → Streaming Delta Tables

- **Ingestion Gateway**: 데이터베이스에 연결해 메타데이터, 스냅샷, 변경 로그(change log)를 추출하고 Unity Catalog Volume에 스테이징한다.
- **Unity Catalog Volume**: 중간 스테이징 계층 역할을 하며, 다음 파이프라인이 데이터를 읽어 스트리밍할 수 있게 한다. 기본적으로 파이프라인 실행 사용자에게만 접근이 제한된다.

Gateway를 별도로 둔 이유:
- 네트워킹: 방화벽 뒤에 있는 DB에 Private Link 등이 없을 경우, 게이트웨이를 고객 네트워크 내부에 배포할 수 있다.
- 부하 제한: 게이트웨이 하나가 DB와 통신하고 여러 파이프라인으로 분산(fan-out)시켜 확장성을 확보한다. (SaaS는 API 호출 제한으로 부하가 이미 통제되므로 이 문제가 상대적으로 적음)

(참고 문서: docs.databricks.com/aws/en/ingestion/lakeflow-connect/#database-connector-components)

## 5. Partner Connect
Managed Connector가 지원하지 않는 소스는 **Partner Connect**를 활용할 수 있다. Databricks 기술 파트너와 체험 계정을 만들어 Databricks UI에서 파트너 솔루션에 연결, 자사 데이터로 시험해본 뒤 적합한 솔루션을 도입할 수 있다.

지원 소스 예: On-prem databases, Cloud databases, File sources, Enterprise applications
파트너 예시: Informatica, Qlik, Rivery, Alteryx, Prophecy, Fivetran

파트너 커넥터는 전담 엔지니어링 팀이 유지보수하는 폭넓고 깊이 있는 기능을 제공하기 때문에 Databricks는 네이티브 커넥터가 있어도 고객 선택권을 위해 파트너 생태계를 계속 지원한다는 점을 강조한다.

(참고 문서: "What is Databricks Partner Connect" 및 Partner Connect 공식 문서)

## 6. 마무리
이 레슨을 통해 Databricks의 엔터프라이즈 데이터 적재 방법(Managed Connectors - SaaS/DB, Partner Connect)에 대한 개요를 학습했다.
