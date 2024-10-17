import React from 'react';
import './app.css';  // Inclure les styles globaux
import Sidebar from './Sidebar';
import MainContent from './MainContent';
import ChatInput from './ChatInput';


const App: React.FC = () => {
    const handleSendMessage = (message: string) => {
        console.log("Message envoyé :", message);
        // Ajoute la logique pour envoyer le message à l'assistant
    };
    return (
        <div className="app-container">
            <Sidebar />
            <MainContent />
            <ChatInput onSendMessage={handleSendMessage} />
        </div>

    );
}

export default App;
