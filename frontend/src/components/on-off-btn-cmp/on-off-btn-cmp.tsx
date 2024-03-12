import React, { useState, useEffect } from 'react';
import styles from './on-off-btn-cmp.module.scss';

interface OnOffBtnCmpProps {
    stt: boolean;
}

export const OnOffBtnCmp: React.FC<OnOffBtnCmpProps> = ({ stt }) => {
    const [isOn, setIsOn] = useState<boolean>(stt);
    const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
    const [ws, setWs] = useState<WebSocket | null>(null);

    useEffect(() => {
        const webSocket = new WebSocket('ws://localhost:7867/ws/audio/stt');
        setWs(webSocket);

        webSocket.onopen = () => {
            console.log('WebSocket connected');
        };

        webSocket.onerror = (error: Event) => {
            console.error('WebSocket Error:', error);
        };

        webSocket.onclose = () => {
            console.log('WebSocket Disconnected');
        };

        return () => {
            webSocket.close();
        };
    }, []);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const recorder = new MediaRecorder(stream);
            setMediaRecorder(recorder);

            recorder.ondataavailable = (event: BlobEvent) => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    console.log(event.data)
                    ws.send(event.data);
                }
            };

            recorder.start(200); // Emit data every 200ms
        } catch (error) {
            console.error('Error accessing the microphone:', error);
        }
    };

    const stopRecording = () => {
        if (mediaRecorder) {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach((track: MediaStreamTrack) => track.stop());
            setMediaRecorder(null); // Clear the recorder once stopped
        }
    };

    const toggleSTT = async () => {
        try {
            const response = await fetch('http://localhost:7867/api/stt_toggle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ stt_on_off: !isOn }), // Adjust this payload as needed for your backend
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }

            const data = await response.json();
            console.log('STT Toggle Success:', data);
        } catch (error) {
            console.error('Error toggling STT:', error);
            setIsOn(isOn); // Optionally revert the state if the API call fails
        }
    };

    const toggleButton = async () => {
        setIsOn(!isOn);

        if (!isOn) {
            stopRecording();

            await toggleSTT();
        } else {
            await startRecording();
            await toggleSTT();
        }
    };

    const buttonClass = isOn ? styles.OnOffB : `${styles.OnOffB} ${styles.OffB}`;

    return (
        <div className={styles.root}>
            <button className={buttonClass} onClick={toggleButton}>
                {isOn ? 'STT, Off' : 'STT, On'}
            </button>
        </div>
    );
};
