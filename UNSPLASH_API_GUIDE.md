# Unsplash API 키 생성 가이드

## 1. Unsplash 개발자 계정 만들기

1. [Unsplash Developers](https://unsplash.com/developers) 페이지 방문
2. 우측 상단의 "Register as a developer" 클릭
3. Unsplash 계정이 없다면 먼저 회원가입
4. 개발자 약관에 동의

## 2. 새 애플리케이션 생성

1. 로그인 후 대시보드에서 "New Application" 버튼 클릭
2. 애플리케이션 이름 입력 (예: "English Study Video Generator")
3. 애플리케이션 설명 입력
4. 용도 선택 (Personal 또는 Commercial)
5. API 사용 가이드라인에 동의

## 3. API 키 받기

1. 애플리케이션 생성 후 대시보드에서 해당 앱 클릭
2. "Keys" 섹션에서 다음 정보 확인:
   - **Access Key**: 공개 키 (이것을 사용)
   - **Secret Key**: 비밀 키 (보안 유지)

## 4. 프로젝트에 API 키 설정

`.env` 파일에 다음과 같이 추가:
```
UNSPLASH_ACCESS_KEY=your_access_key_here
```

## 5. 무료 사용 제한

- **Demo (개발) 단계**: 시간당 50회 요청
- **Production 승인 후**: 시간당 5,000회 요청
- 더 많은 요청이 필요하면 Unsplash+에 가입

## 6. Production 승인 받기 (선택사항)

더 많은 API 요청이 필요한 경우:
1. 대시보드에서 애플리케이션 선택
2. "Apply for Production" 클릭
3. 애플리케이션 설명과 사용 목적 상세히 작성
4. 승인까지 며칠 소요

## 주의사항

- API 키를 GitHub 등에 업로드하지 마세요
- Unsplash API 사용 시 이미지 출처 표시 필수
- 상업적 용도로 사용 시 라이선스 확인