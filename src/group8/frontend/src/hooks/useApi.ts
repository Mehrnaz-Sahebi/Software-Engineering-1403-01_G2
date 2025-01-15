// useApi.ts
import { useState, useCallback } from "react";
import axios, { AxiosRequestConfig, AxiosResponse, AxiosError } from "axios";

type HttpMethod = "get" | "post" | "put" | "patch" | "delete";

interface UseApiProps {
  url: string;
  method?: HttpMethod;
  headers?: Record<string, string> | null;
}

interface UseApiReturn<T> {
  response: T | null;
  error: AxiosError | null;
  loading: boolean;
  fetchData: (body?: unknown) => Promise<void>; // Accept a body parameter
}

const useApi = <T>({
  url,
  method = "get",
  headers = null,
}: UseApiProps): UseApiReturn<T> => {
  const [response, setResponse] = useState<T | null>(null);
  const [error, setError] = useState<AxiosError | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchData = useCallback(
    async (body?: unknown) => {
      setLoading(true);
      try {
        const config: AxiosRequestConfig = {
          method,
          url,
          data: body || null, // Use the provided body or fall back to null
          headers: headers || {},
        };
        const result: AxiosResponse<T> = await axios(config);
        setResponse(result.data);
      } catch (err) {
        setError(err as AxiosError);
      } finally {
        setLoading(false);
      }
    },
    [url, method, headers]
  );

  return { response, error, loading, fetchData };
};

export default useApi;
