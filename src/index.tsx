import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // Optionnel : inclure le fichier CSS si tu as des styles globaux
import App from './app'; // Le composant principal de ton application
import reportWebVitals from './reportWebVitals'; // Pour mesurer les performances (facultatif)

// Récupérer l'élément <div id="root"></div> dans public/index.html
const rootElement = document.getElementById('root');

// Créer la racine pour React
if (rootElement) {
    const root = ReactDOM.createRoot(rootElement);

    // Rendre l'application à l'intérieur du <div id="root"></div>
    root.render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
    );
}

// Si tu veux mesurer les performances, tu peux appeler la fonction reportWebVitals
// et envoyer les résultats à un service d'analyse ou les afficher dans la console
reportWebVitals();
