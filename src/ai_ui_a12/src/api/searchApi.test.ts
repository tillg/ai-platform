import { getBrainList } from './searchApi';
import { BrainModel } from './apiModelsSearch'; 

describe('getBrainList', () => {
    beforeEach(() => {
        global.fetch = jest.fn();
    });

    afterEach(() => {
        jest.resetAllMocks();
    });

    it('should return a list of BrainModel instances on success', async () => {
        const mockResponse = {
            result: [
                { id: 1, name: 'Brain1', description: 'Description1', path: '/path1', importer: 'importer1' },
                { id: 2, name: 'Brain2', description: 'Description2', path: '/path2', importer: 'importer2' }
            ]
        };

        (global.fetch as jest.Mock).mockResolvedValue({
            ok: true,
            json: async () => mockResponse
        });

        const brainList = await getBrainList();
        expect(brainList).toHaveLength(2);
        expect(brainList[0]).toBeInstanceOf(BrainModel);
        expect(brainList[0].id).toBe(1);
        expect(brainList[1].name).toBe('Brain2');
    });

    it('should throw an error if the fetch fails', async () => {
        (global.fetch as jest.Mock).mockResolvedValue({
            ok: false,
            status: 500,
            statusText: 'Internal Server Error'
        });

        await expect(getBrainList()).rejects.toThrow('Failed to fetch getBrainList: 500 Internal Server Error');
    });
});