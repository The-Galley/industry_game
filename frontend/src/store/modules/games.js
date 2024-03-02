import axios from 'axios';
const url = 'https://industry-game.ru';

function getTokenFromCookie() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'token') {
            return value;
        }
    }
    return null;
}

const token = getTokenFromCookie();

export const actions = {
    async getGameList(page){
        return await axios.get(`${url}/api/v1/games/`, {
            params: {
                page: page !== undefined ? page : 1,
            },
            headers: {
                "Authorization": token,
            },
        });
    },
    async createGame(form) {
        return await axios.post(`${url}/api/v1/games/`, form, {
            headers: {
                "Authorization": token
            }
            });
        },
    async getGameById(game_id) {
        return await axios.get(`${url}/api/v1/games/${game_id}/`,  {
            headers: {
                "Authorization": token
            }
            });
        },
    async updateGameById(gameData, game_id) {
        return await axios.post(`${url}/api/v1/games/${game_id}/`, gameData, {
            headers: {
                "Authorization": token
            }
        });
    },
    async getUsersLobby(game_id) {
        return await axios.get(`${url}/api/v1/games/${game_id}/lobby/`,  {
            headers: {
                "Authorization": token
            }
        });
    },
    async addUsersLobby(game_id) {
        return await axios.post(`${url}/api/v1/games/${game_id}/lobby/`,  null,{
            headers: {
                "Authorization": token
            }
        });
    },
    async getUserCheck(game_id) {
        return await axios.get(`${url}/api/v1/games/${game_id}/lobby/status/`,  {
            headers: {
                "Authorization": token
            }
        });
    },
    async deleteUserFromLobby(game_id) {
        return await axios.delete(`${url}/api/v1/games/${game_id}/lobby/`,  {
            headers: {
                "Authorization": token
            }
        });
    },
  };

export default {actions};