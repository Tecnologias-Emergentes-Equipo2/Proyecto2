import streamlit as st
import cv_utils
from streamlit_webrtc import webrtc_streamer
import cv2

def main():
    """ 
    Streamlit sugiere el uso de una función de ciclo principal para ejecutar todo el flujo.
    Como la aplicación es llamada desde la línea de comandos, se ejecutará a través del 
    if __name__ == 'main' 
    """

    st.title('Demo para proyecto de sistemas inteligentes')

    with st.expander('Recuperar video de Youtube'):
        url_video = st.text_input('Ingresa un url de youtube')
        url_video = url_video.strip()

        if st.button('Procesar'):
            st.subheader('Usando el widget de streamlit')
            st.video(url_video)

        if st.button('Procesar video con OpenCV'):
            stframe = st.empty()
            vf = cv_utils.get_video(url_video)
            while vf.isOpened():
                ret, frame = vf.read()
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                stframe.image(rgb)

    with st.expander('Webcam input'):
        webrtc_streamer(key='Test1')



if __name__ == '__main__':
    main()