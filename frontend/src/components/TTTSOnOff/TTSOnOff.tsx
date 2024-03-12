import React, { useState, useEffect } from 'react';
import styles from './TTSOnOff.module.scss';

interface TTSOnOffProps {
  tts: boolean;
}

export const TTSOnOff: React.FC<TTSOnOffProps> = ({ tts }) => {
  const [isOn, setIsOn] = useState<boolean>(tts);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const webSocket = new WebSocket('ws://localhost:7867/ws/audio/tts'); // Adjust this URL to your WebSocket endpoint
    webSocket.binaryType = 'arraybuffer';
    setWs(webSocket);

    webSocket.onmessage = () => {
      playMp3();
    };

    return () => {
      if (webSocket) webSocket.close();
    };
  }, []);

  const playMp3 = () => {
    // Directly use the MP3 URL from your backend
    const mp3Url = 'http://localhost:7867/api/serve_mp3'; // Adjust this URL as needed
    const audio = new Audio(mp3Url);
    audio.play().catch((error) => console.error('Error playing audio:', error));
  };

  const toggleButton = async () => {
    setIsOn(!isOn); // Optimistically toggle the state for a responsive UI

    try {
      const payload = {
        tts_on_off: !isOn,
      };

      const response = await fetch('http://localhost:7867/api/tts_toggle', { // Adjust this URL to your actual endpoint URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Success:', data);
      // Optionally update the state based on the response
    } catch (error) {
      console.error('Error:', error);
      setIsOn(isOn); // Revert the state in case of an error
    }
  };

  const buttonClass = isOn ? styles.OnOffB : `${styles.OnOffB} ${styles.OffB}`;

  return (
    <div className={styles.root}>
      <button className={buttonClass} onClick={toggleButton}>
        {isOn ? 'TTS, Off' : 'TTS, On'}
      </button>
    </div>
  );
};
