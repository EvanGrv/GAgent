import React from 'react';
import { FaCog, FaCommentDots, FaHome, FaRobot, FaStar } from 'react-icons/fa'; // Importation d'icônes

const Sidebar: React.FC = () => {
    return (
        <div className="sidebar">
            <div className="logo">ICE ANIMATION</div>
            <ul className="menu">
                <li><FaHome /> Ice Acquistion</li>
                <li><FaRobot /> Ice Animation</li>
                <li><FaCommentDots /> Ice with Index </li>
                <li><FaStar /> Soon...</li>
            </ul>
            <ul className="history">
            </ul>
        </div>
    );
};

export default Sidebar;
