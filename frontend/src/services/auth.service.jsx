import { API_URL } from "@/api";

const TOKEN_KEY = import.meta.env.VITE_TOKEN_KEY || "access_token";
const USER_KEY = "user";

export class AuthService {
    async login(data = {}) {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
            },
        }).then((res) => res.json());

        if (response.access_token) {
            localStorage.setItem(TOKEN_KEY, response.access_token);
        }
        return response;
    }

    async signup(data = {}) {
        return await fetch(`${API_URL}/auth/signup`, {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
            },
        }).then((res) => res.json());
    }

    logout() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
    }

    getToken() {
        return localStorage.getItem(TOKEN_KEY);
    }

    isAuthenticated() {
        return Boolean(this.getToken());
    }

    saveUser(user = undefined) {
        if (!user) return;
        localStorage.setItem(USER_KEY, JSON.stringify(user));
    }

    getUser() {
        try {
            return JSON.parse(localStorage.getItem(USER_KEY));
        } catch (err) {
            return null;
        }
    }
}

export const authService = new AuthService();
