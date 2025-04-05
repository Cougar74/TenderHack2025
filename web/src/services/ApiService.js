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
        if (!query) {
            return;
        }

        const uuid = getUuid();

        const response = await request(
            `${_apiBase}/api/query/${uuid}`,
            'POST',
            JSON.stringify({ query }),
        );

        return response;
    };

    const postSetRate = async (id, rate) => {
        const response = await request(
            `${_apiBase}/api/set_rate/${id}`,
            'POST',
            JSON.stringify({ rate }),
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