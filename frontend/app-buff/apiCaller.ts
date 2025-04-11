import axios from "axios";

export const callApi = (urlApi: string, method = 'GET', data: any = null) => {
    // let urlApi = process.env.REACT_APP_API;

    let options: { url: string; method: string; data?: any } = {
         url: `http://localhost:8000${urlApi}`,
         method,
    };

    if (data !== null) {
         options["data"] = data;
    }

    return axios(options)
         .then((response) => response)
         .catch((error) => error.response);
};