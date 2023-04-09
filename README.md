## 1. 데이터베이스 설계

효율적이고 유연한 구조로, 각 테이블 간의 관계를 명확하게 설계했습니다. 사용자 인증 및 권한 관리를 효과적으로 수행하며, 가계부 및 예산 정보를 사용자 별로 관리할 수 있습니다. 이로써 사용자가 원활하게 서비스를 이용하고 시스템 확장 및 유지보수가 용이 해집니다.

- `User`: 사용자 정보(Django의 AbstractUser상속)
    - id (PK): 사용자 식별자
    - username: 이메일 (unique, 이메일로 회원가입)
- `CustomType`: 사용자 정의 지출 유형
    - id (PK): 지출 유형 식별자
    - user_id (FK): 사용자 식별자
    - name : 지출 유형 이름
- `Ledger`: 가계부 정보
    - id (PK): 가계부 식별자
    - user_id (FK): 사용자 식별자
    - type_id (FK): 지출 유형
    - name: 가계부 제목
    - memo: 가계부에 상세한 메모
    - amout: 지출 비용
    - date: 지출 날짜
- `SharedLedger`: 공유된 가계부 정보
    - id (PK): 공유된 가계부 식별자
    - ledger_id (FK): 가계부 식별자
    - token: uuid 토큰 (unique)
    - encoded_token: Base62로 인코딩된 토큰
    - expires_at: 만료되는 날짜
- `Monthly_budget`:
    - id (PK): 월 별 예산 식별자
    - user_id (FK): 사용자 식별자
    - year: 해당 연도
    - month: 해당 월
    - budget: 해당 월의 예산

## 2. REST API설계

RESTful API 디자인 원칙을 따르고 있어, 일관성 있는 엔드포인트 작성이 가능하고 각 리소스에 대해 적절한 HTTP 메서드를 사용합니다. 이를 통해 유지보수와 확장성이 증가하며, 개발자가 API를 쉽게 이해할 수 있습니다.

- `User`: 사용자
    - `POST /api/users`: 사용자 회원가입
    - `POST /api/users/signin`: 사용자 로그인
    - `POST /api/users/signout`: 사용자 로그아웃
    - `GET /api/users/me`: 현재 로그인한 사용자의 정보 조회
    - `PATCH /api/users/password`: 현재 로그인한 유저의 패스워드 
- `CustomType`: 사용자 정의 지출 유형
    - `GET /api/custom-types`: 사용자가 추가한 모든 지출 유형 조회
    - `POST /api/custom-types`: 새로운 지출 유형 추가
    - `PUT /api/custom-types/{name}`: 지출 유형 수정
    - `DELETE /api/custom-types/{name}`: 지출 유형 삭제
- `Ledger`: 가계부
    - `GET /api/ledgers`: 사용자의 가계부 목록 조회
    - `POST /api/ledgers`: 새로운 가계부 항목 추가
    - `GET /api/ledgers/{id}`: 특정 가계부 항목 조회
    - `PUT /api/ledgers/{id}`: 특정 가계부 항목 수정
    - `DELETE /api/ledgers/{id}`: 특정 가계부 항목 삭제
    - `POST /api/ledgers/{id}/duplicate`: 특정 가계부 항목 복제
    - `POST /api/ledgers/{id}/share`: 특정 가계부 항목 공유 URL 생성
    - `DELETE /api/ledgers/{id}/share`: 특정 가계부 항목 공유 삭제
    - `GET /api/ledgers/date`: 특정 연월의 가계부 목록 조회
    - `GET /{token}`: 공유된 특정 가계부 항목 조회
- `MonthlyBudget`: 월별 예산
    - `GET /api/monthly-budgets`: 사용자의 월별 예산 목록 조회
    - `POST /api/monthly-budgets`: 새로운 월별 예산 추가
    - `GET /api/monthly-budgets/{id}`: 특정 월별 예산 조회
    - `PUT /api/monthly-budgets/{id}`: 특정 월별 예산 수정
    - `DELETE /api/monthly-budgets/{id}`: 특정 월별 예산 삭제
    

## 3. 아키텍쳐 설계

- 웹 서버: `Nginx`의 리버스 프록시를 통해 백엔드 서버로 요청을 전달합니다. 이를 통해서 갑작스러운 사용자 증가에도 유연하게 대처할 수 있습니다.
- 백엔드 서버: `DRF`를 사용하여 빠르고 효율적인 API 서버를 개발합니다. 재사용 가능한 코드 작성이 가능합니다.
- 데이터베이스: `Mysql 5.7` 버전을 사용하며, 장고의 ORM 기능을 활용하여 쉽고 안정적으로 데이터를 관리합니다.
- 배포: `Docker`를 사용하여 컨테이너화된 서비스를 제공함으로써, 환경 구성이 단순화되고, 배포 및 관리가 용이합니다.
- 보안: 인증에 `JWT`토근 방식을 사용합니다. RSA를 사용해 비밀번호를 암호화  전달합니다.
- 코드 스타일: `pre-commit, isort, pylint, black, autoflake`을 사용해 일관된 코드 스타일을 유지하여 협업시 문제를 최소화합니다.

## 4. 진행하면서 겪은 문제들

1. mysqlclient 설치 문제 해결:
    - Homebrew를 사용하여 MySQL 라이브러리를 설치한 후에 다시 시도하였습니다. 이를 통해mysqlclient 설치 문제가 해결되었습니다.
2. Mysql 5.7과 Django 4.2 연결 문제 해결:
    - Mysql 5.7 버전과 Django 4.2 버전 간의 호환성 문제로 인해 연결이 되지 않았습니다. 이를 해결하기 위해 Django 버전을 3.2로 다운그레이드하여 호환성 문제를 해결하였습니다.
3. 장고 쿼리 카운트 라이브러리를 활용한 최적화:
    - 장고 쿼리 카운트 라이브러리를 사용하여 쿼리 조회 성능을 측정하였고, 로그인 함수에서 불필요한 쿼리가 발생하는 것을 발견하였습니다. 이를 최적화하여 로그인 과정의 성능을 개선하였습니다.
    - 최적화 전
        
        ```python
        token = TokenObtainPairSerializer().validate(data)
        user = authenticate(**data)
        ```
        
        | Type | Database | Reads | Writes | Totals | Duplicates |
        | --- | --- | --- | --- | --- | --- |
        | RESP | default | 4 | 1 | 5 | 2 |
        | ------ | ----------- | ---------- | ---------- | ---------- | ------------ |
        
        Total queries: 5 in 0.1474s
        
    - 최적화 후
        
        ```python
        user = authenticate(**data)
        
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        token = RefreshToken.for_user(user)
        ```
        
        | Type | Database | Reads | Writes | Totals | Duplicates |
        | --- | --- | --- | --- | --- | --- |
        | RESP | default | 3 | 1 | 4 | 0 |
        | ------ | ----------- | ---------- | ---------- | ---------- | ------------ |
        
        Total queries: 4 in 0.1014s
        
4. drf-spectacular와 serializer의 depth 문제 해결:
    - drf-spectacular를 사용할 때 serializer의 depth 부분에서 에러가 발생하였습니다. 이를 해결하기 위해 drf-spectacular의 depth 지원 여부를 조사 하였고, 지원하지 않음을 확인하였습니다. 그 결과, serializer에서 depth를 제거하고 순환 참조가 발생할 수 있는 필드를 exclude로 제거하여 문제를 해결하였습니다.

## 5. 코드에 관한 생각

1. 확장 가능한 코드를 작성
    - 확장 가능한 코드를 작성하기 위해 읽기 쉽고 중복이 없는 코드를 작성 하였으며, 테스트하기 쉬운 구조를 고려하고 다른 코드와의 간섭을 최소화하였습니다.
2. 프로젝트 진행 중 테이블 구조 변경
    - 프로젝트 진행 중 테이블 구조 변경이 필요할 때, 테스트 때는 삭제 후 재 테스트가 가능하나 실제 운영 환경에서는 어려움이 있습니다. 영향 없는 변경은 진행하고, 영향 있는 경우엔 데이터 추출 후 충돌 해결 후 다시 삽입하는 방식을 생각했습니다. 더 좋은 방법을 알려주시면 감사하겠습니다!
3. api/ 프리픽스 사용
    - API 설계 과정에서, api/ 프리픽스를 사용함으로써 API와 페이지를 명확하게 구분했습니다. 하지만, 이로 인해 drf-spectacular가 생성한 Swagger 문서에서 모든 API가 하나의 카테고리로 표시되어 읽기 어렵습니다. 이에 대해 저는 프론트 서버와 백엔드 서버가 동일한 컴퓨터에서 실행되는 경우에는 api/ 프리픽스를 사용하는 것이 좋지만, 서버가 분리된 경우에는 프리픽스를 사용하지 않고 Swagger 문서의 가독성을 향상시키는 것이 좋다고 생각합니다.
4. ViewSet과 ModelViewSet의 선택
    - ViewSet과 ModelViewSet의 사용에 따라 유연성과 기본 CRUD 동작을 고려하여, 각 앱 별로 적절한 방식을 선택하였습니다.
5. [settings.py](http://settings.py) 분리
    - 여러 개발자와의 협업을 효율적으로 진행하기 위해, settings.py를 base, prod, local로 분리하여 관리하였습니다.
6. 단축 URL 기능을 구현하며 생각한 내용
    - 외부 서비스 대신 직접 구현
        - 외부 API 의존도를 줄이기 위해 가능한 경우 직접 구현하는 것이 좋다고 판단했습니다.
    - SHA256 대신 uuid v4 사용
        - 동일한 데이터라도 고유한 값을 생성하기 위해 무작위 UUID를 사용했습니다.
    - Base62 인코딩
        - URL에 안전하지 않은 문자를 배제한 Base62 인코딩 방식을 사용하여 UUID의 정수값 앞 14자리를 선택해 인코딩하여 단축 URL을 생성하였습니다.
        - 관련 코드
            
            ```python
            @action(detail=True, methods=["post"], url_path="share", url_name="share")
            def share_ledger(self, request: HttpRequest, pk: Optional[str] = None) -> Response:
                ledger = Ledger.objects.get(id=pk)
                expiration_date = datetime.datetime.now() + timedelta(days=1)
                shared_ledger = SharedLedger.objects.create(
                    ledger=ledger, expires_at=expiration_date
                )

                encoded_token = base62_encode(shared_ledger.token.int % 10**14)

                shared_ledger.encoded_token = encoded_token
                shared_ledger.save()

                share_url = request.build_absolute_uri(
                    reverse("shared-ledger", args=[encoded_token])
                )

                return Response({"url": share_url}, status=status.HTTP_200_OK)
            ```
            
    - 단축 URL 조회
        - SharedLedger의 encoded_token을 사용하여 검색을 수행한 후 만료 여부를 확인하고, 만료되지 않았다면 ledger의 내용을 반환합니다.
        - 관련 코드
            
            ```python
            class SharedLedger(models.Model):
                id = models.BigAutoField(primary_key=True)
                token = models.UUIDField(default=uuid.uuid4, unique=True)
                encoded_token = models.CharField(max_length=100, unique=True, blank=True)
                ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
                expires_at = models.DateTimeField()
                created_at = models.DateTimeField(auto_now_add=True)
            
                def is_expired(self):
                    return datetime.datetime.now() > self.expires_at
            
                def __str__(self):
                    return str(self.token)
            
            def retrieve(self, request: HttpRequest, token: str) -> Response:
                shared_ledger = SharedLedger.objects.get(encoded_token=token)

                if shared_ledger.is_expired():
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializer = LedgerSerializer(shared_ledger.ledger)

                return Response(serializer.data, status=status.HTTP_200_OK)
            ```
            
    - 이러한 접근 방식을 통해 단축 URL 기능을 성공적으로 구현하였고, 이 과정에서 다양한 기술적 고려 사항을 다루게 되었습니다. 이 경험이 앞으로의 프로젝트에서도 도움이 될 것이라 생각합니다.
7. RSA사용
    - 비밀번호를 단순히 https로 전달하면 안전할 것이라 생각했습니다. 하지만 어떻게 하면 더 안전하게 전송할 수 있을까 조사하던중 RSA 비대칭키를 사용하면 안전하다는 정보를 얻었습니다. pycryptodome를 사용해 제 프로젝트에 적용했습니다.

## 6. 테스트 방법

총 53개의 테스트 코드를 작성했습니다. 직접 테스트 해보는 방법은 다음과 같습니다. (m1 mac환경)

```bash
git clone https://github.com/chawanghyeon/python-ledger.git
```

프로젝트 루트 파일로 이동 후 아래 명령어를 실행합니다.

```bash
docker-compose up -d
```

실행 완료 후 mysql terminal에서 다음 명령어들을 실행합니다.
root 비밀번호는 rootpassword입니다.

```bash
mysql -u root -p
GRANT ALL PRIVILEGES ON payhere.* TO 'payhere'@'%';
GRANT ALL PRIVILEGES ON test_payhere.* TO 'payhere'@'%';
FLUSH PRIVILEGES;
exit
```

web이 실행되고 있는 terminal에서 다음 명령어를 실행합니다.

```bash
python manage.py test --settings=payhere.settings.prod
```
