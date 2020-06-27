import axios from 'axios'

export class GestureData {
    data: Array<Array<any>>

    constructor(data: Array<Array<any>>) {
        this.data = data
    }

    toArray(): Array<Array<any>> {
        return [...this.data]
    }
}

export class Gesture {
    name: string
    projection2d: Array<Array<number>>
    projection3d: Array<Array<number>>
    gestureData: GestureData
    image: string
    prediction: Array<[number, string]>

    constructor (
        name?: string,
        image?: string,
        gestureData?: GestureData,
        projection2d?: Array<Array<number>>,
        projection3d?: Array<Array<number>>,
        prediction?: Array<[number, string]>
    ) {
        this.name = name
        this.image = image
        this.gestureData = gestureData
        this.projection2d = projection2d
        this.projection3d = projection3d
        this.prediction = prediction
    }
}

export const API_URL = ''

export async function train(name: string, gesture: GestureData, apiUrl: String = API_URL): Promise<Gesture> {
    let res = await axios.post(`${apiUrl}/train`, {
        name,
        gesture_data: gesture.toArray()
    })
    let { image, gesture_data, projection_2d, projection_3d } = res.data.gesture
    let gestureData = new GestureData(gesture_data)
    return new Gesture(
        name,
        `${apiUrl}/${image}`,
        gestureData,
        projection_2d,
        projection_3d
    )
}

export async function predict(gesture: GestureData, apiUrl: String = API_URL): Promise<Gesture> {
    let res = await axios.post(`${apiUrl}/predict`, {
        gesture_data: gesture.toArray()
    })
    let { name, image, gesture_data, projection_2d, projection_3d } = res.data.gesture
    let gestureData = new GestureData(gesture_data)
    let prediction = res.data.prediction
    return new Gesture(
        name,
        `${apiUrl}/${image}`,
        gestureData,
        projection_2d,
        projection_3d,
        prediction
    )
}

export async function retrain(apiUrl: String = API_URL) {
    let res = await axios.post(`${apiUrl}/retrain`)
}