
한국어 문서 내 검색 기능

개발 환경 :
 - Linux
 - Python 2.7.3
 
필요한 패키지 :
 - konlpy
 - mecab-ko-dic
 - mecab-ko
 - pyhwp
 - pyopenssl
 - odt2txt
 
실행하는 데 필요한 파일 :
 - ko_ui_test.py
 - ko_extraction.py
 - hwp, txt, odt, docx, pdf 형식의 파일
 
실행 방법 :
 1. ko_ui_test.py 실행
 2. 'File Open' 버튼 클릭
 3. 파일 선택
 4. 'Conversion to text' 버튼 클릭
 5. 입력란에 검색하고 싶은 단어 입력
 6. 'Search' 버튼 클릭

결과 : 
  - 검색 결과 입력한 단어와 일치하는 단어가 있으면 그 단어가 포함된 파일의 경로와 파일명을 보여줌 
  ex) /python/example.pdf
  - 일치하는 단어가 없을 경우 'No Such File!' 이라는 문구를 보여줌

제약 조건 :
 * 한 번 text로 변경된 파일은 기록에 남아있으므로 후에 다시 text로 변경할 필요가 없음
 * 수정된 파일은 다시 text로 변경해야 함
 * 한국어 검색만 가능
