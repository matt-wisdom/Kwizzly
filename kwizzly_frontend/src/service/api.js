import axios from 'axios'

function get_api(route){
    var api = axios.create({
        headers: {
        "Content-Type": "application/json",
        },
    });

    api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
        config.headers["Authorization"] = 'Bearer ' + token;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
    );
    api.interceptors.response.use(
        (res) => {
        return res;
        },
        async (err) => {
            try{
                if (err.response.status === 401) {
                    console.log("Removing key");
                    localStorage.removeItem('access_token');
                    //route.push("/login");
                    route;
                }
            }
            catch(err) {
                return Promise.reject("Error communicating with server: Server did not respond")
            }
        return Promise.reject(err);
        }
    );
    return api
}
export default get_api;