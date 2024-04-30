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
