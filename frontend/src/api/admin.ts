import { api } from "~/lib/query";

export const adminApi = {
  getAllUsers: async () => {
    const response = await api.get("/admin/users");
    return response.data;
  },
  verifyUser: async (userId: string) => {
    await api.post(`/admin/users/${userId}/verify`);
  },
};
