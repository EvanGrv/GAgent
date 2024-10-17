import React, { useState } from 'react';
import { FaPaperclip, FaPaperPlane } from 'react-icons/fa'; // Importer des icônes pour les boutons
import './app.css';  // Importer les styles

const ChatInput: React.FC<{ onSendMessage: (message: string) => void }> = ({ onSendMessage }) => {
    const [input, setInput] = useState('');

    const handleSendMessage = () => {
        if (input.trim()) {
            onSendMessage(input);  // Appelle la fonction de callback avec le message
            setInput('');  // Réinitialise le champ d'entrée
        }
    };

    return (
        <div className="chat-input-container">
            <FaPaperclip className="icon-attachment" />
            <input
                type="text"
                className="chat-input"
                placeholder="Message Ice Acquistion"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}  // Envoie le message quand "Enter" est appuyé
            />
            <FaPaperPlane className="icon-send" onClick={handleSendMessage} />
        </div>
    );
};

export default ChatInput;
