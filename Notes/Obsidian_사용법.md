# Obsidian 사용법 가이드

**작성일:** 2026-09-30

## 목차
1. [시작하기](#시작하기)
2. [기본 마크다운 문법](#기본-마크다운-문법)
3. [노트 연결하기](#노트-연결하기)
4. [검색 기능](#검색-기능)
5. [그래프 뷰](#그래프-뷰)
6. [태그 활용](#태그-활용)
7. [이 프로젝트 활용법](#이-프로젝트-활용법)

---

## 시작하기

### Obsidian이란?
- 마크다운 기반의 지식 관리 시스템
- 로컬 파일 저장으로 데이터 소유권 보장
- 노트 간 연결을 통한 지식 네트워크 구축

### 볼트(Vault) 열기
1. Obsidian 실행
2. "Open folder as vault" 선택
3. 이 프로젝트의 루트 디렉토리 선택
   ```
   /Users/dkim/WorkSpace/Databricks-Certified-Data-Engineer-Associate-Questions
   ```

---

## 기본 마크다운 문법

### 제목 (Headers)
```markdown
# 제목 1
## 제목 2
### 제목 3
#### 제목 4
```

### 텍스트 강조
```markdown
**굵게** 또는 __굵게__
*기울임* 또는 _기울임_
~~취소선~~
==하이라이트==
```

### 리스트
```markdown
- 순서 없는 리스트
- 항목 2
  - 하위 항목

1. 순서 있는 리스트
2. 항목 2
   1. 하위 항목
```

### 코드 블록
````markdown
인라인 코드: `spark.read.table()`

코드 블록:
```python
df = spark.read.table("catalog.schema.table")
df.show()
```
````

### 인용구
```markdown
> 이것은 인용구입니다
> 여러 줄도 가능합니다
```

### 테이블
```markdown
| 열1 | 열2 | 열3 |
|-----|-----|-----|
| 값1 | 값2 | 값3 |
| 값4 | 값5 | 값6 |
```

---

## 노트 연결하기

### 기본 링크 문법
```markdown
[[파일명]]                    # 기본 링크
[[파일명|표시될 텍스트]]      # 별칭 사용
[[폴더/파일명]]               # 폴더 경로 포함
```

### 예시
```markdown
[[index]]                                    # 인덱스 페이지로 이동
[[topics/delta-lake]]                        # Delta Lake 토픽으로 이동
[[Databricks_Data_Engineering_Concepts]]     # 컨셉 문서로 이동
[[topics/delta-lake|Delta Lake 개념]]        # "Delta Lake 개념"으로 표시
```

### 헤딩 링크
```markdown
[[파일명#헤딩]]                              # 특정 섹션으로 이동
[[CDC_SCD_REVIEW#SCD Type 1]]                # CDC 문서의 SCD Type 1 섹션으로
```

### 블록 링크
```markdown
[[파일명#^블록ID]]                           # 특정 블록으로 이동
```

---

## 검색 기능

### 기본 검색
- **단축키:** `Cmd/Ctrl + Shift + F`
- 모든 노트에서 텍스트 검색

### 검색 연산자
```
file:delta-lake              # 파일명으로 검색
path:topics/                 # 경로로 검색
tag:#exam                    # 태그로 검색
"exact phrase"               # 정확한 구문 검색
COPY AND INTO                # AND 연산
COPY OR INTO                 # OR 연산
-COPY                        # NOT 연산 (제외)
```

### 실전 예시
```
file:delta tag:#important                    # delta 파일 중 important 태그
path:topics/ "Unity Catalog"                 # topics 폴더의 Unity Catalog 관련
SCD AND (Type1 OR Type2)                     # SCD Type1 또는 Type2 관련
```

---

## 그래프 뷰

### 그래프 뷰란?
- 노트 간 연결 관계를 시각화
- 지식 구조를 한눈에 파악

### 그래프 뷰 열기
- **단축키:** `Cmd/Ctrl + G`
- 사이드바 아이콘 클릭

### 로컬 그래프
- 현재 노트와 연결된 노트만 표시
- 우클릭 > "Open local graph" 또는 `Cmd/Ctrl + Shift + G`

### 활용 팁
- 필터를 사용해 특정 태그나 경로만 표시
- 노드를 클릭하면 해당 노트로 이동
- 연결이 많은 노트는 중요한 허브 역할

---

## 태그 활용

### 태그 문법
```markdown
#태그명
#중첩/태그/가능

#exam
#important
#review
#databricks/delta-lake
#databricks/unity-catalog
```

### 이 프로젝트 권장 태그
```markdown
#exam                        # 시험 관련
#important                   # 중요 개념
#review                      # 복습 필요
#sql                         # SQL 관련
#python                      # Python 관련
#streaming                   # 스트리밍 관련
#batch                       # 배치 처리 관련
#architecture                # 아키텍처 패턴
#best-practice               # 모범 사례
```

### 태그 검색
- 사이드바의 태그 패널에서 모든 태그 확인
- 태그 클릭으로 해당 태그가 있는 모든 노트 검색

---

## 이 프로젝트 활용법

### 1. 시작점
[index.md](index.md)를 시작점으로 사용하세요
- 모든 주제가 체계적으로 정리되어 있습니다
- Quick Navigation으로 원하는 주제로 빠르게 이동

### 2. 학습 흐름

#### 기초 개념 학습
1. [Databricks_Data_Engineering_Concepts.md](Databricks_Data_Engineering_Concepts.md) 읽기
2. Topics 폴더의 세부 주제 학습
   - [[topics/delta-lake]]
   - [[topics/delta-live-tables]]
   - [[topics/unity-catalog]]

#### 주차별 학습
1. [de_wk1_wk2_references.md](de_wk1_wk2_references.md) 부터 시작
2. 순서대로 주차별 자료 학습
3. SQL 구문 파일로 실습
   - [CREATE_FLOW_SYNTAX.sql](CREATE_FLOW_SYNTAX.sql)
   - [STREAMING_TABLE_SYNTAX.sql](STREAMING_TABLE_SYNTAX.sql)
   - [SET_CUSTOM_TAG_SYNTAX.sql](SET_CUSTOM_TAG_SYNTAX.sql)

#### 시험 준비
1. [[topics/exam-prep]] 확인
2. [question-mapping.md](question-mapping.md)로 문제 유형 파악
3. [log.md](log.md)로 진도 체크

### 3. 나만의 노트 만들기

#### 새 노트 생성
- `Cmd/Ctrl + N` 으로 새 노트 생성
- `Notes/` 폴더에 저장 권장

#### 학습 노트 템플릿
```markdown
---
created: 2026-09-30
tags: #review #important
---

# [주제명]

## 핵심 개념
-

## 예제 코드
```python
# 코드
```

## 연관 개념
- [[관련 노트 1]]
- [[관련 노트 2]]

## 복습 필요 사항
- [ ] 항목 1
- [ ] 항목 2

## 참고 자료
-
```

### 4. 유용한 플러그인 (선택사항)

#### Calendar
- 일별 학습 노트 관리
- 학습 진도 시각화

#### Dataview
- 태그나 메타데이터로 동적 리스트 생성
- 진도율 자동 계산

#### Mind Map
- 개념도 시각화
- 학습 구조 정리

#### Kanban
- 학습 진도 칸반 보드
- To-do 관리

---

## 단축키 모음

### 필수 단축키
```
Cmd/Ctrl + N              새 노트
Cmd/Ctrl + O              빠른 노트 열기
Cmd/Ctrl + P              명령 팔레트
Cmd/Ctrl + Shift + F      전체 검색
Cmd/Ctrl + G              그래프 뷰
Cmd/Ctrl + E              편집/미리보기 전환
Cmd/Ctrl + ,              설정
```

### 편집 단축키
```
Cmd/Ctrl + B              굵게
Cmd/Ctrl + I              기울임
Cmd/Ctrl + K              링크 삽입
Cmd/Ctrl + [              들여쓰기 감소
Cmd/Ctrl + ]              들여쓰기 증가
```

### 탐색 단축키
```
Cmd/Ctrl + Click          새 탭에서 링크 열기
Alt + ←                   뒤로 가기
Alt + →                   앞으로 가기
```

---

## 팁과 트릭

### 1. 빠른 메모
- 떠오르는 아이디어는 즉시 새 노트로 생성
- 나중에 정리하고 연결

### 2. 일일 노트
- Daily Notes 기능 활용
- 매일 학습한 내용 기록

### 3. 백링크 활용
- 노트 우측의 Backlinks 패널 확인
- 어떤 노트에서 현재 노트를 참조하는지 파악

### 4. 폴더 vs 링크
- 폴더는 물리적 구조
- 링크는 논리적 구조
- 두 가지를 함께 활용하면 효과적

### 5. 정기적인 리뷰
- 그래프 뷰로 고립된 노트 확인
- 연결이 부족한 노트는 다른 노트와 연결

---

## 학습 워크플로우 예시

### 새로운 개념 학습 시
1. `Cmd/Ctrl + N`으로 새 노트 생성
2. 제목과 태그 작성
3. 핵심 내용 정리
4. 관련 노트 링크 연결
5. 예제 코드 작성
6. 복습 체크리스트 생성

### 복습 시
1. `Cmd/Ctrl + Shift + F`로 `#review` 태그 검색
2. 그래프 뷰로 연관 개념 확인
3. 링크된 노트들을 순차적으로 복습
4. 이해도에 따라 태그 업데이트

### 시험 준비 시
1. [index.md](index.md)에서 전체 구조 파악
2. 주제별로 그래프 뷰 확인
3. `#important` 태그 노트 집중 복습
4. [exam-prep.md](topics/exam-prep.md) 전략 숙지
5. [question-mapping.md](question-mapping.md)로 문제 풀이

---

## 추가 리소스

### Obsidian 공식 문서
- https://help.obsidian.md/

### 커뮤니티
- Obsidian Forum: https://forum.obsidian.md/
- Discord: https://discord.gg/obsidianmd

### 튜토리얼
- YouTube: "Obsidian for Beginners"
- Obsidian 공식 튜토리얼 영상

---

## 문제 해결

### 링크가 작동하지 않을 때
- 파일 이름 정확히 확인
- 경로가 맞는지 확인
- 파일 확장자 `.md` 제외

### 동기화 문제
- Git을 사용하여 버전 관리
- `.obsidian/workspace` 파일은 개인 설정이므로 gitignore 권장

### 성능 문제
- 너무 많은 플러그인 비활성화
- 큰 이미지 파일은 외부 링크 사용
- 인덱싱 완료까지 대기

---

**Happy Learning! 🚀**

Databricks Data Engineer Associate 시험 합격을 응원합니다!