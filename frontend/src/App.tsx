import React from 'react';
import classNames from 'classnames';
import styles from './App.module.scss';
import NavBar from './components/NavBar';
import ChatBox from './components/ChatBox';
import PastConvos from './components/PastConvos';
import { RightBar } from './components/right-bar/right-bar';
import { useWebState } from './hooks/useWebState'; // Adjust the import path as necessary

const App: React.FC = () => {
  const [webState, updateWebState, isLoading, error] = useWebState('http://localhost:7867/api/get_web_state');

  if (isLoading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error) {
    return <div className={styles.error}>Error: {error}</div>;
  }

  // Handlers for updating the state; these can be passed down to child components as needed
  const handleUpdateModel = (modelSelected: string) => updateWebState('modelSelected', modelSelected);
  const handleUpdateTemperature = (temperature: string) => updateWebState('temperature', temperature);
  const handleUpdateAgent = (agentSelected: string) => updateWebState('agentSelected', agentSelected);

  return (
    <div className={classNames(styles.app)}>
      <NavBar stt={webState.stt} tts={webState.tts} />
      <div className={styles.content}>
        <PastConvos previousconvo={webState.pastConvos} />
        <ChatBox />
        <RightBar
          modelSelected={webState.modelSelected}
          temperature={webState.temperature}
          agentSelected={webState.agentSelected}
          onUpdateModel={handleUpdateModel}
          onUpdateTemperature={handleUpdateTemperature}
          onUpdateAgent={handleUpdateAgent}
          models={webState.models}
          agents={webState.agents}
        />
      </div>
    </div>
  );
};

export default App;
