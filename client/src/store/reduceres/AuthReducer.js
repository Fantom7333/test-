import { LOGOUT_USER, LOGIN_USER, LOG_ERROR_MASSAGE } from "../actions/actionTypes"


let initialState = {
    isAuth: false,
    authError: false
}


const AuthReducer = ( state = initialState, action ) => {
    switch( action.type ) {

        case LOGIN_USER:
            return {
                ...state,
                isAuth: true
            }
        case LOGOUT_USER:
            return {
                ...state,
                isAuth: false
            }    

        case LOG_ERROR_MASSAGE:
            return {
                ...state,
                authError: true
            }    
        default:
            return state
    }
}

export default AuthReducer