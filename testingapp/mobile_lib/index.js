"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
exports.__esModule = true;
exports.retrain = exports.predict = exports.train = exports.API_URL = exports.Gesture = exports.GestureData = void 0;
var axios_1 = require("axios");
var GestureData = /** @class */ (function () {
    function GestureData(data) {
        this.data = data;
    }
    GestureData.prototype.toArray = function () {
        return __spreadArrays(this.data);
    };
    return GestureData;
}());
exports.GestureData = GestureData;
var Gesture = /** @class */ (function () {
    function Gesture(name, image, gestureData, projection2d, projection3d, prediction) {
        this.name = name;
        this.image = image;
        this.gestureData = gestureData;
        this.projection2d = projection2d;
        this.projection3d = projection3d;
        this.prediction = prediction;
    }
    return Gesture;
}());
exports.Gesture = Gesture;
exports.API_URL = '';
function train(name, gesture, apiUrl) {
    if (apiUrl === void 0) { apiUrl = exports.API_URL; }
    return __awaiter(this, void 0, void 0, function () {
        var res, _a, image, gesture_data, projection_2d, projection_3d, gestureData;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, axios_1["default"].post(apiUrl + "/train", {
                        name: name,
                        gesture_data: gesture.toArray()
                    })];
                case 1:
                    res = _b.sent();
                    _a = res.data.gesture, image = _a.image, gesture_data = _a.gesture_data, projection_2d = _a.projection_2d, projection_3d = _a.projection_3d;
                    gestureData = new GestureData(gesture_data);
                    return [2 /*return*/, new Gesture(name, apiUrl + "/" + image, gestureData, projection_2d, projection_3d)];
            }
        });
    });
}
exports.train = train;
function predict(gesture, apiUrl) {
    if (apiUrl === void 0) { apiUrl = exports.API_URL; }
    return __awaiter(this, void 0, void 0, function () {
        var res, _a, name, image, gesture_data, projection_2d, projection_3d, gestureData, prediction;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, axios_1["default"].post(apiUrl + "/predict", {
                        gesture_data: gesture.toArray()
                    })];
                case 1:
                    res = _b.sent();
                    _a = res.data.gesture, name = _a.name, image = _a.image, gesture_data = _a.gesture_data, projection_2d = _a.projection_2d, projection_3d = _a.projection_3d;
                    gestureData = new GestureData(gesture_data);
                    prediction = res.data.prediction;
                    return [2 /*return*/, new Gesture(name, apiUrl + "/" + image, gestureData, projection_2d, projection_3d, prediction)];
            }
        });
    });
}
exports.predict = predict;
function retrain(apiUrl) {
    if (apiUrl === void 0) { apiUrl = exports.API_URL; }
    return __awaiter(this, void 0, void 0, function () {
        var res;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, axios_1["default"].post(apiUrl + "/retrain")];
                case 1:
                    res = _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.retrain = retrain;
