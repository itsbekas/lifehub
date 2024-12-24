export type Provider = {
  id: number;
  name: string;
  type: string;
  allow_custom_url: boolean;
  modules: Array<Module>;
};

export type Module = {
  id: number;
  name: string;
  type: string;
  providers: Array<Provider>;
};

export type User = {
  username: string;
  email: string;
  name: string;
  created_at: string;
};
