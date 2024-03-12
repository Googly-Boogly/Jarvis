import React, { useState, useEffect } from 'react';
import PastConvos_module from './PastConvos.module.scss';

interface ConvoDetails {
    chat_id: number;
    title: string;
    added: string;
    updated: string;
    total_chats_id: number;
  }
  
  interface PastConvosProps {
      previousconvo: ConvoDetails[];
  }

function PastConvos({ previousconvo }: PastConvosProps) {
    const [isLoading, setIsLoading] = useState(false); // For loading state management

    const startNewChat = async () => {
        setIsLoading(true); // Start loading
        try {
            const response = await fetch('http://localhost:7867/api/create_new_chat', {
                method: 'POST', // Assuming a POST request is required
            });
            if (!response.ok) {
                throw new Error('Failed to start new chat');
            }
            console.log('New chat initialized');
            window.location.reload();
            // Here you would ideally inform the parent component to refresh the state,
            // but since it's not directly connected to fetching logic here, consider using a callback prop if necessary.
        } catch (error) {
            console.error('Error starting new chat:', error);
        } finally {
            setIsLoading(false); // End loading
        }
    };

    const selectPastConvo = async (chat_id: number) => {
        try {
            const response = await fetch('http://localhost:7867/api/chat_select', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ chat_id }), // Updated to use chat_id
            });
            if (!response.ok) {
                throw new Error('Failed to select past conversation');
            }
            console.log(`Past conversation selected with ID: ${chat_id}`);
            window.location.reload();
        } catch (error) {
            console.error(`Error selecting past conversation with ID (${chat_id}):`, error);
        }
    };

    return (
        <div className={PastConvos_module.MainContainerDivPastConvos}>
            {isLoading ? (
                <div>Loading...</div>
            ) : (
                <>
                    <div className={PastConvos_module.NewChat} onClick={!isLoading ? startNewChat : undefined}>
                        <h3>New Chat</h3>
                    </div>
                    <div>
                        {previousconvo.map((convo, index) => (
                            <div key={index} className={PastConvos_module.PastConversationDivWidg} onClick={() => selectPastConvo(convo.chat_id)}>
                                <h2>{convo.title}</h2>
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
}

export default PastConvos;
