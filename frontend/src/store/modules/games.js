import axios from 'axios';

const actions = {
    async getGameList(page, token){
        return await axios.get('/api/v1/games/', {
            params: {
                page: page !== undefined ? page : 1,
            },
            headers: {
                "Authorization": token,
            },
        });
    }
  };

export default {actions};