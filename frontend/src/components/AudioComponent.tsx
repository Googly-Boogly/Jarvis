// AudioComponent.js
import { useEffect, useRef, useState } from 'react';
import { Socket } from 'socket.io-client';

const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors'); // Import the cors middleware

// Create Express app
const app = express();
app.use(cors()); // Enable CORS for all routes

// Create HTTP server and attach Express app to it
const server = http.createServer(app);

// Attach Socket.io to the server
const io = new Server(server);

const AudioComponent = () => {
    const [isRecording, setIsRecording] = useState(false);
    const [stream, setStream] = useState<MediaStream | null>(null);
    const [timerInterval, setTimerInterval] = useState<NodeJS.Timeout | null>(null);
    const [transcriptLength, setTranscriptLength] = useState(0);
    
    const socket = useRef<Socket | null>(null);
    const serverIP = '3.14.136.39'; 
    const endpoint = ':80'; // Connection to backend WS
  
    useEffect(() => {
      socket.current = io(`${serverIP}${endpoint}`);
      return () => {
        socket.current?.disconnect();
      };
    }, []);
  
    const startRecording = async (event: React.MouseEvent<HTMLButtonElement>) => {
      const id = "yourId"; // Replace with the actual logic to get the id
      console.log("Recording started with id:", id);
      try {
        const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const speakerStream = await (navigator as any).mediaDevices.getDisplayMedia({
          audio: true,
          video: false,
        });
        
        const audioContext = new (window as any).AudioContext();
        const micSource = audioContext.createMediaStreamSource(audioStream);
        const speakerSource = audioContext.createMediaStreamSource(speakerStream);
  
        const destination = audioContext.createMediaStreamDestination();
        micSource.connect(destination);
        speakerSource.connect(destination);
  
        setIsRecording(true);
        setStream(destination.stream);
  
        const mimeTypes = ["audio/mp4", "audio/webm"].filter((type) =>
          MediaRecorder.isTypeSupported(type)
        );
  
        if (mimeTypes.length === 0) {
          return alert("Browser not supported");
        }
  
        setTimerInterval(
          setInterval(() => {
            setTranscriptLength((t) => t + 1);
          }, 1000)
        );
  
        let recorder = new MediaRecorder(destination.stream, { mimeType: mimeTypes[0] });
  
        recorder.addEventListener("dataavailable", async (event) => {
          if (event.data.size > 0 && socket.current?.connected) {
            socket.current?.emit("audio", { data: event.data });
          }
        });
  
        recorder.start(1000);
      } catch (error) {
        console.error("Error accessing media devices:", error);
      }
    };
  
    const stopRecording = () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
      setIsRecording(false);
      clearInterval(timerInterval!);
      socket.current?.emit("stop-transcript");
      console.log("Recording stopped");
    };

  // Code for sending data to the backend

  return (
    <div>
      <button onClick={stopRecording}>Stop Recording</button>
      <button onClick={startRecording}>Start Recording</button>
    </div>
  );
};

export default AudioComponent;