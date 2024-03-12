import React, { useState, useEffect, useRef } from 'react';
import { useWebState } from '../hooks/useWebState'; // Adjust the import path as necessary
import ChatBoxModule from './ChatBox.module.scss';
import UpArrowButton from './UpArrowButton';

interface Convo {
    who_said_it: string;
    text: string;
  }

const ChatBox: React.FC = () => {
  const [message, setMessage] = useState<string>('');
  const [isPolling, setIsPolling] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const lastConversationRef = useRef<string>('');
  const [webState, updateWebState, isLoading, error] = useWebState('http://localhost:7867/api/get_web_state');
  const { current_convo: conversation } = webState;

  useEffect(() => {
    // Automatically adjust textarea height
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }, [message]);

  useEffect(() => {
    // Serialize current conversation for comparison
    const currentConversationSerialized = JSON.stringify(conversation);
    if (lastConversationRef.current !== currentConversationSerialized) {
      // Conversation changed
      setIsPolling(false); // Stop polling when a change is detected
      lastConversationRef.current = currentConversationSerialized;
    }

    if (isPolling) {
        const intervalId = setInterval(async () => {
          await fetchUpdatedConversation(); // This should be a new function to fetch the updated conversation
        }, 5000); // Adjust polling interval as needed
      
        return () => clearInterval(intervalId);
      }
  }, [isPolling, conversation, updateWebState]);

  const fetchUpdatedConversation = async () => {
    try {
      const response = await fetch('http://localhost:7867/api/get_web_state');
      if (!response.ok) throw new Error('Failed to fetch updated conversation');
      const data = await response.json();
      updateWebState('current_convo', data.current_convo); // Assuming 'data.current_convo' contains the updated conversation
    } catch (error) {
      console.error('Error fetching updated conversation:', error);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(event.target.value);
  };

  const handleKeyPress = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = async () => {
    if (message.trim() === '') return;

    try {
      const response = await fetch('http://localhost:7867/api/send_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "create_new_message": message }),
      });

      if (!response.ok) throw new Error('Failed to send message');
      setMessage('');
      setIsPolling(true); // Start polling after sending a message
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleClick = () => {
    sendMessage();
  };
  
  return (
    <div className={ChatBoxModule.customTextboxWidg}>
      <div className={ChatBoxModule.RealLimit}>
        <div className={ChatBoxModule.FullTextBoxWidg}>
        {Array.isArray(conversation) && conversation.map((convo: Convo, index: number) => (
            <div key={index} className={ChatBoxModule.CurrentChatWidg}>
              <div className={ChatBoxModule.leftdivbox}>
                <h2 className={ChatBoxModule.H2TagIdk1}>{convo.who_said_it}</h2>
              </div>
              <h3 className={ChatBoxModule.h3WidgCust}>{convo.text}</h3>
            </div>
          ))}
          {isLoading && <p>Loading...</p>}
          {error && <p>Error: {error}</p>}
        </div>
      </div>
      <div className={ChatBoxModule.inputDivBoxWidg}>
        <div className={ChatBoxModule.tempIdk}>
          <textarea
            ref={textareaRef}
            className={ChatBoxModule.textInputLlmBox}
            value={message}
            onChange={handleInputChange}
            onKeyDown={handleKeyPress}
            placeholder="Type your message here..."
          />
        </div>
        <div>
          <UpArrowButton onClick={handleClick} />
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
