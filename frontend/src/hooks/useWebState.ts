import { useState, useEffect } from 'react';


interface Convo {
  who_said_it: string;
  text: string;
}

interface Model {
    model_id: number;
    model_name: string;
    model_info: string;
    // Include any other model properties you need
  }
  
  interface Agent {
    agent_id: number;
    agent_name: string;
    agent_description: string;
    // Include any other agent properties you need
  }

interface PastConvo {
    chat_id: number;
    title: string;
    added: string;
    updated: string;
    total_chats_id: number; // Add this property if required by ConvoDetails
  }

interface WebState {
  website_state_id?: number;
  user_id?: number;
  tts: boolean;
  stt: boolean;
  current_chat?: number;
  modelSelected: string;
  temperature: string;
  agentSelected: string;
  added?: string; // Store as ISO string
  updated?: string; // Store as ISO string
  pastConvos: PastConvo[];
  current_convo: Convo[];
  models: Model[];
  agents: Agent[];
}

// Assuming API response aligns with this structure
interface APIResponse {
  website_state_id?: number;
  user_id?: number;
  tts: boolean;
  stt: boolean;
  current_chat?: number;
  model_selected: string;
  temperature: number;
  agent_selected: string;
  added: string; // Assuming the API provides this as a string
  updated: string;
  past_convos: PastConvo[];
  current_convo: Convo[];
  models: Model[];
  agents: Agent[];
}

interface UseWebStateReturn {
    webState: WebState;
    updateWebState: (type: 'Model' | 'Temperature' | 'Agent', value: string) => void;
    isLoading: boolean;
    error: string | null;
  }

  export function useWebState(apiUrl: string, pollingInterval: number | null = null): [WebState, (type: keyof WebState, value: any) => void, boolean, string | null] {
    const [webState, setWebState] = useState<WebState>({
      modelSelected: '',
      temperature: '',
      agentSelected: '',
      pastConvos: [],
      stt: false,
      tts: false,
      current_convo: [],
      models: [],
      agents: [],
    });
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
  
    useEffect(() => {
      const fetchWebState = async () => {
        setIsLoading(true);
        try {
          const response = await fetch(apiUrl);
          if (!response.ok) throw new Error('Failed to fetch web state');
          const data: APIResponse = await response.json();
          const newState: WebState = {
            ...data,
            modelSelected: data.model_selected,
            agentSelected: data.agent_selected,
            temperature: data.temperature.toString(),
            pastConvos: data.past_convos,
            current_convo: data.current_convo,
            models: data.models,
            agents: data.agents,
          };
          setWebState(newState);
        } catch (error) {
          setError('Failed to load data from the server');
        } finally {
          setIsLoading(false);
        }
      };
  
      fetchWebState(); // Initial fetch
  
      let interval: NodeJS.Timeout | null = null;
      if (pollingInterval && pollingInterval > 0) {
        // Start polling only if pollingInterval is greater than 0
        interval = setInterval(fetchWebState, pollingInterval);
      }
  
      return () => {
        if (interval) clearInterval(interval); // Cleanup on component unmount
      };
    }, [apiUrl, pollingInterval]);
  
    const updateWebState = (type: keyof WebState, value: any) => {
      setWebState((prev) => ({
        ...prev,
        [type]: value,
      }));
    };
  
    return [webState, updateWebState, isLoading, error];
  }
  