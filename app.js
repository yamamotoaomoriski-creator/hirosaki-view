/**
 * FOUR KINGS Command Room - LocalStorage Persistence Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    const AI_KEYS = ['chatgpt', 'gemini', 'grok', 'copilot'];
    const STORAGE_PREFIX = '4kings_command_room_';

    AI_KEYS.forEach((key) => {
        const inputElement = document.getElementById(`ai-${key}`);
        if (!inputElement) return;

        const storageKey = `${STORAGE_PREFIX}${key}`;

        // Load saved content from localStorage
        const savedContent = localStorage.getItem(storageKey);
        if (savedContent !== null) {
            inputElement.value = savedContent;
        }

        // Save input changes to localStorage
        inputElement.addEventListener('input', (event) => {
            localStorage.setItem(storageKey, event.target.value);
        });
    });
});
