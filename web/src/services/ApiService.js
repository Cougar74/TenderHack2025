import { useHttp } from "../hooks/http.hook";

const useApiService = () => {
    const { loading, request, error, clearError } = useHttp();

    const _apiBase = process.env.REACT_APP_API_URL;
    const getUuid = () => {
        let uuid = localStorage.getItem('uuid');

        if (!uuid) {
            uuid = crypto.randomUUID();
            localStorage.setItem('uuid', uuid);
        }

        return uuid;
    };

    const getUserHistory = async () => {
        const uuid = getUuid();
        const response = await request(`${_apiBase}/api/history/${uuid}`);

        return response.history;
    };

    const postQueryResponse = async (query) => {
        const uuid = getUuid();
        const response = await request(
            url=`${_apiBase}/api/query/${uuid}`,
            method = 'POST',
            body=JSON.stringify({ query }),
        );

        const { id, answer } = response;
        return { id, answer };
    };

    const postSetRate = async (id, rate) => {
        const uuid = getUuid();
        const response = await request(
            url=`${_apiBase}/api/rate/${uuid}`,
            method = 'POST',
            body=JSON.stringify({ id, rate }),
        );

        return;
    }

    return {
        loading,
        error,
        clearError,
        getUserHistory,
        postQueryResponse,
        postSetRate
    };
};

export default useApiService