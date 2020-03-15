import { EMAIL_ERROR, NAME_ERROR, REGISTER_ERROR } from "../actions/actionTypes"

const initialState = {
    isError: false,
    emailError: false,
    nameError: false
}



const RegistrationReducer = ( state = initialState, action ) => {
    switch( action.type ) {

        case EMAIL_ERROR:
            return {
                ...state,
                emailError: true
            }
        case NAME_ERROR:
            return {
                ...state,
                nameError: true
            }
        case REGISTER_ERROR:
            return {
                ...state,
                isError: action.errorType
            }
        default:
            return state
    }
}

export default RegistrationReducer