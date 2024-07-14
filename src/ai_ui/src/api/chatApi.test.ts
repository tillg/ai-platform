import { chatApi } from './chatApi';
import { ChatRequest } from './apiModelsChat';
import { beforeEach, describe } from 'node:test';

// Mocking the global fetch function
global.fetch = jest.fn();

// Utility function to mock fetch responses
const mockFetchResponse = (ok: boolean, status: number, statusText: string, content?: string) => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok,
        status,
        statusText,
        json: () => Promise.resolve({ content }),
    });
};

describe('chatApi', () => {
    const request: ChatRequest = {
        messages: []
    };

    beforeEach(() => {
        (global.fetch as jest.Mock).mockClear();
    });

    it('should return a ChatResponse on successful fetch', async () => {
        mockFetchResponse(true, 200, 'OK', 'Test content');

        const response = await chatApi(request);

        expect(response).toEqual({
            content: 'Test content',
            inner_working: {
                detail: 'It worked 😉',
            },
        });
    });

    it('should throw an error if content field is missing in the response', async () => {
        mockFetchResponse(true, 200, 'OK');

        await expect(chatApi(request)).rejects.toThrow('Content field is missing in the response');
    });

    it('should throw an error on failed fetch', async () => {
        mockFetchResponse(false, 404, 'Not Found');

        await expect(chatApi(request)).rejects.toThrow('Failed to fetch chatApi: 404 Not Found');
    });
});