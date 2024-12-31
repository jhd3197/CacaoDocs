import data from './data.json';

export const fetchData = async () => {
    // Simulate an asynchronous fetch
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(data.data);
        }, 500);
    });
};