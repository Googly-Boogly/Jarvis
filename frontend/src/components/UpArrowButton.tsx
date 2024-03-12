import React from 'react';

import UpArrowButton_module from './UpArrowButton.module.scss';

interface UpArrowButtonProps {
    onClick: () => void; // Adjust the type based on the expected onClick handler
}

const UpArrowButton: React.FC<UpArrowButtonProps> = ({ onClick }) => {
    return (
        <button onClick={onClick} className={UpArrowButton_module.NewClass}>
            <span className={UpArrowButton_module.uparrowcls}>&#8593;</span>{' '}
            {/* This is the up arrow character */}
        </button>
    );
};

export default UpArrowButton;
