import cv2
import numpy as np
import streamlit as st

# 1. 수관 울폐도 계산 함수 (기존 코드와 동일하되, 파일 형태만 맞춤)
def calculate_canopy_closure(image_bytes):
    # Streamlit에서 업로드한 파일을 OpenCV가 읽을 수 있게 변환
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    total_pixels = binary_mask.size
    canopy_pixels = np.sum(binary_mask == 0)
    closure_percentage = (canopy_pixels / total_pixels) * 100
    
    return closure_percentage, binary_mask

# ==========================================
# 👇 여기서부터가 앱 화면(UI)을 구성하는 부분입니다.
# ==========================================

# 앱 제목
st.title("🌳 수관 울폐도 자동 분석 앱")
st.write("스마트폰으로 촬영한 수관(나뭇가지) 사진을 업로드해주세요.")

# 파일 업로드 버튼 만들기 (카메라로 바로 찍어서 올리기도 지원됨!)
uploaded_file = st.file_uploader("사진 선택 또는 촬영", type=['jpg', 'jpeg', 'png'])

# 사용자가 사진을 업로드했다면 분석 시작
if uploaded_file is not None:
    st.write("분석을 시작합니다...")
    
    # 업로드된 사진을 바이트 형태로 읽기
    bytes_data = uploaded_file.getvalue()
    
    # 원본 사진을 앱 화면에 보여주기
    st.image(bytes_data, caption="업로드한 원본 사진", use_container_width=True)
    
    # 분석 함수 실행
    percentage, mask = calculate_canopy_closure(bytes_data)
    
    if percentage is not None:
        # 결과 수치를 크고 예쁘게 표시
        st.success("분석이 완료되었습니다!")
        st.metric(label="측정된 수관 울폐도", value=f"{percentage:.2f} %")
        
        # 흑백 변환 결과 사진을 화면에 보여주기
        st.image(mask, caption="분석된 흑백 마스크 (검은색: 수관)", use_container_width=True)
    else:
        st.error("이미지 분석에 실패했습니다. 다시 시도해주세요.")