import streamlit as st
import cv_utils
import time 
from streamlit_webrtc import webrtc_streamer
import cv2

def main():
    """ 
    Streamlit sugiere el uso de una función de ciclo principal para ejecutar todo el flujo.
    Como la aplicación es llamada desde la línea de comandos, se ejecutará a través del 
    if __name__ == 'main' 
    """
    
    model, classes, colors, output_layers = cv_utils.load_trained_yolo()

    st.title('Demo para proyecto de sistemas inteligentes')
    st.write('Este es una aplicación de muestra para nuestro modelo entrenado bajo la arquitectura YOLOv4. El objetivo del modelo es determinar si una persona tiene cubrebocas y si lo tiene mal puesto')
    st.write('Si bien el modelo funciona bajo pruebas estáticas, (véase la libreta) esta implementación es poco eficiente y podría mejorar usando dos threads con futures para la captura de imagen y el procesamiento.')

    with st.expander('Recuperar video de Youtube'):
        url_video = st.text_input('Ingresa un url de youtube')
        url_video = url_video.strip()

        if st.button('Procesar video con OpenCV'):
            stframe = st.empty()
            vf = cv_utils.get_video(url_video)
            stop = st.button('Detener')
        

            while vf.isOpened():
                ret, frame = vf.read()

                height, width, channels = frame.shape
                blob, outputs = cv_utils.detect_objs(frame, model, output_layers)
                boxes, confs, class_ids = cv_utils.get_boxes(outputs, height, width)
                res = cv_utils.draw_labels(boxes, confs, colors, class_ids, classes, frame)
                stframe.image(res)

                if stop:
                    break
            
            vf.release()

    with st.expander('Webcam input'):
        webrtc_streamer(key='Test1')



if __name__ == '__main__':
    main()