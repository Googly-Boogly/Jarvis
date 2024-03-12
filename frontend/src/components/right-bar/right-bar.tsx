import React, { useState, useEffect } from 'react';
import classNames from 'classnames';
import styles from './right-bar.module.scss';



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


export interface RightBarProps {
  className?: string;
  modelSelected: string;
  temperature: string;
  agentSelected: string;
  models: Model[];
  agents: Agent[];
  onUpdateModel: (modelSelected: string) => void;
  onUpdateTemperature: (temperature: string) => void;
  onUpdateAgent: (agentSelected: string) => void;
}

export const RightBar = ({
  className,
  modelSelected,
  temperature,
  agentSelected,
  onUpdateModel,
  onUpdateTemperature,
  onUpdateAgent,
  models,
  agents,
}: RightBarProps) => {
  const [selectedModel, setSelectedModel] = useState(modelSelected);
  const [selectedTemperature, setSelectedTemperature] = useState(temperature);
  const [selectedAgent, setSelectedAgent] = useState(agentSelected);

  // Use useEffect to update local state if props change
  useEffect(() => {
    setSelectedModel(modelSelected);
    setSelectedTemperature(temperature);
    setSelectedAgent(agentSelected);
  }, [modelSelected, temperature, agentSelected]);
  console.log(models)
  console.log(agents)
  const updateSelection = async (type: 'Model' | 'Temperature' | 'Agent', value: string) => {
    let endpoint = '';
    switch (type) {
      case 'Model':
        setSelectedModel(value);
        endpoint = 'http://localhost:7867/api/model_change';
        onUpdateModel(value); // Corrected to use the specific prop function
        break;
      case 'Temperature':
        setSelectedTemperature(value);
        endpoint = 'http://localhost:7867/api/temp_change';
        onUpdateTemperature(value); // Corrected to use the specific prop function
        break;
      case 'Agent':
        setSelectedAgent(value);
        endpoint = 'http://localhost:7867/api/agent_select';
        onUpdateAgent(value); // Corrected to use the specific prop function
        break;
      default:
        console.error('Invalid selection type');
        return;
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ value }),
      });

      if (!response.ok) {
        throw new Error('Failed to update selection');
      }

      const data = await response.json();
      console.log(`${type} updated:`, data);
      
      // No need to reload the page, as we're now properly updating the parent state.
      // window.location.reload(); // Consider removing this to prevent reloading.
    } catch (error) {
      console.error(`Error updating ${type}:`, error);
    }
  };


  // Hardcoded options for the dropdowns

  const temperatures = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'];


  return (
    <div className={classNames(styles.root, className)}>
      {/* Model Selection */}
      <div className={styles.dividerCls}>
        <div className={styles.rightbarh}>
          <h3>Model Selected: </h3>
        </div>
        <div className={styles.botRandom}>
          <select
            className={styles.selectorcls}
            value={selectedModel}
            onChange={(e) => updateSelection('Model', e.target.value)}
          >
            {models.map((model) => (
              <option key={model.model_id} value={model.model_name}>
                {model.model_name}
              </option>
            ))}
          </select>
        </div>
      </div>
      {/* Temperature */}
      <div className={styles.dividerCls}>
              <div className={styles.rightbarh}>
                <h3>Temperature: </h3>
              </div>
              <div className={styles.botRandom}>
                <select
                  className={styles.selectorcls}
                  value={selectedTemperature}
                  onChange={(e) => updateSelection('Temperature', e.target.value)}
                >
                  {temperatures.map((temp, index) => (
                    <option key={index} value={temp}>
                      {temp}
                    </option>
                  ))}
                </select>
                <h3>0.0 = Auto</h3>
              </div>
            </div>
      {/* Agent Selection */}
      <div className={styles.dividerCls}>
        <div className={styles.rightbarh}>
          <h3>Agent Selected: </h3>
        </div>
        <div className={styles.botRandom}>
          <select
            className={styles.selectorcls}
            value={selectedAgent}
            onChange={(e) => updateSelection('Agent', e.target.value)}
          >
            {agents.map((agent) => (
              <option key={agent.agent_id} value={agent.agent_name}>
                {agent.agent_name}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};
