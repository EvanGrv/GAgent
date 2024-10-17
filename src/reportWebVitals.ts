import { onCLS, onFID, onFCP, onLCP, onTTFB, Metric } from 'web-vitals';

const reportWebVitals = (onPerfEntry?: (metric: Metric) => void) => {
    if (onPerfEntry && typeof onPerfEntry === 'function') {
        onCLS(onPerfEntry);  // Passe correctement les métriques
        onFID(onPerfEntry);
        onFCP(onPerfEntry);
        onLCP(onPerfEntry);
        onTTFB(onPerfEntry);
    }
};

export default reportWebVitals;
