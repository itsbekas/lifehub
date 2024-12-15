type Provider = {
  id: number;
  name: string;
  type: string;
  allow_custom_url: boolean;
  modules: Array<Module>;
};

type Module = {
  id: number;
  name: string;
  type: string;
  providers: Array<Provider>;
};

type T212Transaction = {
  timestamp: string;
  amount: number;
  type: string;
  ticker: string;
};

type T212Data = {
  balance: {
    timestamp: string;
    free: number;
    invested: number;
    result: number;
  };
  history: Array<T212Transaction>;
};

type CalendarEvent = {
  id: number;
  title: string;
  start: string;
  end: string;
  location: string;
};

type User = {
  username: string;
  email: string;
  name: string;
  created_at: string;
};
