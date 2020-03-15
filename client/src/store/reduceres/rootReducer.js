import { combineReducers } from "redux"

import quizReducer from "../reduceres/quizReducer"
import QuizTestRoundsReducer from "../reduceres/QuizTestRoundsReducer"
import mainPageReducer from "../reduceres/mainPageReducer"
import AuthReducer from "../reduceres/AuthReducer"
import RegistrationReducer from "../reduceres/RegistrationReducer"


export default combineReducers({
    quizReducer,
    QuizTestRoundsReducer,
    mainPageReducer,
    AuthReducer,
    RegistrationReducer
})