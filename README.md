# Mecaspace - YouTube English Study Video Generator

🎬 영어와 한국어 문장을 읽어주는 YouTube 학습 동영상을 자동으로 생성하는 도구입니다.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 주요 기능

- 🎙️ **다중 TTS 엔진 지원**: Google TTS (무료) 및 Azure Speech (고품질)
- 🖼️ **자동 이미지 수집**: Unsplash API 연동 또는 자동 플레이스홀더 생성
- 🎵 **배경음악 처리**: 동영상 길이에 맞춰 자동 조정
- 📹 **전문적인 동영상 생성**: 동적 인트로/아웃트로, 전환 효과, 애니메이션
- 🎥 **동적 인트로/아웃트로**: 시간대별 색상 변화, 타이핑 애니메이션, 인터랙티브 요소
- 🎨 **모던 YouTube 스타일**: 2025년 트렌드를 반영한 미니멀하고 세련된 디자인
- 📝 **YouTube 메타데이터**: 제목, 설명, 태그 자동 생성
- ⏰ **스케줄 자동화**: 매일 정해진 시간에 동영상 생성

## 🚀 빠른 시작

### 설치

```bash
# 저장소 클론
git clone https://github.com/jeromwolf/mecaspace.git
cd mecaspace

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 설정
cp .env.example .env
```

### 첫 동영상 생성

```bash
# 샘플 데이터 생성
python main.py --sample

# 동영상 생성
python main.py sample_sentences.csv
```

## 📖 상세 사용법

### 동영상 생성 옵션

```bash
python main.py input.csv -o "output.mp4" -t nature -m calm
```

**옵션 설명:**
- `-o, --output`: 출력 파일명 (기본값: 자동 생성)
- `-t, --theme`: 배경 이미지 테마
  - `nature` (기본값): 자연 풍경
  - `study`: 학습 환경
  - `city`: 도시 풍경
  - `abstract`: 추상적 이미지
- `-m, --music`: 배경음악 스타일
  - `calm` (기본값): 차분한 음악
  - `upbeat`: 활기찬 음악
  - `inspiring`: 영감을 주는 음악

### 입력 파일 형식

**CSV 형식** (권장):
```csv
English,Korean
Hello, how are you?,안녕하세요, 어떻게 지내세요?
I'm learning English.,저는 영어를 배우고 있습니다.
Nice to meet you.,만나서 반갑습니다.
```

**JSON 형식**:
```json
[
  {"english": "Hello", "korean": "안녕하세요"},
  {"english": "Thank you", "korean": "감사합니다"}
]
```

**Excel 형식**: `.xlsx` 또는 `.xls` 파일도 지원

### 자동 스케줄링

```bash
# 스케줄 데이터 준비
python scheduler.py --create-sample-data

# 매일 오전 8시 자동 실행
python scheduler.py
```

### 모던 에셋 생성

```bash
# 모던 스타일 인트로/아웃트로 생성
python -m src.utils.modern_assets

# 커스텀 썸네일 생성
python -m src.utils.thumbnail_generator
```

## ⚙️ 환경 설정

### API 키 설정 (선택사항)

`.env` 파일에서 다음 설정을 할 수 있습니다:

```env
# 고품질 이미지를 위한 Unsplash API
UNSPLASH_ACCESS_KEY=your_key_here

# 자연스러운 음성을 위한 Azure Speech
AZURE_SPEECH_KEY=your_key_here
AZURE_SPEECH_REGION=koreacentral

# YouTube 자동 업로드를 위한 API
YOUTUBE_API_KEY=your_key_here
```

> 💡 **참고**: API 키가 없어도 기본 기능은 모두 작동합니다!

### 동영상 설정

```env
# 동영상 해상도
VIDEO_WIDTH=1920
VIDEO_HEIGHT=1080

# 문장 표시 시간 (초)
SENTENCE_DISPLAY_TIME=8

# 배경음악 볼륨 (0.0-1.0)
MUSIC_VOLUME=0.1

# 애니메이션 설정
TYPING_SPEED=0.05  # 타이핑 애니메이션 속도
TRANSITION_TIME=1.0  # 전환 효과 시간
```

## 📁 프로젝트 구조

```
mecaspace/
├── 📂 src/
│   ├── 📂 core/          # 핵심 설정 및 구성
│   ├── 📂 services/      # 서비스 모듈
│   │   ├── tts_service.py      # 음성 합성
│   │   ├── image_service.py    # 이미지 수집
│   │   ├── music_service.py    # 배경음악 처리
│   │   └── video_service.py    # 동영상 생성
│   └── 📂 utils/         # 유틸리티
│       ├── data_loader.py      # 데이터 로더
│       ├── youtube_metadata.py # YouTube 메타데이터
│       ├── modern_assets.py    # 모던 인트로/아웃트로 생성
│       └── thumbnail_generator.py # 썸네일 생성
├── 📂 output/            # 생성된 파일
├── 📂 data/              # 입력 데이터
├── 📂 assets/            # 생성된 에셋 파일
├── 📄 main.py            # 메인 실행 파일
├── 📄 scheduler.py       # 스케줄러
└── 📄 requirements.txt   # 의존성 목록
```

## 🎥 출력 예시

생성된 동영상은 다음과 같은 구성을 가집니다:

1. **동적 인트로** (4초): 
   - 시간대별 그라데이션 배경 (아침: 산호색, 오후: 하늘색, 저녁: 보라색, 밤: 남색)
   - 타이핑 애니메이션 효과로 나타나는 제목
   - 플로팅 애니메이션 장식 요소
   - 슬라이드인 자막 효과

2. **메인 콘텐츠**: 각 문장마다
   - 영어 문장 표시 및 음성 (타이핑 애니메이션)
   - 한국어 번역 표시 및 음성
   - 반투명 백그라운드 보드로 가독성 향상
   - 배경 이미지와 음악
   - 학습 효과를 위한 영어 문장 반복

3. **동적 아웃트로** (5초): 
   - 방사형 그라데이션 배경
   - 펄스 애니메이션 구독 버튼
   - 좋아요 버튼과 알림 벨 아이콘
   - 감사 메시지와 다음 영상 예고

## 🔧 문제 해결

### FFmpeg 설치 필요
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# https://ffmpeg.org/download.html 에서 다운로드
```

### 일반적인 문제들

| 문제 | 해결 방법 |
|------|----------|
| TTS 오류 | `.env`에서 `TTS_ENGINE=gtts`로 변경 |
| 이미지 로드 실패 | 인터넷 연결 확인, API 키 확인 |
| 메모리 부족 | 동영상 해상도 낮추기 |

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

## 👨‍💻 개발자

- **Jerome Wolf** - [GitHub](https://github.com/jeromwolf)

## 📦 버전 기록

### v2.0.0 (2025-07-31)
- ✨ 동적 인트로/아웃트로 기능 추가
- 🎨 시간대별 그라데이션 배경 효과
- ⌨️ 타이핑 애니메이션 효과 구현
- 🎬 모던 YouTube 스타일 디자인
- 🖼️ 향상된 썸네일 생성기
- 📱 반응형 텍스트 레이아웃

### v1.0.0 (2025-01-01)
- 🎉 첫 릴리즈
- 🎙️ TTS 엔진 통합
- 🖼️ Unsplash API 연동
- 📹 기본 동영상 생성 기능

## 🙏 감사의 말

- 영어 학습에 도움을 주신 모든 분들께 감사드립니다
- 오픈소스 커뮤니티에 감사드립니다