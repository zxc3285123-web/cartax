# 자동차세 신호등

자동차 취득세 · 자동차세 계산기 사이트. 수하물 신호등과 같은 방식(파이썬 빌더 → 정적 HTML)으로 만들었습니다.

## 파일 구조

| 파일 | 역할 | 수정 빈도 |
|---|---|---|
| `_config.py` | 사이트 이름·주소·운영자·이메일·애드센스 ID | 처음 한 번 |
| `_rates.py` | 세율, 차령 산정, 감면 한도, 잔가율, 공채 매입률, 연납 공제율 | 세법 개정 시 |
| `_cars.py` | 차종 DB (185개 모델, 244개 트림) | 신차 나올 때 |
| `_posts.py` | 가이드 글 원고 20편 | 글 추가할 때 |
| `_build.py` | 빌더 | 거의 안 건드림 |
| `docs/` | **빌드 결과물** — 이 폴더가 사이트입니다 | 자동 생성 |

밑줄(`_`)로 시작하는 파일은 원고와 빌더입니다. **지우면 안 됩니다.**

## 빌드

```bash
python3 _build.py
```

`docs/` 폴더가 통째로 다시 만들어집니다. 외부 라이브러리 없이 파이썬 3만 있으면 됩니다.

## GitHub Pages 올리기

1. 깃허브에 새 저장소 `cartax` 생성 (Public)
2. 이 폴더 전체를 푸시 — `docs/` 까지 같이 커밋해야 합니다
3. 저장소 **Settings → Pages → Source** 를 **Deploy from a branch**,
   브랜치 `main`, 폴더 **`/docs`** 로 설정
4. 몇 분 뒤 `https://zxc3285123-web.github.io/cartax` 에서 열립니다

```bash
cd cartax
git init && git add -A
git commit -m "자동차세 신호등 최초 배포"
git branch -M main
git remote add origin https://github.com/zxc3285123-web/cartax.git
git push -u origin main
```

이후에는 `python3 _build.py` 하고 `git add -A && git commit -m "수정" && git push` 하면 자동 반영됩니다.

주소가 다르면 `_config.py` 의 `SITE_URL` 을 고치고 다시 빌드하세요.
사이트맵·canonical·내부 링크가 전부 그 값을 씁니다.

### ads.txt 를 루트에 두려면

`zxc3285123-web.github.io` 라는 **이름의 저장소**를 하나 더 만들고 거기에 `ads.txt` 만 넣으면
`zxc3285123-web.github.io/ads.txt` 로 서빙됩니다. 프로젝트 사이트(`/cartax`)와 별개로 동작합니다.

나중에 도메인을 사면 그 루트 저장소에 커스텀 도메인을 걸어 두는 것만으로
`/baggage` 와 `/cartax` 가 한꺼번에 새 도메인으로 옮겨갑니다.

## 자주 하는 작업

**차종 추가** — `_cars.py`에 한 줄 추가 후 빌드
```python
("현대", "신차이름", ["별칭1", "별칭2"], "승용", "국산", [
    ("트림명", 1598, 2500, "가솔린")]),   # (트림, 배기량cc, 가격 만원, 연료)
```
차종 상세 페이지·사이트맵·전체 표가 자동으로 생깁니다.

**세율 변경** — `_rates.py`의 해당 값만 수정. 계산기와 모든 글의 예시 숫자가 함께 바뀝니다.

**글 추가** — `_posts.py`의 `POSTS` 리스트에 dict 추가. 목록·이전/다음 링크·사이트맵 자동 반영.

**애드센스 승인 후** — `_config.py`의 `ADSENSE_CLIENT`에 `ca-pub-...`를 넣고 빌드하면 광고 스크립트와 `ads.txt`가 자동 생성됩니다.

## 블로그에 계산기 삽입하기

`docs/embed.html` 이 삽입 전용 경량 페이지입니다. 헤더·푸터·전체 차종표를 뺀 계산기만 들어 있고,
배경이 투명해서 어느 스킨에나 얹힙니다. `noindex` 라 본문과 중복 색인되지 않습니다.

**티스토리** — 글쓰기에서 `기본모드` → `HTML` 로 바꾸고 붙여넣기:

```html
<iframe src="https://내주소/embed.html" width="100%" height="1600"
        style="border:1px solid #dbe9e7;border-radius:12px" scrolling="no"></iframe>
```

**구글 블로그(Blogger)** — `HTML 보기` 에서 같은 코드를 붙여넣습니다.
Blogger 는 `<script>` 도 허용하므로, 아래를 함께 넣으면 높이가 자동으로 맞춰집니다:

```html
<iframe id="cartax" src="https://내주소/embed.html" width="100%" height="1600"
        style="border:1px solid #dbe9e7;border-radius:12px" scrolling="no"></iframe>
<script>
window.addEventListener("message", function(e){
  if(e.data && e.data.cartaxHeight) document.getElementById("cartax").height = e.data.cartaxHeight;
});
</script>
```

**네이버 블로그** — 불가능합니다. 스마트에디터가 `<iframe>` 과 `<script>` 를 모두 제거합니다.
대신 글 안에 차종별 세금 표를 텍스트로 넣고, 계산기로 가는 링크를 거세요.

## 애드센스 준비 상황

- [x] 개인정보처리방침 / 이용약관 / 문의 / 소개 페이지
- [x] robots.txt · sitemap.xml · 404
- [x] 가이드 글 20편 (약 17,300자)
- [x] 주제별 분류와 관련 글 내부 링크
- [ ] `zxc3285123-web.github.io` 루트 저장소에 `ads.txt` 배치 (위 참조)
- [ ] (선택) 커스텀 도메인 — 없어도 애드센스 승인에는 지장 없습니다

## 계산 근거

- 지방세법 제12조(취득세 표준세율), 제127조(자동차세), 제128조(납기·연납)
- **자동차세 산식**: 각 기분세액 = A/2 − (A/2 × 5/100)(n−2). 기분마다 계산 후 각각 10원 미만 절사
- **차령 n**: 최초등록일 기준. 1~6월 등록은 (과세연도−등록연도)+1, 7~12월 등록은 1기분만 1년 적게
- **연납 공제**: 연세액 × (납부기한 다음날~12/31 일수 ÷ 365) × 공제율
- 지방세특례제한법 제66~67조(경차·친환경차 감면), 제180조(중복감면 배제)
- 지방세 시가표준액 조사·산정 기준 [별표 16] 차량 용도별 감가상각률표
- 2023년 3월 시행 1,600cc 미만 채권매입 면제

검증 완료 항목: 자동차세 22건(차령·반기 분리 포함), 취득세 7건, 공채 7건, 연납 4건 — 파이썬 계산과 브라우저 JS 계산 결과가 일치하는지 교차 확인했습니다.
