import React from 'react';
import { X } from 'lucide-react';
import Button from './Button';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = 'md'
}) => {
  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="flex min-h-screen items-center justify-center p-2 sm:p-4">
        {/* Backdrop */}
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
          onClick={onClose}
        />
        
        {/* Modal */}
        <div className={`modal-element ${sizeClasses[size]} mx-2 sm:mx-4`}>
          {/* Header */}
          {title && (
            <div className="modal-header">
              <h3 className="text-lg font-medium text-gray-900">{title}</h3>
              <Button
                variant="secondary"
                size="sm"
                icon={X}
                onClick={onClose}
                className="!p-1"
              />
            </div>
          )}
          
          {/* Content */}
          <div className="modal-body">
            {children}
          </div>
          
          {/* Footer */}
          {footer && (
            <div className="modal-footer">
              {footer}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Modal;
