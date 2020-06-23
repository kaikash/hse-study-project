export declare class GestureData {
    data: Array<Array<any>>;
    constructor(data: Array<Array<any>>);
    toArray(): Array<Array<any>>;
}
export declare class Gesture {
    name: string;
    projection2d: Array<Array<number>>;
    projection3d: Array<Array<number>>;
    gestureData: GestureData;
    image: string;
    prediction: Array<[number, string]>;
    constructor(name?: string, image?: string, gestureData?: GestureData, projection2d?: Array<Array<number>>, projection3d?: Array<Array<number>>, prediction?: Array<[number, string]>);
}
export declare const API_URL = "";
export declare function train(name: string, gesture: GestureData, apiUrl?: String): Promise<Gesture>;
export declare function predict(gesture: GestureData, apiUrl?: String): Promise<Gesture>;
export declare function retrain(apiUrl?: String): Promise<void>;
