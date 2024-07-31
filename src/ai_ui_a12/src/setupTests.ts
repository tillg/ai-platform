// src/setupTests.ts

import '@testing-library/jest-dom';

class MockResizeObserver {
    // You can optionally type the callback for better code documentation
    private callback: ResizeObserverCallback;

    constructor(callback: ResizeObserverCallback) {
        this.callback = callback;
    }

    observe(target: Element): void {
        // Optionally implement mock behavior
    }

    unobserve(target: Element): void {
        // Optionally implement mock behavior
    }

    disconnect(): void {
        // Optionally implement mock behavior
    }
}

// Assign the mock class to global.ResizeObserver
Object.defineProperty(window, 'ResizeObserver', {
    writable: true,
    configurable: true,
    value: MockResizeObserver
});


// Check if scrollIntoView is not already defined (to avoid overwriting it in environments where it exists)
if (!Element.prototype.scrollIntoView) {
    Element.prototype.scrollIntoView = jest.fn();
}