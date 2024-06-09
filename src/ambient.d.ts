type Provider = {
    id: number;
    name: string;
    type: string;
    modules: Array<Module>;
};

type Module = {
    id: number;
    name: string;
    type: string;
    providers: Array<Provider>;
};

type t212Transaction = {
    timestamp: string;
    amount: number;
    type: string;
    ticker: string;
}

type t212Data = {
    balance: {
        timestamp: string;
        free: number;
        invested: number;
        result: number;
    };
    history: Array<t212Transaction>;
}
