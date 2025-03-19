import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

# 한글 폰트 설정 (한글이 깨지는 문제 해결)
matplotlib.rc('font', family='Malgun Gothic')  # 윈도우용
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

# 사용자 입력을 저장할 네트워크 데이터
if 'contacts' not in st.session_state:
    st.session_state.contacts = []
if 'edges' not in st.session_state:
    st.session_state.edges = []

# 사용자 입력 폼
st.sidebar.header("네트워크 구성")
name = st.sidebar.text_input("이름 입력")
phone = st.sidebar.text_input("전화번호 입력")
related_name = st.sidebar.selectbox("연결할 사람", [""] + [c[0] for c in st.session_state.contacts if c[0] != name])
strength = st.sidebar.slider("관계 강도 (1-10)", 1, 10, 5)

if st.sidebar.button("추가하기"):
    if name and phone:
        if name not in [c[0] for c in st.session_state.contacts]:
            st.session_state.contacts.append((name, phone))
        if related_name and related_name in [c[0] for c in st.session_state.contacts]:
            st.session_state.edges.append((name, related_name, strength))
        st.sidebar.success(f"{name} 추가 완료!")
    else:
        st.sidebar.error("이름과 전화번호를 입력하세요.")

# 네트워크 다이어그램 생성 함수
def draw_network():
    G = nx.Graph()
    
    if not st.session_state.contacts:
        st.warning("네트워크에 추가된 사람이 없습니다.")
        return
    
    # 기존 차트 초기화 (Streamlit 렌더링 오류 방지)
    plt.clf()
    
    contact_names = [c[0] for c in st.session_state.contacts]
    for contact in contact_names:
        G.add_node(contact)
    
    for edge in st.session_state.edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    
    plt.figure(figsize=(5, 5))
    pos = nx.spring_layout(G, seed=42)  # 동일한 레이아웃 유지
    
    edges_weights = [edge[2] for edge in st.session_state.edges]
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='black', font_family='Malgun Gothic', width=[w / 2 for w in edges_weights])
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(edge[0], edge[1]): str(edge[2]) for edge in st.session_state.edges}, font_family='Malgun Gothic')
    
    st.pyplot(plt)

# Streamlit UI
st.title("네트워크 다이어그램")

if st.button("네트워크 보기"):
    draw_network()
